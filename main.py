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
import model
from database import SessionLocal,engine
from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

model.Base.metadata.create_all(bind=engine)
app = FastAPI()

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
def add_employee_data(Employee_id: int,employee: Employee,current_user: User = Depends(jwt_auth.get_current_active_user),db:Session=Depends(get_db)):
    u=model.User(id=Employee_id, Name = employee.Name,Profile_image= employee.Profile_image,Gender=employee.Gender,
                Department= employee.Department, Salary =employee.Salary,Start_Date= employee.Start_Date,Notes=employee.Notes)
    db.add(u)
    db.commit()
    return u

@app.get('/get_employee/{Employee_id}')
def single_employee_data(Employee_id: int,current_user: User = Depends(jwt_auth.get_current_active_user),db:Session=Depends(get_db)):
    u=db.query(model.User).filter(model.User.id == Employee_id).first()
    return u

@app.get('/get_all_employee')
def get_all_employee(current_user: User = Depends(jwt_auth.get_current_active_user),db:Session=Depends(get_db)):
    data = db.query(model.User).all()
    return data

@app.delete('/delete_employee/{Employee_id}')
def delete_Employee(Employee_id: int,current_user: User = Depends(jwt_auth.get_current_active_user),db:Session=Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == Employee_id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{Employee_id} not found")

    user.delete(synchronize_session=False)
    db.commit()
    return {"data delete successfully"}
    

@app.put('/update_employee_data/{Employee_id}')
def update_employee(Employee_id: int, employee:Employee,current_user: User = Depends(jwt_auth.get_current_active_user),db:Session=Depends(get_db)):
    try:
        u=db.query(model.User).filter(model.User.id == Employee_id).first()
        if employee.Name is not None:
            u.Name = employee.Name
        if employee.Profile_image is not None:
            u.Profile_image = employee.Profile_image
        if employee.Gender is not None:
            u.Gender = employee.Gender
        if employee.Department is not None:
            u.Department = employee.Department
        if employee.Salary is not None:
            u.Salary = employee.Salary
        if employee.Start_Date is not None:
            u.Start_Date = employee.Start_Date
        db.add(u)
        db.commit()
        return u
    except:
        return HTTPException(status_code=404,detail="employee is not found")