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

        data = json.loads(request.httprequest.data)

        student = request.env['student.data'].sudo().create({
            'student_name': data.get('student_name'),
            'age': data.get('age'),
            'student_class': data.get('student_class'),
            'stream': data.get('stream'),
            'phone': data.get('phone'),
            'fees_status': data.get('fees_status'),
        })

        return json.dumps({
            "status": "success",
            "id": student.id,
            "message": "Student Created Successfully"
        })