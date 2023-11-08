from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Regexp, IPAddress, Email, AnyOf  # noqa: E501


class LoginForm(FlaskForm):
    username = StringField(validators=[Length(min=4, max=20)])
    password = PasswordField(validators=[Length(min=12, max=255), Regexp(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*\.!@$%^\&\(\)\{\}\[\]:;<>,\.\?\/~_\+-=\|]).{12,255}$", message=u"The password not match with padding")])  # noqa: E501


class AddUserForm(FlaskForm):
    firstname = StringField(validators=[Length(min=3, max=255, message="First Name fields must be between 3 and 255 characters long"), Regexp(r"^[a-zA-Z0-9-]{3,255}$", message=u"The firstname not match with padding")])  # noqa: E501
    name = StringField(validators=[Length(min=3, max=255, message="Last Name fields must be between 3 and 255 characters long"), Regexp(r"^[a-zA-Z0-9-]{3,255}$", message=u"The name not match with padding")])  # noqa: E501
    username = StringField(validators=[Length(min=3, max=255, message="Username fields must be between 3 and 255 characters long"), Regexp(r"^[a-zA-Z0-9-.]{3,255}$", message=u"The username not match with padding")])  # noqa: E501
    role = StringField(validators=[AnyOf(['Admin', 'User'], message="Role is not correct"), Regexp(r"^[a-zA-Z0-9-._\s]{3,255}$", message=u"The role not match with padding")])  # noqa: E501
    email = EmailField(validators=[Email(), Length(min=3, max=255, message="Email fields must be between 3 and 255 characters long")])  # noqa: E501
    job = StringField(validators=[Length(min=3, max=255, message="Job fields must be between 3 and 255 characters long"), Regexp(r"^[a-zA-Z0-9-._\s]{3,255}$", message=u"The job not match with padding")])  # noqa: E501
    password = PasswordField(validators=[Length(min=12, max=255, message="Password fields must be between 12 and 255 characters long"), Regexp(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*\.!@$%^\&\(\)\{\}\[\]:;<>,\.\?\/~_\+-=\|]).{12,255}$", message="The password not match with padding")])  # noqa: E501
