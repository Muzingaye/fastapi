class ProviderData(BaseModel):
    response_code: str | None = None


class Result(BaseModel):
    status: str
    category: str
    sub_category: str


class Data(BaseModel):
    id: str
    result: Result
    reconciliation_id: str
    amount: str
    currency: str
    provider_data: ProviderData | None = None


class PayUPost(BaseModel):
    id: str
    account_id: str
    payment_id: str
    created: str
    app_id: str
    data: Data