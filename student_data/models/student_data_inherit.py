from odoo import models, fields


class StudentDataInherit(models.Model):
    _inherit = "student.data"

    admission_date = fields.Date(
        string="Admission Date"
    )

    guardian_name = fields.Char(
        string="Guardian Name"
    )

    guardian_phone = fields.Char(
        string="Guardian Phone"
    )