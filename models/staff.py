from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime


# pending Allow staff to update their profiles (with admin approval for qualifications).
# a button will be shown after updating any other role profile submit for admin
# hospital employee will be also be needed to create

# logging system in which anything which is adding or doing a log is creating like who did when did with timestamp


class HospitalStaff(models.Model):
    _name = 'hospital.staff'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Staff records details'
    _rec_name = 'name'
    _order = 'name asc'

    name = fields.Char(string='Staff Name', required=False)
    full_name = fields.Char(string='Full Name', required=False)
    phone_number = fields.Char(string='Phone Number', required=False,
                               help='Phone Number without + sign or without country code')
    email = fields.Char(string='Email Address', required=False)

    image = fields.Binary(string='Image', required=False)

    patient_ids = fields.Many2many('hospital.patient', string='Patients')
    doctor_ids = fields.Many2many('hospital.doctor', string='Doctors')
    department_id = fields.Many2one('hospital.department', string='Department')

    address = fields.Char(string='Address', required=False)
    department = fields.Char(string='Department', required=False)
    age = fields.Integer(string='Staff Age', required=False)

    birth_date = fields.Date(string='Birth Date', required=False)
    city = fields.Char(string='city', required=False)
    degree = fields.Integer(string='Staff Degree', required=False)
    degree_type = fields.Char(string='Staff related last Degree',
                              required=False)  # add a functionality later so Staff can add multiple degrees as well

    gender = fields.Selection([
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ], string='Gender', required=False)

    professional = fields.Selection([
        ('General Staff', 'General Staff'),
        ('International Staff', 'International Staff'),
        ('heart Staff', 'Heart Staff'),
        ('Eye Staff', 'Eye Staff'),
    ], string='Professional Degree', required=False)

    role = fields.Selection([
        ('nurse', 'Nurse'),
        ('receptionist', 'Receptionist'),
        ('admin', 'Admin'),
        ('lab_technician', 'Lab Technician'),
        ('pharmacist', 'Pharmacist'),
        ('security', 'Security'),
        ('cleaner', 'Cleaner'),
        ('maintenance', 'Maintenance'),
    ], string='role', required=False)

    # employement_details

    hire_date = fields.Date(string='Hire Date', required=False)
    # employee_id = fields.Many2one('hospital.employee', string='Employee', required=False)
    years_experience = fields.Integer(string='Years Experience', required=False, compute='_compute_years_experience',
                                      store=True)  # will figure out others attribute later

    contract_type = fields.Selection([
        ('part_time', 'Part Time'),
        ('full_time', 'Full Time'),
        ('internship', 'Internship'),
        ('3 months', '3 Months'),
        ('6 months', '6 Months'),
        ('12 months', '12 Months'),
    ], string='Contract Type', required=False)  # later add option to manually user can also enter

    salary = fields.Float(string='Salary', required=True, default=0.0)

    work_schedule = fields.Selection([
        ('day_shift', 'Day Shift (08:00-16:00)'),
        ('evening_shift', 'Evening Shift (16:00-00:00)'),
        ('night_shift', 'Night Shift (00:00-08:00)'),
        ('rotating', 'Rotating Shifts'),
    ], string='Work Schedule', required=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('terminated', 'Terminated'),
        ('retired', 'Retired'),
    ], string='status', default='draft', tracking=True)

    active = fields.Boolean(string='Active', default=True)

    @api.depends('hire_date')
    def _compute_years_experience(self):
        for rec in self:
            if rec.hire_date:
                rec.years_experience = date.today().year - rec.hire_date.year
            else:
                rec.years_experience = 0

    # education background will do it later

    # only one model will be added like
    # degree name
    # and user can be able to add multiple boxes like college name
    # college year
