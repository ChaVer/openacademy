# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions

class Partner(models.Model):
    _inherit = 'res.partner'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    instructor = fields.Boolean("Instructor", default=False)

    session_ids = fields.Many2many('openacademy.session',
        string="Attended Sessions", readonly=True)


class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelte='set null', string='Responsible', index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    _sql_constraints = [('name_description_check','CHECK(name!=description)','Le nom d\'un cours doit être différent de sa description'),
                        ('unique_course_name','UNIQUE(name)','il ne peut pas y avoir deux cours de même nom'),]

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6,2), help="duration in days")
    seats = fields.Integer(string="number of seats")
    active = fields.Boolean(default=True)
    instructor_id = fields.Many2one('res.partner', string='instructor')
    course_id = fields.Many2one('openacademy.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats


    @api.onchange('seats', 'attendee_ids')
    def _verif_valid_seats(self):
        if self.seats<0:
            return {
                'warning' : {'title' : "nombre de sièges incorrect",
                              'message' : "nombre de sièges ne peut pas être <0",
                             }
            }
        if self.seats<len(self.attendee_ids):
            return {
                'warning': {'title': "trop de participants",
                            'message': "nombre de participants ne peut pas être > au nombre de places dispos",
                            }
            }

    @api.constrains('seats', 'attendee_ids')
    def _constraint_seats(self):
        for record in self:
            if record.seats<len(record.attendee_ids):
                raise exceptions.ValidationError("pas assez de place")


