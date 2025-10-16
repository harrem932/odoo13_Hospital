{
    'name': 'Hospital Management System',
    'version': '1.2.1',
    'summary': 'Complete Hospital Management with Doctors, Patients, and Staff',
    'sequence': 10,
    'description': """ 
    Complete Hospital Management System with:
    - Doctor Management with workflow and wizards
    - Patient Management with medical history and billing
    - Staff Management with roles and departments
    - Department Management for hospital organization
    """,
    'category': 'Healthcare',
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',  # Then load security rules
        'views/department.xml',  # Load department views first
        'views/doctor.xml',
        'views/patient.xml',
        'views/staff.xml',
        'views/menu.xml',
        'reports/hospital_reports.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
