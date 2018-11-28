# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError

SELECTION_YES = 1
SELECTION_NO = 0
SELECTION_YES_NO = [
    (SELECTION_YES, 'Si'),
    (SELECTION_NO, 'No')
]
SELECTION_SEX_MALE = '01'
SELECTION_SEX_FEMALE = '02'
SELECTION_SEX = [
    (SELECTION_SEX_MALE, 'Masculino'),
    (SELECTION_SEX_FEMALE, 'Femenino'),
]
SELECTION_DOC_TYPE_DOI = '01'
SELECTION_DOC_TYPE_PASSPORT = '02'
SELECTION_DOC_TYPE = [
    (SELECTION_DOC_TYPE_DOI, 'DNI'),
    (SELECTION_DOC_TYPE_PASSPORT, 'PASAPORTE'),
]

STATE_AVAILABLE = 'available'
STATE_BUSSY = 'bussy'
STATE_MAINTENANCE = 'maintenance'

SELECTION_MOBILE_STATE = [
    (STATE_AVAILABLE, 'Disponible'),
    (STATE_BUSSY, 'En servicio'),
    (STATE_MAINTENANCE, 'En mantenimiento'),
]


class OehealthSamuBodywork(models.Model):
    """docstring for OehealthSamuCarroceria"""

    _name = 'oehealth.samu.bodywork'
    _description = 'OehealthSamuCarroceria description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuCondition(models.Model):
    """docstring for OehealthSamuCondition"""

    _name = 'oehealth.samu.condition'
    _description = 'OehealthSamuCondition description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuFuel(models.Model):
    """docstring for OehealthSamuCombustible"""

    _name = 'oehealth.samu.fuel'
    _description = 'OehealthSamuCombustible description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuModel(models.Model):
    """docstring for OehealthSamuModel"""

    _name = 'oehealth.samu.model'
    _description = 'OehealthSamuModel description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuMaintenance(models.Model):
    """docstring for OehealthSamuMantainance"""

    _description = 'OehealthSamuMantainance description'
    _name = 'oehealth.samu.maintenance'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuBrand(models.Model):
    """docstring for OehealthSamuBrand"""

    _name = 'oehealth.samu.brand'
    _description = 'OehealthSamuBrand description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')

    _sql_constraints = [
        ('unique_brand_code', 'unique(brand_code)', u'El código de la marca ya existe.'),
    ]


