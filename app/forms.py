from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import (
    Length,
    Regexp,
    IPAddress,
    Email,
    AnyOf,
    optional,
)  # noqa: E501


class LoginForm(FlaskForm):
    username = StringField(validators=[Length(min=4, max=20)])
    password = PasswordField(
        validators=[
            Length(min=12, max=255),
            Regexp(
                r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*\.!@$%^\&\(\)\{\}\[\]:;<>,\.\?\/~_\+-=\|]).{12,255}$",
                message="The password not match with padding",
            ),
        ]
    )  # noqa: E501


class AddUserForm(FlaskForm):
    firstname = StringField(
        validators=[
            Length(
                min=3,
                max=255,
                message="First Name fields must be between 3 and 255 characters long",
            ),
            Regexp(
                r"^[a-zA-Z0-9-]{3,255}$", message="The firstname not match with padding"
            ),
        ]
    )  # noqa: E501
    name = StringField(
        validators=[
            Length(
                min=3,
                max=255,
                message="Last Name fields must be between 3 and 255 characters long",
            ),
            Regexp(r"^[a-zA-Z0-9-]{3,255}$", message="The name not match with padding"),
        ]
    )  # noqa: E501
    username = StringField(
        validators=[
            Length(
                min=3,
                max=255,
                message="Username fields must be between 3 and 255 characters long",
            ),
            Regexp(
                r"^[a-z0-9-.]{3,255}$", message="The username not match with padding"
            ),
        ]
    )  # noqa: E501
    role = StringField(
        validators=[
            AnyOf(["Admin", "User"], message="Role is not correct"),
            Regexp(
                r"^[a-zA-Z0-9-._\s]{3,255}$", message="The role not match with padding"
            ),
        ]
    )  # noqa: E501
    email = EmailField(
        validators=[
            # Email(),
            Regexp(r'^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$', message="The name not match with padding"),
            Length(
                min=3,
                max=255,
                message="Email fields must be between 3 and 255 characters long",
            ),
        ]
    )  # noqa: E501
    job = StringField(
        validators=[
            Length(
                min=3,
                max=255,
                message="Job fields must be between 3 and 255 characters long",
            ),
            Regexp(
                r"^[a-zA-Z0-9-._\s]{3,255}$", message="The job not match with padding"
            ),
        ]
    )  # noqa: E501
    password = PasswordField(
        validators=[
            Length(
                min=12,
                max=255,
                message="Password fields must be between 12 and 255 characters long",
            ),
            Regexp(
                r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*\.!@$%^\&\(\)\{\}\[\]:;<>,\.\?\/~_\+-=\|]).{12,255}$",
                message="The password not match with padding",
            ),
        ]
    )  # noqa: E501


class ModifyIpForm(FlaskForm):
    interface = StringField()
    ip = StringField(validators=[IPAddress(message="Bad IP address")])
    netmask = StringField(validators=[IPAddress(message="Bad Netmask address")])
    gateway = StringField(validators=[IPAddress(message="Bad Gateway address")])
    dns1 = StringField(validators=[IPAddress(message="Bad DNS 1 address")])
    dns2 = StringField(validators=[optional(), IPAddress(message="Bad DNS 2 address")])
