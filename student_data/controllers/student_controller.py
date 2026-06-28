from odoo import http
from odoo.http import request
import json


class StudentAPI(http.Controller):

    @http.route(
        '/api/v1/create/withdraw/request',
        csrf=False,
        auth="public",
        methods=['OPTIONS', 'POST']
    )
    def create_student(self, **kwargs):

        body = request.httprequest.data.decode("utf-8")

        data = {}

        for line in body.splitlines():

            if "=" in line:
                key, value = line.split("=", 1)
                data[key.strip()] = value.strip()

        student = request.env['student.data'].sudo().create({

            'student_name': data.get('student_name'),

            'age': int(data.get('age', 0)),

            'student_class': data.get('student_class'),

            'stream': data.get('stream'),

            'phone': data.get('phone'),

            'fees_status': data.get('fees_status'),

        })

        return request.make_response(
            json.dumps({
                "status": "success",
                "id": student.id,
                "message": "Student Created Successfully"
            }),
            headers=[('Content-Type', 'application/json')]
        )