class OehealthSamuUnitytype(models.Model):
    """docstring for OehealthSamuCombustible"""

    _name = 'oehealth.samu.unitytype'
    _description = 'OehealthSamuCombustible description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class UnidadesMoviles(models.Model):
    """docstring for UnidadesMoviles"""

    _name = 'oehealth.samu.mobileunit'
    _description = 'UnidadesMoviles description'

    state = fields.Selection(SELECTION_MOBILE_STATE, 'Estado', readonly=True, default=lambda *e: STATE_AVAILABLE)
    name = fields.Char(string='Unidad movil')
    carroceria_id = fields.Many2one('oehealth.samu.bodywork', u'Carrocería')
    condition_id = fields.Many2one('oehealth.samu.condition', u'Condición')
    has_gps = fields.Boolean(string='¿Tiene GPS?')
    kilometraje = fields.Integer(string='Kilometraje')
    combustible_id = fields.Many2one('oehealth.samu.fuel', 'Combustible')
    codigo_patrimonial = fields.Char(u'Código patrimonial')
    modelo_id = fields.Many2one('oehealth.samu.model', 'Modelo')
    mantainance_id = fields.Many2one('oehealth.samu.maintenance', 'Mantenimiento cada')
    placa = fields.Char(string='Placa', help='Placa de unidad movil')
    brand_id = fields.Many2one('oehealth.samu.brand', 'Marca de la unidad movil')
    image = fields.Binary('Foto')
    line_ids = fields.One2many('oehealth.samu.mobileunit.line', 'line_id', u'Imágenes')
    state_id = fields.Many2one('res.country.state', u'Región')
    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
    unitytype_id = fields.Many2one('oehealth.samu.unitytype', 'Tipo')

    current_mileage = fields.Integer('Kilometraje actual')
    previous_mileage = fields.Integer('Kilometraje anterior')
    last_mileage_traveled = fields.Integer(u'Último kilometraje recorrido')
    current_fuel = fields.Float('Combustible actual')
    consumed_fuel = fields.Float('Combustible consumido')
    soat_expiration_date = fields.Date('Fecha de caducida de SOAT')
    next_technical_review = fields.Date(u'Próxima fecha de revisión técnica')
    approximate_maintenance_date = fields.Date('Fecha aproximada de mantenimiento')
    mechanical_company_id = fields.Many2one('oehealth.samu.mechanicalcompany', u'Empresa mecánica')

    radiator_water = fields.Selection(SELECTION_YES_NO, 'Agua de radiador')
    battery_water = fields.Selection(SELECTION_YES_NO, u'Agua de batería')
    wiper_water = fields.Selection(SELECTION_YES_NO, 'Agua de limpiaparabrisas')
    siren = fields.Selection(SELECTION_YES_NO, 'Sirena')
    high_light = fields.Selection(SELECTION_YES_NO, 'Luz alta')
    low_light = fields.Selection(SELECTION_YES_NO, 'Luz baja')

    mobile_unit_id = fields.Many2one('oehealth.samu.llamada', 'Llamada')


class UnidadesMovilesLinea(models.Model):
    """docstring for UnidadesMovilesLinea"""

    _name = 'oehealth.samu.mobileunit.line'
    _description = 'UnidadesMovilesLinea description'

    name = fields.Char('Nombre')
    line_id = fields.Many2one(comodel_name='oehealth.samu.mobileunit', string='Imágenes', help='Help note')
    image = fields.Binary('Foto')


class OehealthSamuMechanicalcompany(models.Model):
    """docstring for OehealthSamuMechanicalcompany"""

    _name = 'oehealth.samu.mechanicalcompany'
    _description = 'OehealthSamuMechanicalcompany description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuProfile(models.Model):
    """docstring for OehealthSamuProfile"""

    _name = 'oehealth.samu.profile'
    _description = 'OehealthSamuProfile description'

    name = fields.Char('Perfil')
    code = fields.Char('Código del perfil')


class OehealthSamuInstruction(models.Model):
    """docstring for OehealthSamuInstruction"""

    _name = 'oehealth.samu.instruction'
    _description = 'OehealthSamuInstruction description'

    name = fields.Char('Instrucción', help='Grado de instrucción')
    code = fields.Char('Código', help='Código de grado de instrucción')


class OehealthSamuInformant(models.Model):
    """docstring for OehealthSamuInformant"""

    _name = 'oehealth.samu.informant'
    _description = 'OehealthSamuInformant description'

    code = fields.Char(u'Código')
    full_name = fields.Char('Nombres')
    sex = fields.Selection(SELECTION_SEX, 'Sexo')
    doc_type = fields.Selection(SELECTION_DOC_TYPE, 'Tipo de documento')
    identification_id = fields.Char(u'Número de documento')
    phone_number = fields.Char(u'Número de teléfono / celular')
    state_id = fields.Many2one('res.country.state', u'Región')
    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
    address = fields.Char(u'Dirección')
    address_reference = fields.Text('Referencia')
    gps = fields.Char('GPS')


EMERGENCY_TYPE_PERTINENT = 1
EMERGENCY_TYPE_INPERTINENT = 0

EMERGENCY_TYPE_SELECCTION = [
    (EMERGENCY_TYPE_PERTINENT, 'Pertinente'),
    (EMERGENCY_TYPE_INPERTINENT, 'No pertinente'),
]

