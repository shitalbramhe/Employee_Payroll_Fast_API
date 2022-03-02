"""
@Author: Shital Bajait
@Date: 21-02-2022 13:56:00
@Last Modified by: Shital Bajait 
@Last Modified time: 22-02-2022 12:56:00
@Title : create user for EMployee Payroll 
"""
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI, HTTPException, status
import jwt_auth
from schemas import Employee, Token, User
from fastapi import Depends, FastAPI, HTTPException, status



app = FastAPI()

db={}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = jwt_auth.authenticate_user(jwt_auth.fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=jwt_auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt_auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get('/')
def index():
    return{"Employee Payroll APP"}

@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(jwt_auth.get_current_active_user)):
    return current_user


@app.post('/add_employee/{Employee_id}')
def add_employee_data(Employee_id: int,employee: Employee,current_user: User = Depends(jwt_auth.get_current_active_user)):
    db[Employee_id] = {"Name": employee.Name,"Profile_image": employee.Profile_image,"Gender": employee.Gender,
                       "Department": employee.Department,"Salary": employee.Salary,
                       "Start_Date": employee.Start_Date,"Notes": employee.Notes}
    return {"message","Employee Details added successfully"}

@app.get('/get_employee/{Employee_id}')
def single_employee_data(Employee_id: int,current_user: User = Depends(jwt_auth.get_current_active_user)):
    """
            Description:
                Function get single Employee data
            Parameter:
                None
            Return:
                None
        """
    return db[Employee_id]

@app.get('/get_all_employee')
def get_all_employee(current_user: User = Depends(jwt_auth.get_current_active_user)):
    return db

@app.delete('/delete_employee/{Employee_id}')
def delete_Employee(Employee_id: int,current_user: User = Depends(jwt_auth.get_current_active_user)):
    if Employee_id not in db:
        return {"error","employee is not present in database"}
    del db[Employee_id]
    return {"message","Successfully deleted Employee details"}

@app.put('/update_employee_data/{Employee_id}')
def update_employee_name(Employee_id: int, employee:Employee,current_user: User = Depends(jwt_auth.get_current_active_user)):
    if Employee_id not in db:
        return {"error":"Employee details not found"}

    if employee.Name is not None:
        db[Employee_id]["Name"] = employee.Name
        return {"message":"Employee name updated successfully"}

    if employee.Profile_image is not None:
        db[Employee_id]["Profile_image"] = employee.Profile_image
        return {"message":"Employee Profile_image updated successfully"}

    if employee.Gender is not None:
        db[Employee_id]["Gender"] = employee.Gender
        return {"message":"Employee Gender updated successfully"}

    if employee.Department is not None:
        db[Employee_id]["Department"] = employee.Department
        return {"message":"Employee Department updated successfully"}

    if employee.Salary is not None:
        db[Employee_id]["Salary"] = employee.Salary
        return {"message":"Employee Salary updated successfully"}

    if employee.Start_Date is not None:
        db[Employee_id]["Start_Date"] = employee.Start_Date
        return {"message":"Employee Start_Date updated successfully"}  