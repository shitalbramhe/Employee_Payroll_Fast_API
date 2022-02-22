"""
@Author: Shital Bajait
@Date: 21-02-2022 13:56:00
@Last Modified by: Shital Bajait 
@Last Modified time: 21-02-2022 13:56:00
@Title : create user for EMployee Payroll 
"""
from datetime import date
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

db={}

class Employee(BaseModel):
    Name : Optional[str] = None
    Profile_image: Optional[str] = None
    Gender : Optional[str] = None
    Department : Optional[str] = None
    Salary : Optional[float] = None
    Start_Date : Optional[date] = None
    Notes : Optional[str] = None


@app.get('/')
def index():
    return{"Employee Payroll APP"}


@app.post('/add_employee/{Employee_id}')
def add_employee_data(Employee_id: int,employee: Employee):
    db[Employee_id] = {"Name": employee.Name,"Profile_image": employee.Profile_image,"Gender": employee.Gender,
                       "Department": employee.Department,"Salary": employee.Salary,
                       "Start_Date": employee.Start_Date,"Notes": employee.Notes}
    return {"message","Employee Details added successfully"}

@app.get('/get_employee/{Employee_id}')
def single_employee_data(Employee_id: int):
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
def get_all_employee():
    return db

@app.delete('/delete_employee')
def delete_Employee(Employee_id: int,employee: Employee):
    if Employee_id not in db:
        return {"error","employee is not present in database"}
    del db[Employee_id]
    return {"message","Successfully deleted Employee details"}

@app.put('/update_employee_data/{Employee_id}')
def update_employee_name(Employee_id: int, employee:Employee):
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

    