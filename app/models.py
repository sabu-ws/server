from app import db, UserMixin
from app import bcrypt
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import text
from sqlalchemy import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

import uuid

class Users(db.Model, UserMixin):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, unique=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, server_default=text('gen_random_uuid()'))
    name = Column(String(255), nullable=True)
    firstname = Column(String(255), nullable=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    job_id = Column(Integer, db.ForeignKey("Job.id"))
    role = Column(String(64), nullable=False)
    cookie = Column(String(255), unique=True, nullable=True)
    OTPSecret = Column(String(255), unique=True, nullable=True)
    codeEP = Column(String(255), unique=True, nullable=True)
    picture = Column(String(1024), unique=True, nullable=True)
    enable = Column(Integer, nullable=True, default=1)
    firstCon = Column(Integer, default=0)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    logusb = relationship("USBlog", backref="Users")

class Job(db.Model):
    __tablename__ = "Job"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False, unique=True)
    user = relationship("Users",backref="Job")

class USBlog(db.Model):
    __tablename__ = "USBlog"
    id = Column(Integer, primary_key=True, unique=True)
    virus = Column(Integer, default=0)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, db.ForeignKey("Users.id"))
    device_id = Column(Integer, db.ForeignKey("Devices.id"))


class Devices(db.Model):
    __tablename__ = "Devices"
    id = Column(Integer, primary_key=True, unique=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, server_default=text('gen_random_uuid()'))
    ip = Column(String(64), nullable=True, unique=True)
    hostname = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)
    token = Column(String(255), nullable=False, unique=True)
    state = Column(Integer, nullable=False, default=0)
    enable = Column(Integer, nullable=True, default=1)

    log =  relationship("USBlog",backref="Devices")
    metric =  relationship("Metrics",backref="Devices")


class Metrics(db.Model):
    __tablename__ = "Metrics"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(128), unique=False, nullable=False)
    value = Column(Integer, unique=False, nullable=False)
    idDevice = Column(Integer, db.ForeignKey("Devices.id"))


# class Alerts(db.Model):
#    __tablename__ = "Alerts"
#    id = Column(Integer,primary_key=True,unique=True)
#    timestamp = Column(String(255))
#    name = Column(String(255),nullable=False)
#    description = Column(String(255),nullable=False)
#    tag = Column(String(255),nullable=False)
#    has_read = Column(Integer,nullable=False,default=0)


class Setup(db.Model):
    __tablename__ = "Setup"
    id = Column(Integer, primary_key=True, unique=True)
    action = Column(String(255), nullable=False, unique=True)
    state = Column(Boolean, default=False)