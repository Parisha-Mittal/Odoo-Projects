from odoo import models, fields


class StudentHistory(models.Model):
    _name = "student.history"
    _description = "Student History"

    student_id = fields.Many2one(
        "student.data",
        string="Student",
        required=True,
        ondelete="cascade"
    )

    action = fields.Selection(
        [
            ("created", "Created"),
            ("updated", "Updated"),
            ("deleted", "Deleted")
        ],
        string="Action",
        required=True
    )

    remarks = fields.Char(
        string="Remarks"
    )

    date = fields.Datetime(
        string="Date",
        default=fields.Datetime.now
    )