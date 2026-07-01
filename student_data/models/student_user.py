from odoo import models, fields
import random


class StudentUser(models.Model):
    _name = "student.user"
    _description = "Student User"

    name = fields.Char(
        string="Name",
        required=True
    )

    email = fields.Char(
        string="Email",
        required=True
    )

    password = fields.Char(
        string="Password",
        required=True
    )

    mobile = fields.Char(
        string="Mobile Number",
        required=True
    )

    signup_otp = fields.Char(
        string="Signup OTP",
        readonly=True
    )

    otp_verified = fields.Boolean(
        string="OTP Verified",
        default=False
    )

    active = fields.Boolean(
        default=True
    )

    def generate_otp(self):
        self.signup_otp = str(random.randint(100000, 999999))