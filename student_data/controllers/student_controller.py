from odoo import http
from odoo.http import request
import json


class StudentAPI(http.Controller):

    def _get_text_data(self):

        text = request.httprequest.data.decode("utf-8")

        data = {}

        for line in text.splitlines():

            if "=" in line:
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()

        return data

    @http.route(
        '/api/v1/student/create',
        csrf=False,
        auth="public",
        methods=['OPTIONS', 'POST']
    )
    def create_student(self, **kwargs):

        data = self._get_text_data()

        student = request.env['student.data'].sudo().create({

            'student_name': data.get('student_name'),

            'age': int(data.get('age')),

            'student_class': data.get('student_class'),

            'stream': data.get('stream')
            if data.get('student_class') == '11'
            else False,

            'phone': data.get('phone'),

            'fees_status': data.get('fees_status'),

        })

        return (
            f"Student Created Successfully\n"
            f"Student ID : {student.id}"
        )

    @http.route(
        '/api/v1/student/update',
        csrf=False,
        auth="public",
        methods=['PATCH']
    )
    def update_student(self, **kwargs):

        data = self._get_text_data()

        student = request.env['student.data'].sudo().search(
            [('student_id', '=', data.get('student_id'))],
            limit=1
        )

        if not student.exists():
            return "Student Not Found"

        values = {}

        if data.get('student_name'):
            values['student_name'] = data.get('student_name')

        if data.get('age'):
            values['age'] = int(data.get('age'))

        if data.get('student_class'):

            values['student_class'] = data.get('student_class')

            if data.get('student_class') != '11':

                values['stream'] = False

            elif data.get('stream'):

                values['stream'] = data.get('stream')

        if data.get('phone'):
            values['phone'] = data.get('phone')

        if data.get('fees_status'):
            values['fees_status'] = data.get('fees_status')

        student.write(values)

        return (
            f"Student Updated Successfully\n"
            f"Student ID : {student.id}"
        )

    @http.route(
        '/api/v1/student/all',
        csrf=False,
        auth="public",
        methods=['GET']
    )
    def get_all_students(self, **kwargs):

        students = request.env['student.data'].sudo().search([])

        data = []

        for student in students:

            data.append({

                "id": student.id,

                "student_name": student.student_name,

                "age": student.age,

                "class": student.student_class,

                "stream": student.stream,

                "phone": student.phone,

                "fees_status": student.fees_status,

                "exam_result": student.exam_result,

            })

        return json.dumps(data, indent=4)

    @http.route(
        '/api/v1/student/<int:student_id>',
        csrf=False,
        auth="public",
        methods=['GET']
    )
    def get_student(self, student_id, **kwargs):

        student = request.env['student.data'].sudo().browse(student_id)

        if not student.exists():
            return "Student Not Found"

        data = {

            "id": student.id,

            "student_name": student.student_name,

            "age": student.age,

            "class": student.student_class,

            "stream": student.stream,

            "phone": student.phone,

            "fees_status": student.fees_status,

            "exam_result": student.exam_result,

        }

        return json.dumps(data, indent=4)