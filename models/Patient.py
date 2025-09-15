from odoo import fields, models

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient records details'

    name = fields.Char(string='Patient Name', required=True)
    age = fields.Integer(string='Patient Age', required=True)
    city = fields.Char(string='Patient city', required=True)
    # degree = fields.Integer(string='Patient Degree', required=True)
    # degree_type = fields.Char(string='Patient related last Degree', required=True) # add a functionality later so Patient can add multiple degrees aswell
    help_needed = fields.Selection([
        ('General Patient', 'General Patient'),
        ('International Patient', 'International Patient'),
        ('heart Patient', 'Heart Patient'),
        ('Eye Patient', 'Eye Patient'),
    ], string='patient asking doctor ', required=True)