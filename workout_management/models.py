from datetime import datetime

import bcrypt
from flask import current_app as app
from sqlalchemy.orm import relationship

from workout_management.db import db_context as db
from workout_management.helpers import MailTextHelper
from workout_management.services import SendGrindService

user_plan_association_table = db.Table('plans_users', db.Model.metadata,
                                       db.Column('plan_id', db.Integer, db.ForeignKey('plans.id')),
                                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
                                       )


class User(db.Model):
    __tablename__ = 'users'

    def __init__(self, **dict):
        """Create instance."""
        db.Model.__init__(self, **dict)
        if "password" in dict.keys():
            self.set_password(dict["password"].rstrip())

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    plans = relationship("Plan", back_populates="users", secondary=user_plan_association_table)

    @property
    def full_name(self):
        """Full user_bluprint name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(12))

    def check_password(self, value):
        """Check password."""
        return bcrypt.checkpw(value.encode("utf-8"), self.password)

    def __repr__(self):
        return f"<User #{self.id}: {self.full_name} - {self.email}>"


class Plan(db.Model):
    __tablename__ = 'plans'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    users = relationship("User", back_populates="plans", secondary=user_plan_association_table)
    days = relationship("Day", back_populates="plan")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def associated_user_count(self):
        return len(self.users)

    def notify_users(self):
        for user in self.users:
            SendGrindService(app.config["SENDGRID_API_KEY"]).send(user.email,
                                                                  f"Your plan {self.name} has changed.",
                                                                  MailTextHelper.get_plan_changed_template(self))

    def notify_association(self, user):
        SendGrindService(app.config["SENDGRID_API_KEY"]).send(user.email,
                                                              "New Workout Plan",
                                                              MailTextHelper.get_associated_template(user,
                                                                                                     self))


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey("days.id"))
    day = relationship("Day", back_populates="exercises")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)

    @classmethod
    def new_from_dict(cls, exercise_data):
        return Exercise(name=exercise_data["name"], sets=exercise_data["sets"], reps=exercise_data["reps"])


class Day(db.Model):
    __tablename__ = 'days'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.id"))
    plan = relationship("Plan", back_populates="days")
    exercises = relationship("Exercise", back_populates="day")

    @classmethod
    def new_from_dict(cls, day_data):
        day = Day(number=day_data["number"])

        if "exercises" in day_data:
            for exercise_data in day_data["exercises"]:
                day.exercises.append(Exercise.new_from_dict(exercise_data))

        return day
