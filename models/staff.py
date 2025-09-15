# from odoo import fields, models
#
# class HospitalStaff(models.Model):
#     _name = 'hospital.staff'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = 'Staff records details'
#     #
#     # name = fields.Char(string='Patient Name', required=True)
#     # age = fields.Integer(string='Patient Age', required=True)
#     # city = fields.Char(string='Patient Profession', required=True)
#     # degree = fields.Integer(string='Patient Degree', required=True)
#     # degree_type = fields.char(string='Patient related last Degree', required=True) # add a functionality later so Patient can add multiple degrees aswell
#     # professional = fields.selection([
#     #     ('General Patient', 'General Patient'),
#     #     ('International Patient', 'International Patient'),
#     #     ('heart Patient', 'Heart Patient'),
#     #     ('Eye Patient', 'Eye Patient'),
#     # ], string='Professional Degree', required=True)