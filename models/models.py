# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelte='set null', string='Responsible', index=True)

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6,2), help="duration in days")
    seats = fields.Integer(string="number of seats")
    instructor_id = fields.Many2one('res.partner', string='instructor')
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)