IN_CALL = 'llamada'
IN_REGULATION = 'regulacion'
ON_ROAD = 'camino'
IN_ATTENTION = 'atencion'
ATTENDED = 'atendido'

EMERGENCY_STATE = [
    (IN_CALL, 'Llamada entrante'),
    (IN_REGULATION, u'Regulación'),
    (ON_ROAD, 'En camino'),
    (IN_ATTENTION, 'En atención'),
    (ATTENDED, 'Atendido')
]


class OehealthSamuLlamada(models.Model):
    """docstring for OehealthSamuLlamadas"""

    _name = 'oehealth.samu.llamada'
    _description = 'OehealthSamuLlamadas description'

    doc_date = fields.Date('Fecha de emergencia', default=datetime.today(), required=True)
    state = fields.Selection(EMERGENCY_STATE, 'Estado', readonly=True, default=lambda *e: IN_CALL)
    emergency_type = fields.Selection([(EMERGENCY_TYPE_PERTINENT, 'Pertinente'), (EMERGENCY_TYPE_INPERTINENT, 'No pertinente')], 'Tipo de emergencia', default=lambda *e: EMERGENCY_TYPE_PERTINENT, required=True)
    calldetail_id = fields.Many2one('oehealth.samu.calldetail', 'Detalle de llamada', required=True)
    motivoimpertinente_id = fields.Many2one('oehealth.samu.motivoimpertinente', 'Motivo impertinente')
    observation = fields.Text(u'Observación')
    country_id = fields.Many2one(
        comodel_name='res.country', string=u'País',
        default=lambda self: self.env['ir.model.data'].xmlid_to_res_id('base.pe'), required=True)
    state_id = fields.Many2one('res.country.state', 'Departamento', required=True)
    province_id = fields.Many2one('res.country.state', 'Provincia', required=True)
    district_id = fields.Many2one('res.country.state', 'Distrito', required=True)
    patient_id = fields.Many2one('res.partner', 'Paciente')
    motivollamada_id = fields.Many2one('oehealth.samu.motivollamada', 'Motivo de llamada', required=True)
    emergency_id = fields.Many2one('oeh.medical.samu.emergency', 'Detalle de emergencia')
    name = fields.Char(related='emergency_id.name')
    informant_full_name = fields.Char('Nombres', readonly=True, store=True, required=True)
    informant_sex = fields.Selection(SELECTION_SEX, 'Sexo')
    informant_doc_type = fields.Selection(SELECTION_DOC_TYPE, 'Tipo de documento', required=True)
    informant_identification_id = fields.Char(u'Número de documento', required=True)
    informant_phone_number = fields.Char(u'Número de teléfono / celular', required=True)
    informant_country_id = fields.Many2one(
        comodel_name='res.country', string=u'País',
        default=lambda self: self.env['ir.model.data'].xmlid_to_res_id('base.pe'), required=True)
    informant_state_id = fields.Many2one('res.country.state', u'Región', required=True)
    informant_province_id = fields.Many2one('res.country.state', 'Provincia', required=True)
    informant_district_id = fields.Many2one('res.country.state', 'Distrito', required=True)
    informant_address = fields.Char(u'Dirección', required=True)
    informant_address_reference = fields.Text('Referencia', required=True)
    informant_gps = fields.Char('GPS')

    pertinents = fields.Integer('Pertinentes', readonly=True, store=True)
    inpertinents = fields.Integer('No pertinentes', readonly=True, store=True)
    total_calls = fields.Integer('Total de llamadas', compute='_compute_total_calls', store=True)

    samu_patient_ids = fields.One2many(comodel_name='oeh.medical.patient', inverse_name='samu_patient_id', string='Pacientes')

    mobile_unit_ids = fields.One2many(comodel_name='oehealth.samu.mobileunit', inverse_name='mobile_unit_id', string=u'Unidades móviles')

    @api.one
    def set_to_regulation(self):
        self.state = IN_REGULATION

    @api.one
    def set_to_on_road(self):
        self.state = ON_ROAD
        for record in self.mobile_unit_ids:
            record.write({'state': STATE_BUSSY})

    @api.one
    def set_to_attending(self):
        self.state = IN_ATTENTION

    @api.one
    def set_to_attended(self):
        self.state = ATTENDED
        for record in self.mobile_unit_ids:
            record.write({'state': STATE_AVAILABLE})

    @api.multi
    def _compute_total_calls(self):
        self.ensure_one()
        self.total_calls = self.pertinents + self.inpertinents

    @api.onchange('informant_identification_id', 'informant_doc_type')
    def onchange_informant_identification_id(self):
        for record in self:
            if not record.informant_doc_type or not record.informant_identification_id:
                continue

            if record.informant_doc_type == SELECTION_DOC_TYPE_DOI:
                if record.informant_identification_id and len(record.informant_identification_id) != 8:
                    raise ValidationError(u'El número de DNI debe tener 8 dígitos.')

                try:
                    data = record.env['consultadatos.reniec'].consultardni(record.informant_identification_id)
                except Exception as ex:
                    raise ValidationError('%s' % ex.message)
                record.informant_full_name = u'{} {} {}'.format(data.get('nombres', ''), data.get('ape_paterno', ''), data.get('ape_materno', ''))
                district_id = self.env['res.country.state'].search([
                    ('country_id', '=', self.country_id.id),
                    ('code_reniec', '=', data.get("get_distrito_domicilio_ubigeo_reniec", 'no_ubigeo'))])
                record.informant_state_id = district_id.state_id.id or False,
                record.informant_province_id = district_id.province_id.id or False,
                record.informant_district_id = district_id.id or False,

    @api.onchange('informant_phone_number')
    def onchange_informant_phone_number(self):
        self.ensure_one()
        for record in self:
            if record.informant_phone_number:
                domain_pertinent = [('informant_phone_number', '=', record.informant_phone_number), ('emergency_type', '=', EMERGENCY_TYPE_PERTINENT)]
                domain_inpertinent = [('informant_phone_number', '=', record.informant_phone_number), ('emergency_type', '=', EMERGENCY_TYPE_INPERTINENT)]
                pertinents = self.env['oehealth.samu.llamada'].search(domain_pertinent, limit=1)
                inpertinents = self.env['oehealth.samu.llamada'].search(domain_inpertinent, limit=1)

                record.pertinents = pertinents.search_count([]) or 0
                record.inpertinents = inpertinents.search_count([]) or 0
                record.total_calls = record.pertinents + record.inpertinents


class OehealthSamuPatient(models.Model):
    """docstring for OehealthSamuPatient"""

    _inherit = 'oeh.medical.patient'

    samu_patient_id = fields.Many2one('oehealt.samu.llamada', 'Paciente')
    samu_obs = fields.Text('Observaciones')
    elapsed_time = fields.Integer('Tiempo transcurrido (minutos)', required=True)
    course = fields.Selection(selection=[('0', 'Estacionario'), ('1', 'Otro')], string='Curso', required=True)
    priority = fields.Selection(selection=[('1', 'I'), ('2', 'II'), ('3', 'III')], string='Prioridad', required=True)


class OehealthSamuMotivoLlamada(models.Model):
    """docstring for OehealthSamuMotivoLlamada"""

    _name = 'oehealth.samu.motivollamada'
    _description = 'OehealthSamuMotivoLlamada description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuCallDetail(models.Model):
    """docstring for OehealthSamuCallDetail"""

    _name = 'oehealth.samu.calldetail'
    _description = 'OehealthSamuCallDetail description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuMotivoImpertinente(models.Model):
    """docstring for OehealthSamuMotivoImpertinente"""

    _name = 'oehealth.samu.motivoimpertinente'
    _description = 'OehealthSamuMotivoImpertinente description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')
