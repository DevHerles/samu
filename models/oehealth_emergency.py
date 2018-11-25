# -*- coding: utf-8 -*-
from odoo import api, fields, models


class OehMedicalPatient(models.Model):
    _inherit = 'oeh.medical.patient'

    @api.multi
    def request_samu_emergency(self):
        self.ensure_one()
        return {
            'name': u"Solicitar emergencia",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': self.env.ref('oehealth_samu.oeh_medical_samu_emergency_view_form_inherit_medical_emergency').id,
            'target': 'self',
            'res_model': 'oeh.medical.samu.emergency',
            'context': {
                'default_patient_id': self.id,
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

class OehealthSamuEmergency(models.Model):
    '''
    Registro de pacientes de emergencias
    '''
    _name = 'oeh.medical.samu.emergency'
    _inherit = 'oeh.medical.emergency'

    physician = fields.Char(u'Médico')
    physician_id = fields.Many2one('oeh.medical.physician', 'Médico', required=True)
    nurse_id = fields.Many2one('oeh.medical.physician', 'Enfermera', required=True)
    driver_id = fields.Many2one('hr.employee', 'Conductor', required=True)
    unitytype_id = fields.Many2one('oehealth.samu.unitytype', 'Tipo de unidad', required=True)
    elapsed_time = fields.Integer('Tiempo transcurrido (minutos)')
    observations = fields.Text('Observaciones')
    # mobileunit_ids = fields.One2many('oehealth.samu.mobileunit', 'mobileunit_id', 'Unidades')
    line_ids = fields.One2many('oeh.medical.samu.emergency.line', 'line_id', 'Unidades')


class OehealthSamuEmergencyLine(models.Model):
    _name = 'oeh.medical.samu.emergency.line'

    mobileunit_id = fields.Many2one('oehealth.samu.mobileunit', 'Unidad')
    line_id = fields.Many2one('oeh.medical.samu.emergency', 'Unidad')

    @api.multi
    def goto_mobileunity(self):
        self.ensure_one()
        return {
            'name': u'Ver unidad',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'self',
            'res_model': 'oehealth.samu.mobileunit',
            'view_id': self.env.ref('oehealth_samu.oehealth_samu_unidadesmoviles_view_form').id,
            'context': {
                'default_id': self.mobileunit_id.id,
            },
        }


class WizardEmergency(models.TransientModel):
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


class WizardEmergencyLine(models.TransientModel):
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
            'res_model': 'oeh.medical.samu.emergency',
            'context': {
                'default_patient_id': self.patient_id.id,
            },
        }


class WizardEmergencyLine2(models.TransientModel):
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
