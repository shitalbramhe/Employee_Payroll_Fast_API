from typing import Optional
from pydantic import BaseModel
from datetime import date
import pydantic
from fastapi import Depends, FastAPI, HTTPException, status

class Employee(BaseModel):
    Name : Optional[str] = None
    Profile_image: Optional[str] = None
    Gender : Optional[str] = None
    Department : Optional[str] = None
    Salary : Optional[float] = None
    Start_Date : Optional[date] = None
    Notes : Optional[str] = None

    @pydantic.validator("Salary")
    @classmethod
    def Salary_valid(cls, Salary):
        if not Salary>10000.00 and Salary<400000.00:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Salary should be in range 10000 to 400000')
        return Salary

    @pydantic.validator("Department")
    @classmethod
    def Department_valid(cls, Department):
        chars = ["HR","IT","Sales","Account","Marketing" ]
        if Department not in chars:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Invalid Department name')
        return Department      
            
    @pydantic.validator("Gender")
    @classmethod
    def Gender_valid(cls, Gender):
        chars = ["Female" , "Male", "F", "M" ]
        if Gender not in chars:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'Gender should be Male or Female')
        return Gender

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str