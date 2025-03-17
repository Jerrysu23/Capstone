from pydantic import BaseModel, validator, root_validator, model_validator
from typing import Optional, List
from backend.schema.job import Job


class Address(BaseModel):
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None


class UserInDB(BaseModel):
    user_type: str = "Job Seeker"
    name: Optional[str] = None
    username: str
    hashed_password: str
    birthday: Optional[str] = None
    ethnicity: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[Address] = None
    jobs: Optional[list[Job]] = None
    photo: Optional[bytes] = None


class UserCreate(BaseModel):
    username: str
    password: str
    email: str


class CompanyUserInDB(BaseModel):
    user_type: str = "Company"
    name: str
    username: str
    hashed_password: str
    email: str
    company: str


class CompanyUserResponse(BaseModel):
    name: str
    username: str
    email: str
    company: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    birthday: Optional[str] = None
    ethnicity: Optional[str] = None
    phone: Optional[str] = None
    line_1: Optional[str] = None
    line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    photo: Optional[str] = None

    @model_validator(mode='before')
    def check_address(cls, values):
        line_1 = values.get('line_1')
        if line_1:
            if not values.get('city'):
                raise ValueError('city is required if line_1 is provided')
            if not values.get('state'):
                raise ValueError('state is required if line_1 is provided')
            if not values.get('zip'):
                raise ValueError('zip is required if line_1 is provided')
        return values


class UserEmailUpdate(BaseModel):
    currentEmail: str
    newEmail: str


class UserPasswordUpdate(BaseModel):
    oldPassword: str
    newPassword: str
    confirmPassword: str


class User(BaseModel):
    name: Optional[str] = None
    username: str
    hashed_password: str
    email: str
    company: Optional[str] = None


class UserResponse(BaseModel):
    user: User


class UserInfoUpdateResponse(BaseModel):
    message: str


class UserUpdateResponse(BaseModel):
    name: Optional[str] = None
    username: str
    birthday: Optional[str] = None
    ethnicity: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[Address] = None
    photo: Optional[bytes] = None


class UpdateEmailResponse(BaseModel):
    message: str


class HelperResponses(BaseModel):
    response: str


class HelperResponsesResponse(BaseModel):
    responses: List[HelperResponses]
