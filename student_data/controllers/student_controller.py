from odoo import http
from odoo.http import request
import json
import re

EMAIL_REGEX = re.compile(
    r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
)

def _get_text_data():

    text = request.httprequest.data.decode("utf-8")

    if not text:
        return {}

    return json.loads(text)

class StudentAPI(http.Controller):

    @http.route(
        '/api/v1/student/signup',
        csrf=False,
        auth='public',
        methods=['POST', 'OPTIONS']
    )
    def signup(self, **kwargs):

        try:
            data = _get_text_data()
            required_keys = [
                "name",
                "email",
                "password",
                "mobile"
            ]
            for key in required_keys:
                if not data.get(key):
                    return json.dumps({
                        "status": False,
                        "message": f"{key} is required"
                    })
            if not re.match(EMAIL_REGEX, data.get("email")):
                return json.dumps({
                    "status": False,
                    "message": "Invalid Email"
                })
            existing_user = request.env['student.user'].sudo().search(
                [('email', '=', data.get('email'))],
                limit=1
            )
            if existing_user:
                return json.dumps({
                    "status": False,
                    "message": "User already exists"
                })
            otp = str(__import__("random").randint(100000, 999999))
            user = request.env['student.user'].sudo().create({
                "name": data.get("name"),
                "email": data.get("email"),
                "password": data.get("password"),
                "mobile": data.get("mobile"),
                "signup_otp": otp,
            })
            return json.dumps({
                "status": True,
                "message": "Signup Successful",
                "otp": otp
            })
        except Exception as e:
            return json.dumps({
                "status": False,
                "message": str(e)
            })

    @http.route(
        '/api/v1/student/verify-otp',
        csrf=False,
        auth="public",
        methods=['POST', 'OPTIONS']
    )
    def verify_otp(self, **kwargs):

        data = _get_text_data()

        user = request.env['student.user'].sudo().search([
            ('email', '=', data.get('email'))
        ], limit=1)

        if not user:
            return json.dumps({
                "status": False,
                "message": "User not found"
            })

        if user.signup_otp != data.get("otp"):
            return json.dumps({
                "status": False,
                "message": "Invalid OTP"
            })

        user.write({
            "otp_verified": True,
            "signup_otp": False
        })

        return json.dumps({
            "status": True,
            "message": "OTP Verified Successfully"
        })

    @http.route(
        '/api/v1/student/login',
        csrf=False,
        auth="public",
        methods=['POST', 'OPTIONS']
    )
    def login(self, **kwargs):

        data = _get_text_data()

        user = request.env['student.user'].sudo().search([
            ('email', '=', data.get('email')),
            ('password', '=', data.get('password'))
        ], limit=1)

        if not user:
            return json.dumps({
                "status": False,
                "message": "Invalid Email or Password"
            })

        if not user.otp_verified:
            return json.dumps({
                "status": False,
                "message": "Please verify your OTP first"
            })

        return json.dumps({
            "status": True,
            "message": "Login Successful",
            "user_id": user.id,
            "name": user.name
        })

    @http.route(
        '/api/v1/student/create',
        csrf=False,
        auth="public",
        methods=['OPTIONS', 'POST']
    )
    def create_student(self, **kwargs):

        data = _get_text_data()
        user = request.env['student.user'].sudo().search([
            ('email', '=', data.get('email'))
        ], limit=1)

        if not user:
            return json.dumps({
                "status": False,
                "message": "Please Signup First"
            })

        if not user.otp_verified:
            return json.dumps({
                "status": False,
                "message": "Please Verify OTP"
            })

        student = request.env['student.data'].sudo().create({
            'student_name': data.get('student_name'),
            'age': int(data.get('age')),
            'student_class': data.get('student_class'),
            'stream': data.get('stream') if data.get('student_class') == '11' else False,
            'phone': data.get('phone'),
            'fees_status': data.get('fees_status'),
            'user_id': user.id,
        })

        return json.dumps({
            "status": "success",
            "message": "Student Created Successfully",
            "student_id": student.student_id
        })

    @http.route(
        '/api/v1/student/update',
        csrf=False,
        auth="public",
        methods=['PATCH', 'OPTIONS']
    )
    def update_student(self, **kwargs):

        data = _get_text_data()

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
        print(values)
        student.write(values)

        return json.dumps({
            "status": "success",
            "message": "Student Updated Successfully",
            "student_id": student.student_id
        })

    @http.route(
        '/api/v1/student/all',
        csrf=False,
        auth="public",
        methods=['GET', 'OPTIONS']
    )
    def get_all_students(self, **kwargs):

        students = request.env['student.data'].sudo().search([])

        data = []

        for student in students:

            data.append({

                "student_id": student.student_id,

                "student_name": student.student_name,

                "age": student.age,

                "student_class": student.student_class,

                "stream": student.stream or "",

                "phone": student.phone,

                "fees_status": student.fees_status,

                "exam_result": student.exam_result,

            })

        return json.dumps(data)

    @http.route(
        '/api/v1/student/<string:student_id>',
        csrf=False,
        auth="public",
        methods=['GET', 'OPTIONS']
    )
    def get_student(self, student_id, **kwargs):

        student = request.env['student.data'].sudo().search(
            [('student_id', '=', student_id)],
            limit=1
        )

        if not student.exists():
            return "Student Not Found"

        data = {

            "student_id": student.student_id,

            "student_name": student.student_name,

            "age": student.age,

            "student_class": student.student_class,

            "stream": student.stream or "",

            "phone": student.phone,

            "fees_status": student.fees_status,

            "exam_result": student.exam_result,

        }

        return json.dumps(data)

    @http.route(
        '/api/v1/student/delete',
        csrf=False,
        auth="public",
        methods=['DELETE', 'OPTIONS']
    )
    def delete_student(self, **kwargs):

        data = _get_text_data()

        student = request.env['student.data'].sudo().search(
            [('student_id', '=', data.get('student_id'))],
            limit=1
        )

        if not student.exists():
            return "Student Not Found"

        student.unlink()

        data = {
            "status": "success",
            "message": "Student Deleted Successfully",
            "student_id": student.student_id
        }

        return json.dumps(data)