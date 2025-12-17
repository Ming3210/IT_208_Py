

# student_management/models/student.py
from odoo import models, fields


class Student(models.Model):
    _name = 'student.student'
    _description = 'Student'
    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    email = fields.Char(string='Email')
    is_active = fields.Boolean(string='Active', default=True)