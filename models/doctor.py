from odoo import models, fields

class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital_Management_System'

    name = fields.Char(string='Doctor Name', required=True)
    age = fields.Integer(string='Doctor Age', required=True)
    city = fields.Char(string='Doctor City', required=True)
    degree = fields.Integer(string='Doctor Degree in numbers', required=True)
    degree_type = fields.Char(string='Doctor related last Degree', required=True) # add a functionality later so doctor can add multiple degrees aswell
    specialty = fields.Selection([
        ('General Doctor', 'General Doctor'),
        ('International Doctor', 'International Doctor'),
        ('heart Doctor', 'Heart Doctor'),
        ('Eye Doctor', 'Eye Doctor'),
    ], string='Professional Degree', required=True)
    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Image')