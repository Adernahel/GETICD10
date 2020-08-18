from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

Base = declarative_base()

class Visit(Base):
    __tablename__= 'visit'
    id = Column(Integer, primary_key=True)
    OrderID = Column(Integer,ForeignKey('order.id'))
    Physicianid = Column(Integer,ForeignKey('employee.id'))
    Closing_date = Column(Date)
   
    Physician = relationship("EmployeeModel")
    Order = relationship("Order")
    
    def __repr__(self):
        return "<Visit(OrderID={},Physicianid={},Closing_date={})>"\
            .format(self.OrderID,self.Physicianid,self.Closing_date)

class EmployeeModel(Base):
    __tablename__= 'employee'
    id = Column(Integer, primary_key=True)
    FirstName = Column(String(30))
    LastName = Column(String(50))
    LicenseNo = Column(String(20))
    HireDate = Column(Date)
    Age = Column(Integer)

    def __repr__(self):
        return "<EmployeeModel(FirstName='{}',LastName='{}',LicenseNo='{}',HireDate={},Age={})>"\
            .format(self.FirstName,self.LastName,self.LicenseNo,self.HireDate,self.Age)

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer,primary_key=True)
    RoleName = Column(String(20))
    RoleType = Column(Integer)
    
    def __repr__(self):
        return "<Roles(RoleName='{}'),RoleType='{}'>"\
            .format(self.RoleName,self.RoleType)

class EmployeeRoles(Base):
    __tablename__ = 'employeeroles'
    EmployeeId = Column(Integer,ForeignKey('employee.id'),primary_key=True)
    RoleId= Column(Integer,ForeignKey('roles.id'),primary_key=True)
    
    Employee = relationship("EmployeeModel")
    Roles = relationship("Roles")
    
    def __repr__(self):
        return "<EmployeeRoles(EmployeeId={},RoleId={})>"\
            .format(self.EmployeeId,self.RoleId)

class Service(Base):
    __tablename__= 'services'
    id = Column(Integer,primary_key=True)
    ServiceName = Column(String(40))
    ServiceShort = Column(String(10))
    ServicePrice = Column(Integer) 
    ServiceCost = Column(Integer)
    ServiceDuration = Column(Integer)

    def __repr__(self):
        return "<Service(ServiceName='{}',ServiceShort='{}',ServicePrice={},ServiceCost={},ServiceDuration={}>"\
            .format(self.ServiceName,self.ServiceShort,self.ServicePrice,self.ServiceCost,self.ServiceDuration)

class Procedures(Base):
    __tablename__= 'proceduresdict'
    id = Column(Integer,primary_key=True)
    ICD9 = Column(String(5))
    Name = Column(String(40))
    Version= Column(String(15))

    def __repr__(self):
        return "<Procedures(ICD9='{}',Name='{}',Version='{}')>"\
            .format(self.ICD9,self.Name,self.Version)

class VisitProcedures(Base):
    __tablename__= 'visitprocedures'
    VisitId = Column(Integer,ForeignKey('visit.id'),primary_key=True)
    ProcId = Column(Integer,ForeignKey('proceduresdict.id'),primary_key=True)

    Visit = relationship("Visit")
    Proc = relationship("Procedures")

    def __repr__(self):
        return "<VisitProcedures(VisitId={},ProcId={})>"\
            .format(self.VisitId,self.ProcId)

class Diagnosis(Base):
    __tablename__= 'diagnosisdict'
    id = Column(Integer,primary_key=True)
    ICD10 = Column(String(10))
    Name = Column(String(250)) 
    Version = Column(String(15))

    def __repr__(self):
        return "<Diagnosis(ICD10='{}',Name='{}',Version='{}')>"\
            .format(self.ICD10,self.Name,self.Version)

