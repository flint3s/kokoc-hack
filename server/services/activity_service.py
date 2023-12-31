import datetime
import os
import uuid

import aiofiles
from aiohttp.web_fileresponse import FileResponse
from data.database_service import DatabaseService

from data.model.activity_request import ActivityRequest
from fastapi import HTTPException

from services.employee_service import EmployeeService
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from PIL import Image

from data.model.activity import Activity

from data.model.step_activity import StepActivity

from data.model.employee import Employee

PATH = os.path.join(os.getcwd())


class ActivityService:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def create_activity_request(self, employee_id: int, training_information: str,
                                      adding_kilocalories_count: int, images: str):
        async with AsyncSession(self.database_service.engine) as session:
            activity_request = ActivityRequest(employee_id=employee_id, training_information=training_information,
                                               adding_kilocalories_count=adding_kilocalories_count,
                                               date=datetime.datetime.now(), images=images)

            employee_id = activity_request.employee_id
            year = activity_request.date.year
            month = activity_request.date.month

            st = select(Activity) \
                .where(Activity.employee_id == employee_id) \
                .where(Activity.year_number == year) \
                .where(Activity.month_number == month) \
                .limit(1)
            result = (await session.execute(st)).first()

            activity = None
            if result is not None:
                activity = result[0]
            else:
                activity = Activity(employee_id=employee_id, kilocalories_count=0, year_number=year, month_number=month)

            activity.kilocalories_count += activity_request.adding_kilocalories_count
            session.add(activity)
            await session.commit()
            await session.refresh(activity)

            return await self.database_service.save(activity_request)

    async def save_training_imamge(self, file):
        file_only_name = f'{uuid.uuid4().hex}' + file.filename
        file_name = "/code/public/" + file_only_name
        try:
            im = Image.open(file.file)
            im.save(file_name)
        except Exception:
            raise HTTPException(status_code=500, detail='Что-то пошло не так')
        finally:
            file.file.close()
            im.close()

        return "static/" + file_only_name

    async def get_all_activity_requests_in_company(self, company_id: int):
        employee_service = EmployeeService(self.database_service)
        activity_requests = list()

        employees = await employee_service.get_employees_in_company(company_id)
        for employee in employees:
            for activity_request in employee.activities_requests:
                activity_requests.append(activity_request)

        return activity_requests

    async def get_activity_request_by_id(self, activity_request_id: int):
        async with AsyncSession(self.database_service.engine) as session:
            st = select(ActivityRequest) \
                .where(ActivityRequest.id == activity_request_id) \
                .limit(1)
            result = (await session.execute(st)).first()

            if result:
                return result[0]

    async def get_image_from_activity_request(self, activity_request_id: int):
        activity_request = await self.get_activity_request_by_id(activity_request_id)

        return FileResponse(activity_request.image_path)

    async def get_activity_by_date(self, employee_id: int, month: int, year: int):
        async with AsyncSession(self.database_service.engine) as session:
            st = select(Activity) \
                .where(Activity.employee_id == employee_id) \
                .where(Activity.year_number == year) \
                .where(Activity.month_number == month) \
                .limit(1)
            result = (await session.execute(st)).first()

            if result is not None:
                return result[0]
            else:
                return Activity(employee_id=employee_id, kilocalories_count=0, year_number=year, month_number=month)

    async def get_employees_descending_list_in_company(self, company_id: int):
        async with AsyncSession(self.database_service.engine) as session:

            date = datetime.datetime.now()
            year = date.year
            month = date.month

            employee_service = EmployeeService(self.database_service)
            employees = await employee_service.get_employees_in_company(company_id)
            employees_result = list()
            for employee in employees:
                st = select(Activity) \
                    .where(Activity.employee_id == employee.id) \
                    .where(Activity.year_number == year) \
                    .where(Activity.month_number == month) \
                    .limit(1)
                result = (await session.execute(st)).first()
                activity = None
                if result is not None:
                    activity = result[0]
                else:
                    activity = Activity(employee_id=employee.id, kilocalories_count=0, year_number=year,
                                        month_number=month)
                employees_result.append({
                    "kilocalories_count": activity.kilocalories_count,
                    "employee": employee
                })

            employees_result.sort(key=lambda x: x.get("kilocalories_count"), reverse=True)

            return employees_result

    async def get_employees_descending_list(self):
        async with AsyncSession(self.database_service.engine) as session:

            date = datetime.datetime.now()
            year = date.year
            month = date.month

            employee_service = EmployeeService(self.database_service)
            employees = await employee_service.get_all_base_models_approved_employees()
            employees_result = list()
            for employee in employees:
                st = select(Activity) \
                    .where(Activity.employee_id == employee.id) \
                    .where(Activity.year_number == year) \
                    .where(Activity.month_number == month) \
                    .limit(1)
                result = (await session.execute(st)).first()
                activity = None
                if result is not None:
                    activity = result[0]
                else:
                    activity = Activity(employee_id=employee.id, kilocalories_count=0, year_number=year,
                                        month_number=month)
                employees_result.append({
                    "kilocalories_count": activity.kilocalories_count,
                    "employee": employee
                })

            employees_result.sort(key=lambda x: x.get("kilocalories_count"), reverse=True)

            return employees_result

    async def add_steps(self, employee_id: int, count: int, human_weight: int):
        async with AsyncSession(self.database_service.engine) as session:
            date = datetime.datetime.now()
            year = date.year
            month = date.month
            day = date.day

            st = select(StepActivity) \
                .where(StepActivity.employee_id == employee_id) \
                .where(StepActivity.year == year) \
                .where(StepActivity.month == month) \
                .where(StepActivity.day == day) \
                .limit(1)
            result = (await session.execute(st)).first()

            if result is not None:
                activity = result[0]
            else:
                activity = StepActivity(employee_id=employee_id, kilocalories_count=0, year=year, month=month, day=day)

            activity.count += count
            session.add(activity)
            await session.commit()
            await session.refresh(activity)

            st = select(Activity) \
                .where(Activity.employee_id == employee_id) \
                .where(Activity.year_number == year) \
                .where(Activity.month_number == month) \
                .limit(1)
            result = (await session.execute(st)).first()

            if result is not None:
                activity = result[0]
            else:
                activity = Activity(employee_id=employee_id, kilocalories_count=0, year_number=year, month_number=month)

            average_stride_length = 0.79
            step_factor = 0.0009
            activity.kilocalories_count += count * average_stride_length * human_weight * step_factor
            session.add(activity)
            await session.commit()
            await session.refresh(activity)

        return activity

    async def get_activities_request_by_employee(self, employee_id):
        async with AsyncSession(self.database_service.engine) as session:
            st = select(Employee) \
                .where(Employee.id == employee_id) \
                .limit(1)
            result = (await session.execute(st)).first()
            employee = result[0]

            return employee.activities_requests
