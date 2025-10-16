from odoo import models, fields, api, _  # through _ we get translater to convert our return or errors output
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
# we can combine other above two lines just making it seperate for now
from datetime import date, datetime


# later will be added help text and some more attributes to enchance the user form submission

class HospitalDoctor(models.Model):  # models.Model is our base class
    _name = 'hospital.doctor'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # inheritance concept is implemented
    _description = 'Hospital_Management_System'  # info that is display in techincal info
    _rec_name = 'name'  # will learn about this in detail as of now it will be uses as record name
    _order = 'age asc'  # will show the order on the basis of any field or smallest or largest

    # in each new record the name will be shown of that specific record got it now
    # https://www.youtube.com/watch?v=hUdcQxaNMs4&list=PLZJajKUSxekaeUYlUzQ0BTasskyzDezHZ

    # basic information
    name = fields.Char(string='Doctor Name', required=False)
    full_name = fields.Char(string='Full Name', required=False, help='Enter Doctor Complete Name')

    # Relations m2m allow multiple records to be linked with eo
    patient_ids = fields.Many2many('hospital.patient', string='Patients')
    staff_ids = fields.Many2many('hospital.staff', string='Staff Assistant')
    department_id = fields.Many2one('hospital.department', string='Department')

    # in many2one only we select 1 record out of multiple records, same like hiring process
    # in many2many we can selct multiple records and add in xml widget_tags to show more good

    # Integer fields for storing with validation
    age = fields.Integer(string='Doctor Age', required=False)
    email = fields.Char(string='Email', required=False)

    city = fields.Char(string='Doctor City', required=False)
    country = fields.Char(string='Doctor Country', required=False)
    address = fields.Char(string='Address', required=False)
    degree = fields.Char(string='Doctor Degree in numbers', required=False)
    degree_type = fields.Char(string='Doctor related last Degree',
                              required=False)  # add a functionality later so doctor can add multiple degrees aswell

    notes = fields.Text(string='Notes', required=False)
    image = fields.Binary(string='Image', required=False)
    phone_number = fields.Char(string='Phone Number', required=False)  # before it was INT
    allow_to_edit = fields.Boolean(string='Allow To Edit', default=False, required=False)
    license_number = fields.Char(string='License  Number', required=False)
    issuing_date = fields.Date(string='Issuing Date', required=False)
    is_specialist = fields.Boolean(string='Is Specialist', default=False)

    # New fields for advanced features
    is_consultant = fields.Boolean(string='Is Consultant', default=False)
    consultation_fee = fields.Float(string='Consultation Fee', digits=(10, 2))

    # after _order = 'age asc'
    _sql_constraints = [
        ('unique_license', 'UNIQUE(license_number)', 'License number must be unique!'),
        ('check_salary_positive', 'CHECK(salary >= 0)', 'Salary must be positive!'),
    ]

    birth_date = fields.Date(string='Birth Date')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')

    hire_date = fields.Date(string='Hire Date')
    emergency_contact = fields.Char(string='Emergency Contact')
    rating = fields.Selection([
        ('0', 'No Rating'),
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Rating')

    specialty = fields.Selection([
        ('General Doctor', 'General Doctor'),
        ('International Doctor', 'International Doctor'),
        ('heart Doctor', 'Heart Doctor'),
        ('Eye Doctor', 'Eye Doctor'),
        ('Cardiologist', 'Cardiologist'),
        ('Neurologist', 'Neurologist'),
        ('Orthopedic', 'Orthopedic'),
        ('Pediatrician', 'Pediatrician'),
        ('Dermatologist', 'Dermatologist'),
    ], string='Professional Degree', required=False)

    issuing_authority = fields.Selection([
        ('Punjab', 'Punjab'),
        ('Sindh', 'Sindh'),
        ('KPK', 'KPK'),
        ('Balochistan', 'Balochistan'),
        ('International', 'International'),
    ], string='Issuing Authority', required=False)  # add in this to enter manually later option

    work_schedule = fields.Selection([
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ], string='Working Schedule', required=False)

    time_availability = fields.Selection([
        ('morning', '09:00 AM - 12:20 PM'),
        ('afternoon', '12:20 PM - 06:00 PM'),
        ('evening', '06:00 PM - 11:50 PM'),
        ('night', '01:10 AM - 12:00 AM'),
    ], string='Time Availability', required=False)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')

    digital_signature = fields.Binary(string='Digital Signature', required=False)

    salary = fields.Float(string='Salary', required=False,
                          readonly=True)  # will add more conditions to allow edit rights later on
    department = fields.Char(string='Department', required=False)
    years_experience = fields.Integer(string='Years of Experience', compute='_compute_years_experience')

    active = fields.Boolean(string='Active', default=True)  # for soft deletion concept

    patient_count = fields.Integer(
        string='Patients',
        compute='_compute_patient_count',
        store=True
    )

    @api.depends('hire_date')
    def _compute_years_experience(self):
        for rec in self:
            if rec.hire_date:
                rec.years_experience = date.today().year - rec.hire_date.year
            else:
                rec.years_experience = 0

    @api.depends('patient_ids')
    def _compute_patient_count(self):
        for rec in self:
            rec.patient_count = len(rec.patient_ids)

    # purpose of this method is to limit on the phone number to enter not less than correct digits
    def check_len_phone_number(self):
        for rec in self:
            if rec.phone_number and len(str(rec.phone_number)) < 10:
                raise ValueError('Phone Number must have 10 digits')

    # underscore adds a funcationality to translate the text in the user language if the system is international
    # rec means the record
    #     @api.multi in older versions this id depreceated if using in odoo 12 then can added in it.

    def action_approve(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_("Only draft appointments can be approved."))
            rec.write({'state': 'approved'})

    def action_cancel(self):
        for rec in self:
            if rec.state in ['done', 'cancelled']:
                raise UserError(_("Cannot cancel done or already cancelled appointments."))
            rec.write({'state': 'cancelled'})

    def action_in_progress(self):
        for rec in self:
            if rec.state != 'approved':
                raise UserError(_("Only approved doctors can be moved to In Progress."))
            rec.write({'state': 'in_progress'})
        return True
    

    def action_done(self):
        if self.state != 'in_progress':
            raise UserError("Only in progress records can be marked as done")
        self.write({'state': 'done'})

    @api.onchange('phone_number')
    def check_phone_number(self):
        if self.phone_number and len(str(self.phone_number)) < 10:
            return {
                'warning': {
                    'title': 'Invalid Phone Number',
                    'message': 'Please enter a valid phone number.',
                }
            }

    @api.constrains('age')
    def check_age(self):
        if self.age < 18:
            raise UserError(_("Age must be at least 18"))
        if self.age >= 100:
            raise UserError(_("Age is unrelistic 100"))

    @api.onchange('specialty')
    def check_specialty(self):
        specialty_department_map = {
            'Cardiologist': 'Cardiology',
            'Neurologist': 'Neurology',
            'Orthopedic': 'Orthopedics',
            'Pediatrician': 'Pediatrics',
            'heart Doctor': 'Cardiology',
            'Eye Doctor': 'Ophthalmology',
        }
        if self.specialty in specialty_department_map:
            self.department = specialty_department_map[self.specialty]

    # Search Domain code

    def print_doctor_table(self):
        searches = [
            [('age', '=', 30)],  # Equality
            [('state', '!=', 'draft')],  # Inequality
            [('age', '>', 30)],  # Greater than
            [('age', '>=', 30)],  # Greater than or equal
            [('age', '<', 30)],  # Less than
            [('age', '<=', 30)],  # Less than or equal
            [('name', 'like', 'John')],  # Like
            [('name', 'not like', 'John')],  # Not like
            [('name', 'ilike', 'john')],  # Case-insensitive like
            [('name', 'not ilike', 'john')],  # Not case-insensitive like
            [('name', '=like', 'John%')],  # Equals like
            [('name', '=ilike', 'john%')],  # Equals case-insensitive like
            [('name', 'in', ['John Doe', 'Jane Smith'])],  # In
            [('name', 'not in', ['John Doe', 'Jane Smith'])],  # Not in
            [('age', '=?', False)],  # Equals with null check
            #########below need to understand in detail later
            ['&', ('age', '>', 30), ('gender', '=', 'male')],  # AND
            ['|', ('name', 'ilike', 'john'), ('name', 'ilike', 'jane')],  # OR
            ['!', ('state', '=', 'draft')]  # NOT
        ]
        for domain in searches:
            records = self.env['hospital.doctor'].search(domain)
            print(f"\nDomain: {domain}")
            print(f"Total Records: {len(records)}")
            for rec in records:
                print(
                    f"ID: {rec.id}, Name: {rec.name}, Age: {rec.age}, Gender: {rec.gender}, Doctor: {rec.doctor_id.name or 'None'}")

    def name_get(self):
        """Custom name display with specialty"""
        result = []
        for record in self:
            name = f"Dr. {record.name}"
            if record.specialty:
                name += f" ({record.specialty})"
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """Enhanced search - search by name, license, or specialty"""
        if args is None:
            args = []

        domain = []
        if name:
            domain = ['|', '|',
                      ('name', operator, name),
                      ('license_number', operator, name),
                      ('specialty', operator, name)]

        records = self.search(domain + args, limit=limit)
        return records.name_get()

    # Model Constrains

    @api.constrains('consultation_fee', 'is_consultant')
    def _check_consultation_fee(self):
        """Validate consultation fee for consultants"""
        for record in self:
            if record.is_consultant and record.consultation_fee <= 0:
                raise ValidationError(_("Consultants must have a positive consultation fee."))

    def unlink(self):
        """Soft delete for active doctors, hard delete for drafts"""
        for record in self:
            if record.state in ['approved', 'in_progress']:
                # Soft delete
                record.write({'active': False, 'state': 'cancelled'})
                return True
        # Hard delete for draft records
        return super(HospitalDoctor, self).unlink()

    @api.onchange('is_consultant', 'specialty')
    def _onchange_consultation_fee(self):
        """Auto-set consultation fee based on specialty"""
        if self.is_consultant and self.specialty:
            fee_mapping = {
                'Cardiologist': 500.0,
                'Neurologist': 600.0,
                'Orthopedic': 400.0,
                'General Doctor': 200.0,
                'Pediatrician': 300.0,
            }
            self.consultation_fee = fee_mapping.get(self.specialty, 250.0)
