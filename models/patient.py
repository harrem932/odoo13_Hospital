import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


# later add a system in which patient or doctor or staff upload the lab reports, medication pictures, all visit history, it will be fetched data from
# it and add it to relevant fields

# Allow searching and filtering of patient history by date, doctor, or condition


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient records details'
    _rec_name = 'name'
    _order = 'name asc'

    name = fields.Char(string='Patient Name', required=True)
    full_name = fields.Char(string='Full Name', required=True)
    phone_number = fields.Char(string='Phone Number', required=True)
    emergency_contact = fields.Char(string='Emergency Contact', required=True)
    address = fields.Char(string='Address', required=True)

    patient_id = fields.Many2one('hospital.doctor', string='Assigned Doctor')  # many patients can have single doctor
    staff_ids = fields.Many2many('hospital.staff', string='Staff Assigned')  #
    department_id = fields.Many2one('hospital.department', string='Department')

    age = fields.Integer(string='Patient Age', required=True)
    city = fields.Char(string='Patient city', required=True)
    patient_history = fields.Text(string='Patient History', required=False)
    last_lab_results = fields.Text(string='Last Lab Results', required=False)
    visit_history = fields.Text(string='Visit History', required=False)
    current_symptoms = fields.Text(string='Current Symptoms')

    allergies = fields.Text(string='Known Allergies')
    medication_history = fields.Text(string='Current Medications')

    image = fields.Binary(string='Image', required=False)

    birth_date = fields.Date(string='Birth Date')

    help_needed = fields.Selection([
        ('General Patient', 'General Patient'),
        ('International Patient', 'International Patient'),
        ('heart Patient', 'Heart Patient'),
        ('Eye Patient', 'Eye Patient'),
    ], string='patient asking doctor ', required=False)

    # Gender selection field
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender', required=True)
    # Blood group selection
    blood_group = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Group')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('registered', 'Registered'),
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', tracking=True)

    admission_date = fields.Datetime(string='Admission Date')
    discharge_date = fields.Datetime(string='Discharge Date')
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Priority Level', default='medium')

    # active = fields.Boolean(string='Active', default=True)
    active = fields.Boolean(string='Active', default=True)

    email = fields.Char(string='Email Address')
    # Visit count
    # visit_count = fields.Integer(string='Visit Count', compute='_compute_visit_count', store=True)
    # Next appointment
    next_appointment = fields.Datetime(string='Next Appointment')

    #
    # def log_visit(self, note):
    #     timestamp =datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     entry = f"{timestamp} - {note}"
    #     self.visit_history = (self.visit_history or '') + \n + entry
    #
    # @api.onchange('some_field')
    # def _onchange_some_field(self):
    #     self.log_visit("Field changed by user.")
