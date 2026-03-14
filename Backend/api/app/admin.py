from fastapi import APIRouter, Depends, Request
from api.security import verify_token
from fastapi import Header
from sqlalchemy.exc import IntegrityError

from api.schemas import *
from models.user import User
from api.jwt import *

app = APIRouter(tags=["Admin"],prefix="/api/admin",dependencies=[Depends(verify_token)])

@app.get("/teachers/", response_model=list[UserOut])
async def teacher(request: Request):
    user=request.state.user
    if user.role!="admin":
        return {"error": "Unauthorized"}
    
    teachers=User.objects.filter(role="teacher")
    return teachers


@app.post("/teachers", response_model=UserOut)
async def create_teacher(user:  UserCreate,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    try:
        teacher=User.objects.create(name=user.name,email=user.email,hashed_password=user.password,role=user.role)
    except IntegrityError:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    return teacher


@app.get("/teachers/{teacher_id}/", response_model=UserOut)
async def teacher_detail(teacher_id: int,request: Request):
    user=request.state.user
    if user.role!="admin":
        return {"error": "Unauthorized"}
    
    teacher=User.objects.get(id=teacher_id)
    if teacher is None:
        return {"error": "Teacher not found"}
    
    return teacher


@app.delete("/teachers/{teacher_id}/")
async def delete_teacher(teacher_id: int,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    teacher=User.objects.get(id=teacher_id)
    if teacher is None:
        return {"error": "Teacher not found"}
    
    teacher.delete()
    return {"message": "Teacher deleted successfully"}


@app.put("/teachers/{teacher_id}/", response_model=UserOut)
async def update_teacher(teacher_id: int, user_data: UserOut, request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    teacher = User.objects.get(id=teacher_id)

    if not teacher:
        return {"error": "Teacher not found"}
    
    update_data = user_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(teacher, key, value)
    
    if user_data.hashed_password:
        teacher.hashed_password = user_data.hashed_password

    teacher.save()

    return teacher


@app.get("/students/", response_model=list[StudentOut])
async def student_(request: Request):
    user=request.state.user
    if user.role!="admin":
        return {"error": "Unauthorized"}
    
    students=Student.objects.all()
    return students


@app.post("/students", response_model=StudentCreate)
async def create_student(student:  StudentCreate,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    student=Student.objects.create(name=student.name,email=student.email,phone=student.phone)
    return student


@app.get("/students/{student_id}/", response_model=StudentOut)
async def student_detail(student_id: int,request: Request):
    user=request.state.user
    if user.role!="admin":
        return {"error": "Unauthorized"}
    
    student=Student.objects.get(id=student_id)
    if student is None:
        return {"error": "Student not found"}
    
    return student

@app.put("/students/{student_id}/", response_model=StudentOut)
async def update_student(student_id: int, student_data: StudentOut, request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    student = Student.objects.get(id=student_id)

    if not student:
        return {"error": "Student not found"}
    
    update_data = student_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(student, key, value)
    
    student.save()

    return student


@app.delete("/students/{student_id}/")
async def delete_student(student_id: int,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    student=Student.objects.get(id=student_id)
    if student is None:
        return {"error": "Student not found"}
    
    student.delete()
    return {"message": "Student deleted successfully"}


@app.get("/groups/", response_model=list[GroupOut])
async def group_list(request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    groups=Group.objects.all()
    return groups

@app.post("/groups/", response_model=GroupCreate)
async def create_group(group: GroupCreate,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    group=Group.objects.create(slug=group.slug,name=group.name,description=group.description,teacher_id=group.teacher_id)
    return group


@app.get("/groups/{group_id}/", response_model=GroupOut)
async def group_detail(group_id: int,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    group=Group.objects.get(id=group_id)
    if group is None:
        return {"error": "Group not found"}
    
    return group

@app.put("/groups/{group_id}/", response_model=GroupCreate)
async def update_group(group_id: int, group_data: GroupCreate, request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}

    group = Group.objects.get(id=group_id)

    if not group:
        return {"error": "Group not found"}

    update_data = group_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(group, key if key != 'created_at' else 'updated_at', value)

    group.save()
    return group


@app.delete("/groups/{group_id}/")
async def delete_group(group_id: int,request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    group=Group.objects.get(id=group_id)
    if group is None:
        return {"error": "Group not found"}
    
    group.delete()
    return {"message": "Group deleted successfully"}


@app.post("/groups/{group_id}/students/{student_id}/")
async def add_student_to_group(group_id: int, student_id: int, request: Request):
    u=request.state.user
    if u.role!="admin":
        return {"error": "Unauthorized"}
    
    group = Group.objects.get(id=group_id)
    student = Student.objects.get(id=student_id)

    if not group or not student:
        return {"error": "Group or Student not found"}

    group.students.append(student)
    group.save()

    return {"message": "Student added to group successfully"}




@app.delete("/groups/{group_id}/students/{student_id}/")
async def delete_student_to_groups(group_id: int, student_id: int,request: Request):
    u=request.state.user
    if u.role!='admin':
        return {"error": "Unauthorized"}

    group=Group.objects.get(id=group_id)
    group.students=[i for i in group.students if i.id!=student_id]
    group.save()
    return group.students




