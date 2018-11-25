# -*- coding: utf-8 -*-
from odoo import api, fields, models


class WizardSamuEmergency(models.TransientModel):
    '''
    Registro de pacientes de emergencias
    '''
    _name = 'wizard.samu.emergency'
    _inherit = 'wizard.appointment'
    _description = 'Emergency wizard'

    line_ids = fields.One2many(
        'wizard.samu.emergency.line', 'wizard_emergency_id')
    line_2_ids = fields.One2many(
        'wizard.samu.emergency.line2', 'wizard_emergency_id')


class WizardSamuEmergencyLine(models.TransientModel):
    '''
    Detalle de pacientes de emergencias
    '''
    _name = 'wizard.samu.emergency.line'
    _inherit = 'wizard.appointment.line'
    _rec_name = 'wizard_emergency_id'

    wizard_emergency_id = fields.Many2one('wizard.samu.emergency')

    @api.multi
    def request_emergency(self):
        self.ensure_one()
        return {
            'name': u"Solicitar emergencia",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'self',
            'res_model': 'oeh.medical.emergency',
            'context': {
                'default_patient_id': self.patient_id.id,
            },
        }


class WizardSamuEmergencyLine2(models.TransientModel):
    _name = 'wizard.samu.emergency.line2'
    _inherit = 'wizard.appointment.line2'
    _rec_name = 'wizard_emergency_id'

    wizard_emergency_id = fields.Many2one('wizard.samu.emergency')


class OehMedicalPatient(models.Model):
    _inherit = 'oeh.medical.patient'

    @api.multi
    def request_emergency(self):
        self.ensure_one()
        return {
            'name': u'Solicitar emergencia',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'self',
            'res_model': 'oeh.medical.emergency',
            'context': {
                'default_patient_id': self.id,
            },
        }
