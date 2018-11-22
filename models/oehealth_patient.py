# -*- coding: utf-8 -*-

import datetime
from datetime import timedelta
import logging
import pytz
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

DOC_TYPE_SELECTION_DNI = '01'
DOC_TYPE_SELECTION_PASSPORT = '02'

DOC_TYPE_SELECTION = [
    (DOC_TYPE_SELECTION_DNI, 'DNI'),
    (DOC_TYPE_SELECTION_PASSPORT, 'PASAPORTE'),
]

FLAG_STRING_NOTIENESEGURO = "NO TIENE SEGURO"

TYPE_DOC_NOSECONOCE = 'NOSECONOCE'
TYPE_DOC_DNI = 'DNI'
TYPE_DOC_LIBRETAMILITAR = 'LIBRETAMILITAR'
TYPE_DOC_CARNETEXT = 'CARNETEXT'
TYPE_DOC_ACTANACIMIENTO = 'ACTANACIMIENTO'
TYPE_DOC_PASAPORTE = 'PASAPORTE'
TYPE_DOC_DOCEXTRANJERO = 'DOCEXTRANJERO'
TYPE_DOC_NOTIENE = 'NOTIENE'
TYPE_DOC_SINDOCUMENTO = 'TYPE_DOC_SINDOCUMENTO'

TYPE_DOCUMENTO = [
    (TYPE_DOC_NOSECONOCE, 'NO SE CONOCE'),
    (TYPE_DOC_DNI, 'DNI'),
    (TYPE_DOC_LIBRETAMILITAR, 'LIBRETA MILITAR'),
    (TYPE_DOC_CARNETEXT, 'CARNET EXTRANJERIA'),
    (TYPE_DOC_ACTANACIMIENTO, 'ACTA DE NACIMIENTO'),
    (TYPE_DOC_PASAPORTE, 'PASAPORTE'),
    (TYPE_DOC_DOCEXTRANJERO, 'DOCUMENTO DE IDENTIFICACION DEL EXTRANJERO'),
    (TYPE_DOC_NOTIENE, 'NO TIENE'),
    (TYPE_DOC_SINDOCUMENTO, 'SIN DOCUMENTO')
]

class ResPartner(models.Model):
    """docstring for ResPartner"""

    _inherit = 'res.partner'

    doc_type = fields.Selection(TYPE_DOCUMENTO, string="Tipo Documento", default=TYPE_DOC_DNI)
    sis_filiation = fields.Char(u'Filiación SIS')
    sis_filiation_expiration_date = fields.Date('Válido hasta')
    sis_state = fields.Char('Estado del SIS')
    first_name = fields.Char('First name')
    last_name = fields.Char('Last name')
    last_name_2 = fields.Char('Last name')
    current_address = fields.Char(u'Dirección actual')
    current_reference = fields.Char('Referencia actual')
    current_address_location = fields.Char(u'Direción actual')
    a_country_id = fields.Many2one('res.country.state', u'País')
    a_state_id = fields.Many2one('res.country.state', 'Departamento')
    a_province_id = fields.Many2one('res.country.state', 'Provincia')
    a_district_id = fields.Many2one('res.country.state', 'Distrito')

    entity_country_id = fields.Many2one('res.country.state', u'País')
    entity_department_id = fields.Many2one('res.country.state', 'Departamento')
    entity_province_id = fields.Many2one('res.country.state', 'Provincia')
    entity_district_id = fields.Many2one('res.country.state', 'Distrito')
    entity_address = fields.Char('Dirección')

    def get_datos_sis(self):
        if not (self.doc_type in (TYPE_DOC_DNI, TYPE_DOC_DNI.lower()) and
                self.identification_id and len(self.identification_id) == 8):
            return {}
        t = self.identification_id, self.get_mpi_document_type(self.doc_type)
        return self.env['consultadatos.mpi'].ver_datos_sis(*t)

    @property
    def sis_ok(self):
        """
        Verifica si la persona tiene el sis activo
        ret: True or False
        """

        sis_filiation_expiration_date = self.sis_filiation_expiration_date and \
            fields.Datetime.from_string(self.sis_filiation_expiration_date)
        now = fields.Datetime.from_string(fields.Datetime.now())

        sis_ok = self.sis_filiation and self.sis_filiation != FLAG_STRING_NOTIENESEGURO and \
            (sis_filiation_expiration_date and sis_filiation_expiration_date >= now or not sis_filiation_expiration_date)

        return sis_ok

    def get_mpi_document_type(self, doc_type):
        if doc_type == TYPE_DOC_DNI:
            return '01'
        elif doc_type == TYPE_DOC_LIBRETAMILITAR:
            return '02'
        elif doc_type == TYPE_DOC_CARNETEXT:
            return '03'
        elif doc_type == TYPE_DOC_ACTANACIMIENTO:
            return '04'
        elif doc_type == TYPE_DOC_PASAPORTE:
            return '06'
        elif doc_type == TYPE_DOC_DOCEXTRANJERO:
            return '07'
        elif doc_type == TYPE_DOC_SINDOCUMENTO:
            return '00'
        else:
            raise ValidationError(u'El tipo de documento {} no es válido'.format(doc_type))

