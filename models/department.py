from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)
_logger.info("✅ hospital.department model loaded successfully")


class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Department'
    _rec_name = 'name'
    _order = 'name asc'

    name = fields.Char(string='Department Name', required=True)
    code = fields.Char(string='Department Code', required=True)
    description = fields.Text(string='Description')
    head_doctor_id = fields.Many2one('hospital.doctor', string='Head of Department')
    doctor_ids = fields.One2many('hospital.doctor', 'department_id', string='Doctors')
    staff_ids = fields.One2many('hospital.staff', 'department_id', string='Staff')
    patient_ids = fields.Many2many('hospital.patient', string='Patients')
    active = fields.Boolean(string='Active', default=True)
    capacity = fields.Integer(string='Capacity', help='Maximum number of patients the department can handle')

    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'Department code must be unique!'),
    ]

    @api.constrains('capacity')
    def _check_capacity(self):
        for rec in self:
            if rec.capacity < 0:
                raise ValidationError(_("Capacity cannot be negative."))