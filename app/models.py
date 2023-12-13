from app import db, UserMixin
from app import bcrypt
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Column
from sqlalchemy import Boolean
from sqlalchemy import text
from sqlalchemy import Text
from sqlalchemy import UUID
from sqlalchemy import Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

# from sqlalchemy.sql import expression
# from sqlalchemy.ext.compiler import compiles
# from sqlalchemy.types import DateTime

import uuid
import datetime

# class utcnow(expression.FunctionElement):
#     type = DateTime()
#     inherit_cache = True

# @compiles(utcnow, 'postgresql')
# def pg_utcnow(element, compiler, **kw):
#     return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, unique=True)
    uuid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String(255), nullable=True)
    firstname = Column(String(255), nullable=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    job_id = Column(Integer, db.ForeignKey("job.id"))
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

    logforusb = relationship("USBlog", backref="users")


class Job(db.Model):
    __tablename__ = "job"
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False, unique=True)

    user = relationship("Users", backref="job")


class USBlog(db.Model):
    __tablename__ = "usblog"
    id = Column(Integer, primary_key=True, unique=True)
    virus = Column(Integer, default=0)
    date = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, db.ForeignKey("users.id"))
    device_id = Column(Integer, db.ForeignKey("devices.id"))


class Devices(db.Model):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, unique=True)
    uuid = Column(
        UUID(as_uuid=True),
        unique=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )
    ip = Column(String(64), nullable=True, unique=True)
    hostname = Column(String(255), nullable=True)
    description = Column(String(1024), nullable=True)
    token = Column(String(255), nullable=False, unique=True)
    state = Column(Integer, nullable=False, default=0)
    enable = Column(Integer, nullable=True, default=1)

    log = relationship("USBlog", backref="devices")
    metric = relationship("Metrics", backref="devices")


class Metrics(db.Model):
    __tablename__ = "metrics"
    name = Column(Text(), unique=False, nullable=False)
    value = Column(Integer, unique=False, nullable=False)
    timestamp_ht = Column(
        DateTime(timezone=True),
        nullable=False,
        primary_key=True,
        default=datetime.datetime.now,
    )
    idDevice = Column(Integer, db.ForeignKey("devices.id"))


# class Alerts(db.Model):
#    __tablename__ = "Alerts"
#    id = Column(Integer,primary_key=True,unique=True)
#    timestamp = Column(String(255))
#    name = Column(String(255),nullable=False)
#    description = Column(String(255),nullable=False)
#    tag = Column(String(255),nullable=False)
#    has_read = Column(Integer,nullable=False,default=0)


class Setup(db.Model):
    __tablename__ = "setup"
    id = Column(Integer, primary_key=True, unique=True)
    action = Column(String(255), nullable=False, unique=True)
    state = Column(Boolean, default=False)
