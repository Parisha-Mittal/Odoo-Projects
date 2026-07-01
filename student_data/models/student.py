from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random


class StudentData(models.Model):
    _name = 'student.data'
    _description = 'Student Information'
    _rec_name = 'student_name'

    student_id = fields.Char(
        string="Student ID",
        readonly=True,
        copy=False,
        default="New"
    )
    user_id = fields.Many2one(
        'student.user',
        string="Created By",
        readonly=True
    )

    student_name = fields.Char(
        string="Student Name",
        required=True
    )

    age = fields.Integer(
        string="Age",
        required=True
    )

    student_class = fields.Selection(
        [
            ('1', 'Class 1'),
            ('2', 'Class 2'),
            ('3', 'Class 3'),
            ('4', 'Class 4'),
            ('5', 'Class 5'),
            ('6', 'Class 6'),
            ('7', 'Class 7'),
            ('8', 'Class 8'),
            ('9', 'Class 9'),
            ('10', 'Class 10'),
            ('11', 'Class 11'),
            ('12', 'Class 12'),
        ],
        string="Class",
        required=True
    )

    stream = fields.Selection(
        [
            ('science', 'Science'),
            ('commerce', 'Commerce'),
            ('arts', 'Arts'),
        ],
        string="Stream"
    )

    phone = fields.Char(
        string="Phone Number",
        required=True
    )

    fees_status = fields.Selection(
        [
            ('paid', 'Paid'),
            ('unpaid', 'Unpaid'),
        ],
        string="Fees Status",
        default='unpaid',
        required=True
    )

    exam_result = fields.Char(
        string="Exam Result",
        compute="_compute_exam_result",
        store=True,
        readonly=False
    )

    grade_color = fields.Char(
        compute="_compute_grade_color"
    )

    fee_color = fields.Char(
        compute="_compute_fee_color"
    )

    history_count = fields.Integer(
        compute="_compute_history_count"
    )

    def action_update_fees(self):

        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "name": "Update Fees",
            "res_model": "update.fees.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "active_id": self.id
            }
        }

    def _compute_history_count(self):
        for rec in self:
            rec.history_count = self.env["student.history"].search_count(
                [
                    ("student_id", "=", rec.id)
                ]
    )

    def action_view_history(self):
        self.ensure_one()
        context = dict(self.env.context)
        domain = [
            ("student_id", "=", self.id)
        ]
        return smart_button_action(
            domain,
            context,
            "Student History"
        )

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:

            if not vals.get("student_id") or vals.get("student_id") == "New":

                last_student = self.search(
                    [('student_id', '!=', False)],
                    order='student_id desc',
                    limit=1
                )

                if last_student:

                    last_number = int(last_student.student_id.replace("SD", ""))
                    vals["student_id"] = f"SD{last_number + 1:03d}"

                else:
                    vals["student_id"] = "SD001"

        students = super().create(vals_list)

        for student in students:
            self.env["student.history"].create({
                "student_id": student.id,
                "action": "created",
                "remarks": "Student record created",
            })

        return students

    def write(self, vals):

        result = super().write(vals)

        for rec in self:
            self.env["student.history"].create({
                "student_id": rec.id,
                "action": "updated",
                "remarks": "Student details updated",
            })

        return result

    @api.depends('fees_status')
    def _compute_exam_result(self):

        grades = [
            'A+',
            'A',
            'B+',
            'B',
            'C+',
            'C',
            'D',
            'E',
            'Fail'
        ]

        for rec in self:

            if rec.fees_status == 'paid':
                rec.exam_result = random.choice(grades)
            else:
                rec.exam_result = "Fees not paid. Result not generated."

    @api.onchange('fees_status')
    def _onchange_fees_status(self):

        grades = [
            'A+',
            'A',
            'B+',
            'B',
            'C+',
            'C',
            'D',
            'E',
            'Fail'
        ]

        if self.fees_status == 'paid':
            self.exam_result = random.choice(grades)
        else:
            self.exam_result = "Fees not paid. Result not generated."

    @api.depends('exam_result')
    def _compute_grade_color(self):

        for rec in self:

            if rec.exam_result in ['A+', 'A']:
                rec.grade_color = 'excellent'
            elif rec.exam_result in ['B+', 'B']:
                rec.grade_color = 'good'
            elif rec.exam_result in ['C+', 'C']:
                rec.grade_color = 'average'
            elif rec.exam_result in ['D', 'E']:
                rec.grade_color = 'poor'
            elif rec.exam_result == 'Fail':
                rec.grade_color = 'fail'
            else:
                rec.grade_color = 'none'

    @api.depends('fees_status')
    def _compute_fee_color(self):

        for rec in self:
            if rec.fees_status == 'paid':
                rec.fee_color = 'paid'
            else:
                rec.fee_color = 'unpaid'

    @api.onchange('student_class')
    def _onchange_student_class(self):

        if self.student_class != '11':
            self.stream = False

    @api.constrains('phone')
    def _check_phone(self):

        for rec in self:

            if not rec.phone:
                continue

            if not rec.phone.isdigit():
                raise ValidationError(
                    "Phone number should contain only digits."
                )

            if len(rec.phone) != 10:
                raise ValidationError(
                    "Phone number must contain exactly 10 digits."
                )

    @api.constrains('age')
    def _check_age(self):

        for rec in self:

            if rec.age < 3 or rec.age > 25:
                raise ValidationError(
                    "Age should be between 3 and 25."
                )

def smart_button_action(domain, context, name):

    context.update(
        create=False,
        edit=False,
        delete=False
    )

    return {
        "name": name,
        "type": "ir.actions.act_window",
        "res_model": "student.history",
        "view_mode": "list,form",
        "domain": domain,
        "context": context,
    }