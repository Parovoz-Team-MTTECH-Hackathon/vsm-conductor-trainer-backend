from pydantic import BaseModel, EmailStr, ConfigDict


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class PlayerSignupRequest(UserLoginRequest):
    first_name: str
    last_name: str
    patronymic_name: str


class ManagerSignupRequest(UserLoginRequest):
    name: str


class IntegrationLoginRequest(BaseModel):
    key: str
    secret: str

class IntegrationSignupRequest(IntegrationLoginRequest):
    name: str


class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str

class DeleteRequest(BaseModel):
    client_id: int