class VisitDiagnosis(Base):
    __tablename__= 'vistidiagnosis'
    VisitId = Column(Integer,ForeignKey('visit.id'),primary_key=True)
    DiagId = Column(Integer,ForeignKey('diagnosisdict.id'),primary_key=True)

    Visit = relationship("Visit")
    Diag = relationship("Diagnosis")

    def __repr__(self):
        return "<VisitDiagnosis(VisitId={},DiagId={})>"\
            .format(self.VisitId,self.DiagId)

class Forms(Base):
    __tablename__= 'forms'
    id = Column(Integer,primary_key=True)
    FormName = Column(String(30))
    FormText = Column(Text)

    def __repr___(self):
        return "<Forms(FormName='{}',FormText='{}')>"\
            .format(self.FormName,self.FormText)

class VisitForms(Base):
    __tablename__= 'visitforms'
    id = Column(Integer,primary_key=True)
    VisitId = Column(Integer,ForeignKey('visit.id'))
    FormId = Column(Integer,ForeignKey('forms.id'))
    VisitFormText = Column(Text)

    Visit = relationship("Visit")
    Form = relationship("Forms")
    
    def __repr__(self):
        return "<VisitForms(VisitId={},FormId={},VisitFormText='{}')>"\
            .format(self.VisitId,self.FormId,self.VisitFormText)

class Schedule(Base):
    __tablename__= 'schedule'
    id = Column(Integer,primary_key=True)
    ScheduledDate = (Date)
    ScheduleTimeS = (Integer)
    ScheduleTimeE = (Integer)

    def __repr__(self):
        return "<Schedule(ScheduledDate={},ScheduleTimeS={},ScheduleTimeE={})>"\
            .format(self.ScheduledDate,self.ScheduleTimeS,self.ScheduleTimeE)

class ScheduleTypes(Base):
    __tablename__= 'schedulertypes'
    id = Column(Integer,primary_key=True)
    ScheduleType = Column(Integer)
    ScheduleId = Column(Integer,ForeignKey('schedule.id'))
    PhysicianId = Column(Integer,ForeignKey('employee.id'))
    RoleId = Column(Integer,ForeignKey('roles.id'))

    Physician = relationship("EmployeeModel")
    Role = relationship("Roles")
    Schedule = relationship("Schedule")

    def __repr__(self):
        return "<ScheduleTypes(ScheduleType={},PhysicianId={},RoleId={})>"\
            .format(self.ScheduleType,self.PhysicianId,self.RoleId)

class Order(Base):
    __tablename__ = 'order'
    id = Column(Integer,primary_key=True)
    ServiceId = Column(Integer)
    ScheduleId = Column(Integer,ForeignKey('schedule.id'))
    StartTime = Column(Integer)
    Duration = Column(Integer)
    PatientId = Column(Integer,ForeignKey('patient.id'))
    ScheduleWorkerID = Column(Integer,ForeignKey('employee.id'))
    ScheduleDateAdd = Column(Date)

    Schedule = relationship("Schedule")
    Patient = relationship("Patient")
    ScheduleWorker = relationship("EmployeeModel")

    def __repr__(self):
        return "<Order(ServiceId={},ScheduleId={},StartTime={},Duration={},PatientId={},ScheduleWorkerID={},ScheduleDateAdd={})>"\
            .format(self.ServiceId,self.ScheduleId,self.StartTime,self.Duration,self.PatientId,self.ScheduleWorkerID,self.ScheduleDateAdd)

class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer,primary_key=True)
    NaturalId = Column(String(16))
    FirstName = Column(String(30))
    LastName = Column(String(50))
    BirthDate = Column(Date)    
    Gender = Column(Boolean)
    Street = Column(String(50))
    City = Column(String(30))
    ZipCode = Column(String(10))

    def __repr__(self):
        return "<Patient(NaturalId='{}',FirstName='{}',LastName='{}',BirthDate={},Gender={},Street='{}',City='{}',ZipCode='{}')>"\
            .format(self.NaturalId,self.FirstName,self.LastName,self.BirthDate,self.Gender,self.Street,self.City,self.ZipCode)



