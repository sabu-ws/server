from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import InputRequired, Length, ValidationError, Regexp, IPAddress, Email, AnyOf
# from app.utils import getHostname, getNetInfo

class LoginForm(FlaskForm):
    username = StringField(validators=[Length(min=4, max=20)])
    password = PasswordField(validators=[Length(min=12, max=255),Regexp(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*\.!@$%^\&\(\)\{\}\[\]:;<>,\.\?\/~_\+-=\|]).{12,255}$",message=u"The password not match with padding") ])
    submit = SubmitField()

class AddUserForm(FlaskForm):
    firstname = StringField(validators=[Length(min=3, max=255,message="First Name fields must be between 3 and 255 characters long"),Regexp(r"^[a-zA-Z0-9-]{3,255}$",message=u"The firstname not match with padding")])
    name = StringField(validators=[Length(min=3, max=255,message="Last Name fields must be between 3 and 255 characters long"),Regexp(r"^[a-zA-Z0-9-]{3,255}$",message=u"The name not match with padding")])
    username = StringField(validators=[Length(min=3, max=255,message="Username fields must be between 3 and 255 characters long"),Regexp(r"^[a-zA-Z0-9-.]{3,255}$",message=u"The username not match with padding")])
    role = StringField(validators=[AnyOf(['Admin','User'],message="Role is not correct"),Regexp(r"^[a-zA-Z0-9-._\s]{3,255}$",message=u"The role not match with padding")])
    email = EmailField(validators=[Email(),Length(min=3, max=255,message="Email fields must be between 3 and 255 characters long")])
    job = StringField(validators=[Length(min=3, max=255,message="Job fields must be between 3 and 255 characters long"),Regexp(r"^[a-zA-Z0-9-._\s]{3,255}$",message=u"The job not match with padding")])
    password = PasswordField(validators=[Length(min=12, max=255,message="Password fields must be between 12 and 255 characters long"),Regexp(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*\.!@$%^\&\(\)\{\}\[\]:;<>,\.\?\/~_\+-=\|]).{12,255}$",message="The password not match with padding")])

# class GlobalSettingsForm(FlaskForm):
#     hostname = StringField(validators=[Length(min=3, max=20),Regexp(r"^[a-zA-Z0-9-]{3,20}$",message=u"The hostname not match with padding")], render_kw={"placeholder":getHostname(),"class":"w-full border border-gray-300 dark:bg-gray-600 dark:border-gray-600 dark:focus:outline-none dark:focus:ring-2 dark:focus:ring-white dark:focus:border-transparent dark:text-white rounded px-3 py-2"})
#     password = PasswordField(validators=[Length(min=12, max=255),Regexp(r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[\*\.!@$%^\&\(\)\{\}\[\]:;<>,\.\?\/~_\+-=\|]).{12,255}$",message=u"The password not match with padding") ],id="passwordInput", render_kw={"placeholder": "Your password","class":"w-full border border-gray-300 dark:bg-gray-600 dark:border-gray-600 dark:focus:outline-none dark:focus:ring-2 dark:focus:ring-white dark:focus:border-transparent dark:text-white rounded px-3 py-2"})
#     submit = SubmitField(render_kw={"value":"Submit","class":"bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"})

# class NetworkSettingsForm(FlaskForm):
#     interface = StringField(validators=[InputRequired()],render_kw={"placeholder":getNetInfo("interface"),"class":"w-full border border-gray-300 dark:bg-gray-600 dark:border-gray-600 dark:focus:outline-none dark:focus:ring-2 dark:focus:ring-white dark:focus:border-transparent dark:text-white rounded px-3 py-2"})
#     ipaddr = StringField(validators=[InputRequired(),IPAddress(message="Bad ip address")],render_kw={"placeholder":getNetInfo("ip"),"class":"w-full border border-gray-300 dark:bg-gray-600 dark:border-gray-600 dark:focus:outline-none dark:focus:ring-2 dark:focus:ring-white dark:focus:border-transparent dark:text-white rounded px-3 py-2"})
#     netmask = StringField(validators=[InputRequired(),IPAddress(message="Bad netmask address")],render_kw={"placeholder":getNetInfo("netmask"),"class":"w-full border border-gray-300 dark:bg-gray-600 dark:border-gray-600 dark:focus:outline-none dark:focus:ring-2 dark:focus:ring-white dark:focus:border-transparent dark:text-white rounded px-3 py-2"})
#     gateway = StringField(validators=[InputRequired(),IPAddress(message="Bad gateway address")],render_kw={"placeholder":getNetInfo("gateway"),"class":"w-full border border-gray-300 dark:bg-gray-600 dark:border-gray-600 dark:focus:outline-none dark:focus:ring-2 dark:focus:ring-white dark:focus:border-transparent dark:text-white rounded px-3 py-2"})
#     dns1 = StringField(validators=[InputRequired(),IPAddress(message="Bad dns1 address")],render_kw={"placeholder":getNetInfo("dns1"),"class":"w-full border border-gray-300 dark:bg-gray-600 dark:border-gray-600 dark:focus:outline-none dark:focus:ring-2 dark:focus:ring-white dark:focus:border-transparent dark:text-white rounded px-3 py-2"})
#     dns2 = StringField(validators=[IPAddress(message="Bad dns2 address")],render_kw={"placeholder":getNetInfo("dns2"),"class":"w-full border border-gray-300 dark:bg-gray-600 dark:border-gray-600 dark:focus:outline-none dark:focus:ring-2 dark:focus:ring-white dark:focus:border-transparent dark:text-white rounded px-3 py-2"})
#     submit = SubmitField(render_kw={"value":"Submit","class":"bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"})