class OeHealthPatient(models.Model):
    _name='oeh.medical.patient'
    _inherits={
        'res.partner': 'partner_id',
    }

    MARITAL_STATUS = [
        ('single', 'Soltero'),
        ('married', 'Casado'),
        ('widowed', 'Viudo'),
        ('divorced', 'Divorciado'),
        ('separated', 'Separado'),
    ]

    SEX = [
        ('male', 'Masculino'),
        ('female', 'Femenino'),
    ]

    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True, ondelete='cascade', help='Partner-related data of the patient')
    # doctor = fields.Many2one('oeh.medical.physician', string='Family Physician', help="Current primary care physician / family doctor", domain=[('is_pharmacist','=',False)])
    dob = fields.Date(string='Date of Birth')
    age = fields.Char(compute= '_patient_age', size=32, string='Patient Age', help="It shows the age of the patient in years(y), months(m) and days(d).\nIf the patient has died, the age shown is the age at time of death, the age corresponding to the date on the death certificate. It will show also \"deceased\" on the field")
    sex = fields.Selection(SEX, string='Sex', index=True)
    marital_status = fields.Selection(MARITAL_STATUS, string='Marital Status')
    # ethnic_group = fields.Many2one('oeh.medical.ethnicity','Ethnic group')
    oeh_patient_user_id = fields.Many2one('res.users', string='Responsible Odoo User')
    identification_id = fields.Char(u'Número de documento')
    doc_type = fields.Char('Tipo de documento')

    _sql_constraints = [
        ('code_oeh_patient_userid_uniq', 'unique (oeh_patient_user_id)', "Selected 'Responsible' user is already assigned to another patient !")
    ]

    @api.multi
    def onchange_state(self, state_id):
        if state_id:
            state = self.env['res.country.state'].browse(state_id)
            return {'value': {'country_id': state.country_id.id}}
        return {}

    @api.onchange('identification_id', 'doc_type')
    def onchange_identification_id(self):
        __import__('ipdb').set_trace()
        if self.doc_type and self.doc_type == TYPE_DOC_NOTIENE:
            return {
                'value': {'identification_id': '/'}
            }
        elif self.doc_type and self.doc_type == '01' and self.identification_id:
            if len(self.identification_id) != 8 or not self.identification_id.isdigit():
                return {
                    'warning': {
                        'title': 'Error en el DNI',
                        'message': 'El DNI debe tener 8 números',
                    },
                }

            values = {}
            code = self.identification_id
            data = self.env['consultadatos.mpi'].ver(self.identification_id, '01')
            if "error" in data:
                raise ValidationError(data['error'])

            pb_distrito_id = self.env['res.country.state']
            if data.get("nacimiento_ubigeo", False):
                domain = [
                    ('country_id', '=', self.country_id.id),
                    ('code_reniec', '=', data.get('nacimiento_ubigeo', 'no_ubigeo'))
                ]
                pb_distrito_id = self.env['res.country.state'].search(domain, limit=1)
            distrito_id = self.env['res.country.state'].search([
                ('country_id', '=', self.country_id.id),
                ('code_reniec', '=', data.get(
                    "get_distrito_domicilio_ubigeo_reniec", 'no_ubigeo'))])

            values = {
                'name': '%s %s %s' % (data.get('nombres', ''),
                                      data.get('apellido_paterno', ''),
                                      data.get('apellido_materno', '')),
                'first_name': data.get('nombres', False),
                'last_name': data.get('apellido_paterno', False),
                'last_name_2': data.get('apellido_materno', False),
                'sex': data.get('sexo', False),
                'ethnicity': data.get('etnia_descripcion', False),
                'mobile': data.get('celular', False),
                'street': data.get('domicilio_direccion', False),
                'dob': data.get('fecha_nacimiento', False),
                'zip': data.get('get_distrito_domicilio_ubigeo_reniec', False),
                'website': False,
                'is_reniec': True,
                'clinical_history_number': code,
                'identification_code': code,
                # Datos de nacimiento
                'state_id': pb_distrito_id.state_id.id or False,
                'province_id': pb_distrito_id.province_id.id or False,
                'district_id': pb_distrito_id.id or False,
                'marital_status': data.get("estado_civil", False),
                # Datos de domicilio RENIEC
                'entity_department_id': distrito_id.state_id.id or False,
                'entity_province_id': distrito_id.province_id.id or False,
                'entity_district_id': distrito_id.id or False,
                'entity_address': data.get("domicilio_direccion", False),
                # Datos de domicilio Actual
                'a_state_id': distrito_id.state_id.id or False,
                'a_province_id': distrito_id.province_id.id or False,
                'a_district_id': distrito_id.id or False,
                'current_address': data.get("domicilio_direccion", False),
                'current_reference': data.get("domicilio_direccion", False),
                # Datos de Fallecimiento
                'deceased': not data.get("es_persona_viva", False),
                'image': data.get("foto", False),
            }

            # sis
            t = self.identification_id, self.parent_id.get_mpi_document_type(self.doc_type)

            try:
                datos_sis = self.env['consultadatos.mpi'].ver_datos_sis(*t)
            except Exception:
                raise ValidationError(u'Error al consultar datos del SIS.')

            # if datos_sis:
                # domain = [('codigo_eess', '=', datos_sis.get('codigo_eess', False))]
                # eess = self.env['renaes.eess'].search(domain, limit=1)
                # eess_nombre = eess and eess.name
                # eess_direccion = eess and eess.direccion

                # vals = dict(
                    # sis_nro_contrato=datos_sis.get("contrato", ""),
                    # sis_fecha_afiliacion=datos_sis.get("fecha_afiliacion", ""),
                    # sis_fecha_caducidad=datos_sis.get("fecha_caducidad", ""),
                    # sis_eess_codigo=datos_sis.get("codigo_eess", ""),
                    # sis_eess_nombre=eess_nombre,
                    # sis_eess_direccion=eess_direccion,
                    # sis_tipo_seguro_descripcion=datos_sis.get("tipo_seguro_descripcion", ""),
                    # sis_estado=datos_sis.get("estado", FLAG_STRING_NOTIENESEGURO),
                    # sis_activo=True if datos_sis.get("estado") == ACTIVO else False,
                    # sis_last_update=fields.Datetime.now(),
                # )
                # values.update(vals)

            # if datos_sis.get("contrato", False):
                # values.update({'sis_filiation': datos_sis.get("contrato", False),
                               # 'sis_filiation_expiration_date': datos_sis.get("fecha_caducidad", False)})
            # return {'value': values}

    @api.onchange('first_name', 'last_name', 'last_name_2')
    def _onchange_last_name(self):
        full_name = (self.first_name and (self.first_name + ' ') or '') + \
            (self.last_name and (self.last_name + ' ') or '') + \
            (self.last_name_2 and (self.last_name_2 + ' ') or '')
        self.name = full_name

    @api.multi
    def update_sis(self, datos_sis):
        for record in self:
            if record.sis_activo:
                record.seguro_id.write({
                    'name': 'SIS',
                    'ins_no': datos_sis.get('contrato', False),
                    'start_date': datos_sis.get('fecha_afiliacion', False),
                    'patient': record.id,
                    'regime': 1,
                    'exp_date': datos_sis.get('fecha_caducidad'),
                    'ins_type': 1,
                    'state': 'Active',
                })

    @api.multi
    def validate_sis(self):
        for record in self:
            last_update = record.sis_last_update and fields.Datetime.from_string(record.sis_last_update)

            if not last_update or last_update and last_update + timedelta(minutes=1) < datetime.datetime.now():
                datos_sis = record.get_datos_sis()
                if datos_sis:
                    sis_estado = datos_sis.get('estado', False)
                    if sis_estado == ACTIVO:
                        sis_activo = True
                        sis_estado = 'Active'
                    else:
                        sis_activo = False
                        sis_estado = ''

                    for seguro in record.seguro_id:
                        if seguro.ins_no == record.sis_filiation:
                            seguro.unlink()

                    domain = [('partner_id', '!=', False), ('partner_id', '=', record.id)]
                    patient = self.env['oeh.medical.patient'].search(domain, limit=1)

                    sis_info = {'name': 'SIS',
                                'ins_no': datos_sis.get('contrato', ''),
                                'start_date': datos_sis.get('fecha_afiliacion', False),
                                'partner_id': record.id,
                                'patient': patient.id,
                                'regime': 1,
                                'exp_date': datos_sis.get('fecha_caducidad', False),
                                'ins_type': 1,
                                'state': sis_estado,
                                }

                    domain = [('codigo_eess', '=', datos_sis.get('codigo_eess', False))]
                    eess = self.env['renaes.eess'].search(domain, limit=1)

                    vals = dict(
                        sis_nro_contrato=datos_sis.get('contrato', FLAG_STRING_NOTIENESEGURO),
                        sis_fecha_afiliacion=datos_sis.get('fecha_afiliacion', False),
                        sis_fecha_caducidad=datos_sis.get('fecha_caducidad', False),
                        sis_eess_codigo=datos_sis.get('codigo_eess', False),
                        sis_eess_nombre=eess and eess.name,
                        sis_eess_direccion=eess and eess.direccion,
                        sis_tipo_seguro_descripcion=datos_sis.get('tipo_seguro_descripcion', False),
                        sis_estado=datos_sis.get('estado', FLAG_STRING_NOTIENESEGURO),
                        sis_activo=sis_activo,
                        sis_last_update=fields.Datetime.now(),
                        seguro_id=[[0, False, sis_info]] and []  # Se omite el valor de seguro_id
                    )

                    if datos_sis.get('contrato'):
                        vals.update(
                            {
                                'sis_filiation': datos_sis.get('contrato', False),
                                'sis_filiation_expiration_date': datos_sis.get('fecha_caducidad', False)
                            })

                else:
                    vals = dict(
                        sis_nro_contrato=False,
                        sis_fecha_afiliacion=False,
                        sis_fecha_caducidad=False,
                        sis_eess_codigo=False,
                        sis_eess_nombre=False,
                        sis_eess_direccion=False,
                        sis_tipo_seguro_descripcion=False,
                        sis_estado=False,
                        sis_activo=False,
                        sis_last_update=False,
                        seguro_id=[]
                    )
                record.write(vals)

    def get_datos_sis(self):
        return self.partner_id.get_datos_sis()

    @api.model
    def _create_from_mpi_document_number(self, doc_type, identification_id):

        if doc_type and identification_id:
            data = self.env["consultadatos.mpi"].ver(identification_id, '01')
            if "error" in data:
                raise ValidationError(data['error'])

            pb_distrito_id = self.env['res.country.state']
            country_id = self.env.ref('base.pe').id
            if data.get("nacimiento_ubigeo", False):
                domain = [
                    ('country_id', '=', country_id),
                    ('code_reniec', '=', data.get('nacimiento_ubigeo', 'no_ubigeo'))
                ]
                pb_distrito_id = self.env['res.country.state'].search(domain, limit=1)

            partner_values = {
                'name': '{} {} {}'.format(
                    data.get('nombres', ''),
                    data.get('apellido_paterno', ''),
                    data.get('apellido_materno', '')),
                'display_name': '[{}] {} {} {}'.format(
                    identification_id, data.get('nombres', ''),
                    data.get('apellido_paterno', ''),
                    data.get('apellido_materno', '')),
                'last_name': data.get('apellido_materno', ''),
                'last_name_2': data.get('apellido_materno', ''),
                'first_name': data.get('nombres', ''),
                'identification_id': identification_id,
                'clinical_history_number': identification_id,
                'doc_type': TYPE_DOC_DNI,
                'company_id': self.env.user.partner_id.company_id.id,
                'street': data.get('domicilio_direccion', False),
                'zip': data.get('get_distrito_domicilio_ubigeo_reniec', False),
                'employee': False,
                'is_company': False,
                'lang': 'es_PE',
                'customer': True,
                'is_doctor': False,
                'is_institution': False,
                'is_person': False,
                'is_patient': True,
                'ubigeo': data.get('get_distrito_domicilio_ubigeo_reniec', False),
                'country_id': country_id,
                'state_id': pb_distrito_id.state_id.id or False,
                'province_id': pb_distrito_id.province_id.id or False,
                'district_id': pb_distrito_id.id or False,
                'entity_country_id': country_id,
                'entity_address': data.get('domicilio_direccion', False),
                'entity_department_id': pb_distrito_id.state_id.id or False,
                'entity_province_id': pb_distrito_id.province_id.id or False,
                'entity_district_id': pb_distrito_id.id or False,
                'current_address': data.get('domicilio_direccion', False),
                'image': data.get('foto', False),
                'email': '',
                'is_reniec': True
            }

            person = self.env['res.partner'].create(partner_values)
            patient = self.env['oeh.medical.patient'].create({
                'partner_id': person.id,
                'sex': data.get('sexo', False),
                'dob': data.get("fecha_nacimiento", False),
            })
            return patient

    @api.model
    def create(self, vals):
        if 'first_name' in vals and 'last_name' in vals and 'last_name_2' in vals:
            t_name = (vals['last_name'] or '', vals['last_name_2'] or '', vals['first_name'] or '')
            vals.update({'name': u' '.join(t_name)})

        # Secuencia Paciente sin documento
        if vals.get('doc_type') == TYPE_DOC_NOTIENE:
            sequence = self.env['ir.sequence'].next_by_code('oeh.medical.patient.sindocumento')
            vals.update(dict(identification_id=sequence))

        if not vals.get('identification_code'):
            sequence = self.env['ir.sequence'].next_by_code('oeh.medical.patient')
            patient_class = OehMedicalPatient
        else:
            if not vals.get('identification_code').isdigit():
                raise ValidationError(u'El número del archivo clínico debe contener solamente dígitos.')
            if int(vals.get('identification_code')) <= 0:
                raise ValidationError(u'EL número del archivo clínico debe ser mayor a cero (0).')
            sequence_obj = self.env.ref('oehealth.seq_oeh_medical_patient')
            vals['identification_code'] = vals.get('identification_code').zfill(sequence_obj.padding)
            if len(vals.get('identification_code')) > sequence_obj.padding:
                raise ValidationError(u'El número del archivo clínico puede contener como máximo {} dígitos.'.format(
                    sequence_obj.padding))
            sequence = '{}{}'.format(sequence_obj.prefix or '', vals['identification_code'])
            patient_class = Patient

        vals.update({'identification_code': sequence, 'is_patient': True})

        person = super(patient_class, self).create(vals)

        #  Obtiene información del SIS
        if person.sis_nro_contrato:
            sis_info = {
                'name': 'SIS',
                'ins_no': person.sis_nro_contrato,
                'start_date': fields.Datetime.from_string(person.sis_fecha_afiliacion),
                'patient': person.id,
                'regime': 1,
                'ins_type': 1,
                'state': 'Active' if person.sis_estado == ACTIVO else '',
                'medical_center': person.sis_eess_nombre,
                'medical_center_address': person.sis_eess_direccion,
                'owner_type': 1,
            }
            person.write({'seguro_id': [[0, False, sis_info]]})

        return person

    @api.multi
    def write(self, vals):
        if not ('first_name' in vals or 'last_name' in vals or 'last_name_2' in vals):
            return super(OehMedicalPatient, self).write(vals)

        for record in self:
            values = vals.copy()
            t_name = (values.get('last_name') or record.last_name or '',
                      values.get('last_name_2') or record.last_name_2 or '',
                      values.get('first_name') or record.first_name) or ''
            values.update({'name': u' '.join(t_name)})

            super(OehMedicalPatient, record).write(values)

    _sql_constraints = [
        ('unique_identification_code', 'unique(identification_code)', u'La historia clínica ya existe.'),
    ]
