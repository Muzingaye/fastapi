from fastapi import APIRouter, Depends, HTTPException, status
from api.schemas import payments
from api.config import settings
import hashlib
import hmac
import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

router = APIRouter(
    prefix="/payu/callback",
    tags= ["Payments"]
)
logger = logging.getLogger(__name__)

@router.post(response_model=payments.ProviderData)
async def payu_callback( request: payments.Request, payment: payments.PayUPost):

    signature_header = request.headers.get("signature")
    event_type = request.headers.get("event-type")

    if not signature_header:
        logger.error(
            "PayU callback missing signature: payment_id=%s",
            payment.payment_id,
        )

        raise HTTPException(
            status_code=401,
            detail="Missing signature",
        )

    if not event_type:
        logger.error(
            "PayU callback missing event-type: payment_id=%s",
            payment.payment_id,
        )

        raise HTTPException(
            status_code=400,
            detail="Missing event type",
        )

    signature = signature_header.removeprefix("sig1=")

    if payment.data.provider_data is None:
        payment.data.provider_data = payments.ProviderData()

    payment.data.provider_data.response_code = "true"

    payment.data.currency = "ZAR"


    message = build_signature_message(
        event_type,
        payment,
    )

    # -----------------------------
    # 5. Calculate HMAC
    # -----------------------------

    expected_signature = calculate_signature(
        message,
        settings.pay_private_key,
    )

    # -----------------------------
    # 6. Verify signature
    # -----------------------------

    if not hmac.compare_digest(
        expected_signature,
        signature,
    ):
        logger.error(
            "PayU signature mismatch: payment_id=%s",
            payment.payment_id,
        )

        raise HTTPException(
            status_code=401,
            detail="Invalid signature",
        )

    # -----------------------------
    # 7. Determine status
    # -----------------------------

    payu_status = payment.data.result.status

    if payu_status == "Succeed":
        status = "A"

    elif payu_status == "Pending":
        status = "P"

    else:
        status = "D"

    transaction = await get_transaction_by_reference(
        payment.data.reconciliation_id
    )

    if not transaction:
        logger.error(
            "PayU transaction not found: reconciliation_id=%s",
            payment.data.reconciliation_id,
        )

        raise HTTPException(
            status_code=404,
            detail="Transaction not found",
        )

    if transaction.status != "A":

        await save_payu_transaction(
            transaction_id=transaction.id,
            account_id=transaction.telebet_account,
            reference=transaction.reference,
            payment_id=transaction.payment_id,
            amount=transaction.amount,
            status=status,
        )

        # -------------------------
        # 10. Credit account
        # -------------------------

        if status == "A":

            result = await account_deposit(
                gateway_user="gateway-user",
                password="password",
                account_id=transaction.telebet_account,
                amount=transaction.amount,
                reference=transaction.reference,
            )

            if result.error_code != 0:
                logger.error(
                    "Account deposit failed: "
                    "account=%s reference=%s error=%s",
                    transaction.telebet_account,
                    transaction.reference,
                    result.error_string,
                )

    # -----------------------------
    # 11. Tell PayU we received it
    # -----------------------------

    return Response(status_code=200)


def calculate_signature(message: str, private_key: str) -> str:
    signature = hmac.new(
        private_key.encode("ascii"),
        message.encode("ascii"),
        hashlib.sha256,
    ).hexdigest()

    return signature.lower()