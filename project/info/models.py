# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy
from . import db


class AccountPas(db.Model):
    __tablename__ = 'account_pass'

    zid = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    account = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)


class Activity(db.Model):
    __tablename__ = 'activity'

    hdid = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer, nullable=False)
    tid = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False)
    a_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    is_delete = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())


class Comm(db.Model):
    __tablename__ = 'comm'

    hid = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer, nullable=False)
    tid = db.Column(db.Integer, nullable=False)
    time = db.Column(db.BigInteger, nullable=False)
    content = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(50), nullable=False)


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    major_field = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.String(255), nullable=False)


class Leader(db.Model):
    __tablename__ = 'leader'

    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    zid = db.Column(db.Integer, nullable=False)


class Student(db.Model):
    __tablename__ = 'student'

    sid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    zid = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    tid = db.Column(db.Integer, nullable=False)


class Teacher(db.Model):
    __tablename__ = 'teacher'

    tid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    introduction = db.Column(db.String(255), nullable=False)
    major = db.Column(db.String(255), nullable=False)
    group_id = db.Column(db.Integer, nullable=False)
    zid = db.Column(db.Integer, nullable=False)
