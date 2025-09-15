# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital_Management_System',
    'version' : '1.1',
    'summary': 'Doctors, Patients Records and Invoices Management',
    'sequence': 10,
    'description': """ hospital Management system for odoo 13   """,
    'category': 'Extra Tools',
    # 'website': 'https://www.odoo.com/page/billing',
    # 'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['base', 'web', 'mail'], #['base_setup', 'product', 'analytic', 'portal', 'digest'],


    'data': [
        'security/ir.model.access.csv',
        'views/doctor.xml',
        # 'views/patient.xml',
    ],
    'demo': [  #   'demo/account_demo.xml'
    ],
    'qweb': [ ],
    'installable': True, # it will show the button to install the module
    'application': True, # if we add this then this module will be added in the apps filter otherwise there will be more than 50 apps
    'auto_install': False,
}
