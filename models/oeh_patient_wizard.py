# -*- coding: utf-8 -*-

import datetime
import pytz

from odoo import api, fields, models
from odoo.exceptions import ValidationError

TYPE_DOC_EQUIVALENCE = {'01': 'DNI', '03': 'CARNETEXT', '06': 'PASAPORTE'}
SEX_EQUIVALENT = {'1': 'Hombre', '2': 'Mujer'}
ACTIVO = 'ACTIVO'

SEX = [
    ('1', 'Masculino'),
    ('2', 'Femenino'),
]

class WizardPatient(models.Model):
    """docstring for WizardPatient"""

    _name = 'wizard.patient'
    _description = 'WizardPatient description'

    q = fields.Char()
    line_ids = fields.One2many(comodel_name='wizard.patient.line', inverse_name='line_id', string='Patient')

    def search_patients(self):
        self.line_ids.unlink()

        if not self.q:
            self.line_ids = []
        else:
            patients = self.env['oeh.medical.patient'].search([('identification_id', 'ilike', self.q)])
            list_patients = []

            if patients:
                patients.validate_sis()
                for patient in patients:
                    list_patients.append([0, False, {
                        'patient_id': patient.id,
                        'type_number': patient.type_number,
                        'identification_id': patient.identification_id,
                        'full_name': u'{} {} {}'.format(
                            patient.first_name or patient.name, patient.last_name or "",
                            patient.last_name_2 or ""),
                        'age': patient.age,
                        'sex': patient.sex,
                        'sis_state': patient.sis_estado,
                        }])
                self.line_ids = list_patients
            else:
                if len(self.q) == 8 and self.q.isdigit():
                    response = self.env["consultadatos.mpi"].ver(self.q, '01')
                    if "errors" in response:
                        msg = len(res['errors']) and res['errors'][0].get('detail', 'Error Desconocido')
                        raise ValidationError(msg)
                    sis_state = 'NO TIENE'
                    sis_filiation = 'NO TIENE'
                    sis_filiation_expiration_date = False
                    if response.get('tipo_seguro') == '2':
                        datos_sis = self.env['consultadatos.mpi'].ver_datos_sis(self.q, '01')
                        sis_filiation = datos_sis.get('contrato')
                        sis_filiation_expiration_date = datos_sis.get('fecha_caducidad')
                        sis_state = datos_sis.get('estado')

                    data = {
                        'patient_id': False,
                        'doc_type': TYPE_DOC_EQUIVALENCE.get(
                            response.get('tipo_documento')),
                        'identification_id': response.get('numero_documento'),
                        'full_name': u'{} {} {}'.format(
                            response.get('nombres'), response.get('apellido_paterno'),
                            response.get('apellido_materno'), ''),
                        'age': response.get('edad_str', ''),
                        'sex': response.get('sexo', ''),
                        'sis_state': sis_state,
                        'sis_filiation': sis_filiation,
                        'sis_filiation_expiration_date': sis_filiation_expiration_date}
                    self.line_ids = [[0, False, data]]


class WizardPatientLine(models.TransientModel):
    """docstring for WizardPatientLine"""

    _name = 'wizard.patient.line'
    _description = 'WizardPatientLine description'

    line_id = fields.Many2one('wizard.patient')
    patient_id = fields.Many2one('oeh.medical.patient', 'Paciente')
    doc_type = fields.Char('Tipo de documento')
    identification_id = fields.Char(u'Número de documento')
    full_name = fields.Char('Nombres y apellidos')
    age = fields.Char('Edad')
    sex = fields.Selection(SEX, 'Sexo')
    sis_filiation = fields.Char(u'Filiación SIS')
    sis_filiation_expiration_date = fields.Date('Válido hasta')
    sis_state = fields.Char('Estado del SIS')

    @api.multi
    def new_patient(self):
        self.ensure_one()

        sis_active = False
        if self.sis_state == ACTIVO:
            sis_active = True
        return {
            'name': u"Crear paciente",
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'oeh.medical.patient',
            'target': 'self',
            'view_id': self.env.ref('oehealth_samu.oeh_medical_patient_view_form').id,
            'context': {
                'default_doc_type': self.doc_type,
                'default_identification_id': self.identification_id,
                'default_sis_filiation': self.sis_filiation,
                'default_sis_filiation_expiration_date': self.sis_filiation_expiration_date,
                'default_sis_active': sis_active,
                'default_name': self.full_name,
            },
        }
