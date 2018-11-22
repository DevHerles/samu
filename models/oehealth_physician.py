##############################################################################
#    Copyright (C) 2017 oeHealth (<http://oehealth.in>). All Rights Reserved
#    oeHealth, Hospital Management Solutions
##############################################################################

import datetime
from datetime import timedelta
import logging
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

class OeHealthPhysician(models.Model):
    _name = "oeh.medical.physician"
    _description = "Information about the doctor"
    _inherits={
        'hr.employee': 'employee_id',
    }

    CONSULTATION_TYPE = [
        ('Residential', 'Residential'),
        ('Visiting', 'Visiting'),
        ('Other', 'Other'),
    ]

    @api.multi
    def _app_count(self):
        oe_apps = self.env['oeh.medical.appointment']
        for pa in self:
            domain = [('doctor', '=', pa.id)]
            app_ids = oe_apps.search(domain)
            apps = oe_apps.browse(app_ids)
            app_count = 0
            for ap in apps:
                app_count+=1
            pa.app_count = app_count
        return True

    @api.multi
    def _prescription_count(self):
        oe_pres = self.env['oeh.medical.prescription']
        for pa in self:
            domain = [('doctor', '=', pa.id)]
            pres_ids = oe_pres.search(domain)
            pres = oe_pres.browse(pres_ids)
            pres_count = 0
            for pr in pres:
                pres_count+=1
            pa.prescription_count = pres_count
        return True

    employee_id = fields.Many2one('hr.employee', string='Related Employee', required=True, ondelete='cascade', help='Employee-related data of the physician')
    institution = fields.Many2one('oeh.medical.health.center', string='Institution', help="Institution where doctor works")
    code = fields.Char(string='Licence ID', size=128, help="Physician's License ID")
    speciality = fields.Many2one('oeh.medical.speciality', string='Speciality', help="Speciality Code")
    consultancy_type = fields.Selection(CONSULTATION_TYPE, string='Consultancy Type', help="Type of Doctor's Consultancy", default=lambda *a: 'Residential')
    consultancy_price = fields.Integer(string='Consultancy Charge', help="Physician's Consultancy price")
    available_lines = fields.One2many('oeh.medical.physician.line', 'physician_id', string='Physician Availability')
    degree_id = fields.Many2many('oeh.medical.degrees', id1='physician_id', id2='degree_id', string='Degrees')
    app_count = fields.Integer(compute=_app_count, string="Appointments")
    prescription_count = fields.Integer(compute=_prescription_count, string="Prescriptions")
    is_pharmacist = fields.Boolean(string='Pharmacist?', default=lambda *a: False)
    oeh_user_id = fields.Many2one('res.users', string='Responsible Odoo User')

    _sql_constraints = [
        ('code_oeh_physician_userid_uniq', 'unique(oeh_user_id)', "Selected 'Responsible' user is already assigned to another physician !")
    ]

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}

    @api.onchange('address_id')
    def _onchange_address(self):
        self.work_phone = self.address_id.phone
        self.mobile_phone = self.address_id.mobile

    @api.onchange('company_id')
    def _onchange_company(self):
        address = self.company_id.partner_id.address_get(['default'])
        self.address_id = address['default'] if address else False

    @api.onchange('user_id')
    def _onchange_user(self):
        self.work_email = self.user_id.email
        self.name = self.user_id.name
        self.image = self.user_id.image

    @api.multi
    def write(self, vals):
        if 'name' in vals:
           vals['name_related'] = vals['name']
        return super(OeHealthPhysician, self).write(vals)


class OeHealthPhysicianLine(models.Model):
    # Array containing different days name
    PHY_DAY = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    _name = "oeh.medical.physician.line"
    _description = "Information about doctor availability"

    name = fields.Selection(PHY_DAY, string='Available Day(s)', required=True)
    start_time = fields.Float(string='Start Time (24h format)')
    end_time = fields.Float(string='End Time (24h format)')
    physician_id = fields.Many2one('oeh.medical.physician', string='Physician', index=True, ondelete='cascade')
