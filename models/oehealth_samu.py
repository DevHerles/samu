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


class OehealthSamuFuel(models.Model):
    """docstring for OehealthSamuCombustible"""

    _name = 'oehealth.samu.fuel'
    _description = 'OehealthSamuCombustible description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


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
    # mobileunit_id = fields.Many2one('oeh.medical.samu.emergency')
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


class HrEmployee(models.Model):
    """Sincronización de datos de establecimiento."""

    _inherit = 'hr.employee'

    doc_type = fields.Selection(SELECTION_DOC_TYPE, 'Tipo de documento', default=SELECTION_DOC_TYPE_DOI)
    instruction_id = fields.Many2one('oehealth.samu.instruction', u'Instrucción')
    profile_id = fields.Many2one(comodel_name='oehealth.samu.profile', string='Perfil')

    @api.onchange('identification_id', 'doc_type')
    def onchange_identification_id(self):
        for record in self:
            if record.doc_type == SELECTION_DOC_TYPE_DOI:
                if record.identification_id and len(record.identification_id) != 8:
                    raise ValidationError(u'El número de DNI debe tener 8 dígitos.')

                try:
                    data = record.env['consultadatos.reniec'].consultardni(record.identification_id)
                except Exception as ex:
                    raise ValidationError('%s' % ex.message)
                record.name = u'{} {} {}'.format(data.get('nombres', ''), data.get('ape_paterno', ''), data.get('ape_materno', ''))
                record.image = data.get('fotografia', False)
                partner_vals = dict(street=data.get('domicilio', {}).get('direccion_descripcion', ''),
                        name=record.name,
                        image=record.image)
                if not record.address_home_id:
                    partner_id = record.address_home_id.create(partner_vals)
                    record.address_home_id = partner_id.id
                else:
                    record.address_home_id.write(partner_vals)

                user_vals = dict(name=record.name, image=record.image)
                # if not record.user_id:
                #     user_id = record.user_id.create(user_vals)
                #     record.user_id = user_id.id
                # record.fecha_nacimiento = data.get('nacimiento', {}).get('fecha', False)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    
    identification_id = fields.Char(u'Número de documento')


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    identification_id = fields.Char(u'Número de documento')
    state_id = fields.Many2one('res.country.state', u'Región')
    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
    address = fields.Char(string='Dirección')

    @api.onchange('identification_id', 'doc_type')
    def onchange_identification_id(self):
        for record in self:
            if record.doc_type == SELECTION_DOC_TYPE_DOI:
                if record.identification_id and len(record.identification_id) != 8:
                    raise ValidationError(u'El número de DNI debe tener 8 dígitos.')

                try:
                    data = record.env['consultadatos.reniec'].consultardni(record.identification_id)
                except Exception as ex:
                    raise ValidationError('%s' % ex.message)
                record.name = u'{} {} {}'.format(data.get('nombres', ''), data.get('ape_paterno', ''), data.get('ape_materno', ''))
                record.image = data.get('fotografia', False)
                record.address = data.get('domicilio', {}).get('direccion_descripcion', '')
                partner_vals = dict(street=record.address,
                        name=record.name,
                        image=record.image)
                # if not record.address_home_id:
                #     partner_id = record.address_home_id.create(partner_vals)
                #     record.address_home_id = partner_id.id
                # else:
                #     record.address_home_id.write(partner_vals)

                user_vals = dict(name=record.name, image=record.image)
                # if not record.user_id:
                #     user_id = record.user_id.create(user_vals)
                #     record.user_id = user_id.id
                # record.fecha_nacimiento = data.get('nacimiento', {}).get('fecha', False)

    # @api.model
    # def create(self, vals):
    #     __import__('ipdb').set_trace()
    #     res = super(ResUsers, self).create(vals)
    #     partner_vals = dict(identification_id=vals.get('identification_id'), name=vals.get('name'))
    #     res.partner_id.write(partner_vals)


EMERGENCY_TYPE_INPERTINENT = 0
EMERGENCY_TYPE_PERTINENT = 1

EMERGENCY_TYPE_SELECCTION = [
    (EMERGENCY_TYPE_PERTINENT, 'Pertinente'),
    (EMERGENCY_TYPE_INPERTINENT, 'Impertinente'),
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

    doc_date = fields.Date('Fecha de emergencia', default=datetime.today())
    state = fields.Selection(EMERGENCY_STATE, 'Estado', readonly=True, default=lambda *e: IN_CALL)
    emergency_type = fields.Selection(EMERGENCY_TYPE_SELECCTION, 'Tipo de emergencia')
    calldetail_id = fields.Many2one('oehealth.samu.calldetail', 'Detalle de llamada')
    motivoimpertinente_id = fields.Many2one('oehealth.samu.motivoimpertinente', 'Motivo impertinente')
    observation = fields.Text(u'Observación')
    country_id = fields.Many2one(
        comodel_name='res.country', string=u'País',
        default=lambda self: self.env['ir.model.data'].xmlid_to_res_id('base.pe'))
    state_id = fields.Many2one('res.country.state', 'Departamento')
    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
    doc_type = fields.Selection(SELECTION_DOC_TYPE, 'Tipo de documento')
    identification_id = fields.Char(u'Número')
    patient_id = fields.Many2one('res.partner', 'Paciente')
    motivollamada_id = fields.Many2one('oehealth.samu.motivollamada', 'Motivo de llamada')
    emergency_id = fields.Many2one('oeh.medical.samu.emergency', 'Detalle de emergencia')
    # name = fields.Char(u'Código de llamada', size=64, readonly=True, required=True, default=lambda *a: '/')
    name = fields.Char(related='emergency_id.name')
    informant_full_name = fields.Char('Nombres')
    informant_sex = fields.Selection(SELECTION_SEX, 'Sexo')
    informant_doc_type = fields.Selection(SELECTION_DOC_TYPE, 'Tipo de documento')
    informant_identification_id = fields.Char(u'Número de documento')
    informant_phone_number = fields.Char(u'Número de teléfono / celular')
    informant_country_id = fields.Many2one(
        comodel_name='res.country', string=u'País',
        default=lambda self: self.env['ir.model.data'].xmlid_to_res_id('base.pe'))
    informant_state_id = fields.Many2one('res.country.state', u'Región')
    informant_province_id = fields.Many2one('res.country.state', 'Provincia')
    informant_district_id = fields.Many2one('res.country.state', 'Distrito')
    informant_address = fields.Char(u'Dirección')
    informant_address_reference = fields.Text('Referencia')
    informant_gps = fields.Char('GPS')


    @api.one
    def set_to_regulation(self):
        self.state = IN_REGULATION

    @api.one
    def set_to_on_road(self):
        self.state = ON_ROAD

    @api.one
    def set_to_attending(self):
        self.state = IN_ATTENTION

    @api.one
    def set_to_attended(self):
        self.state = ATTENDED

    # @api.model
    # def create(self, vals):
        # sequence = self.env['ir.sequence'].next_by_code('oeh.medical.samu.emergency')
        # vals['name'] = sequence
        # __import__('ipdb').set_trace()
        # res = super(OehealthSamuLlamada, self).create(vals)

    @api.onchange('informant_identification_id', 'informant_doc_type')
    def onchange_informant_identification_id(self):
        for record in self:
            if record.informant_doc_type == SELECTION_DOC_TYPE_DOI:
                if record.informant_identification_id and len(record.informant_identification_id) != 8:
                    raise ValidationError(u'El número de DNI debe tener 8 dígitos.')

                try:
                    data = record.env['consultadatos.reniec'].consultardni(record.informant_identification_id)
                except Exception as ex:
                    raise ValidationError('%s' % ex.message)
                record.informant_full_name = u'{} {} {}'.format(data.get('nombres', ''), data.get('ape_paterno', ''), data.get('ape_materno', ''))
                # record.image = data.get('fotografia', False)
                record.informant_address = data.get('domicilio', {}).get('direccion_descripcion', '')


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


class CountryState(models.Model):
    _description = "Country state"
    _inherit = 'res.country.state'
    _order = 'name'

    code = fields.Char(
        'Country Code', size=9,
        help='The ISO country code in two chars.\n'
        'You can use this field for quick search.')
    state_id = fields.Many2one('res.country.state', 'Departamento')
    province_id = fields.Many2one('res.country.state', 'Provincia')

    code_reniec = fields.Char('Ubigeo Reniec', size=6)

    @api.model
    def buscar_ubigeo(self, ubigeo):
        domain = [('country_id.code', '=', 'PE'), ('code', '=', ubigeo)]
        return self.search(domain, limit=1)

    @api.model
    def consulta_ubigeoxnombres(self, pais, departamento, provincia, distrito):
        domain = [
            ('country_id.name', '=', pais),
            ('state_id.name', '=', departamento),
            ('province_id.name', '=', provincia),
            ('name', '=', distrito),
        ]
        district = self.env['res.country.state'].search(domain, limit=1)
        return district.id and district.code or ''

    @api.model
    def actualizar_xubigeo(self, model_res, res_id, codigo_ubigeo=False):
        u"""" Metodo para actualizar departamento, provincia, distrito de un recurso.

            :param model_res: modelo del recurso
            :param res_id: id del recurso
            :param codigo_ubigeo: 'ubigeo'

        En una acción de servidor:
        for record in records:
            model_state = env['res.country.state']
            model_state.actualizar_xubigeo(model, record.id)
        """
        res = model_res.browse(res_id)
        if not codigo_ubigeo:
            codigo_ubigeo = res.ubigeo
        if codigo_ubigeo and len(codigo_ubigeo) == 6:
            distrito = self.buscar_ubigeo(codigo_ubigeo)

            if distrito:
                value = dict(departamento_id=distrito.state_id.id,
                             provincia_id=distrito.province_id.id,
                             distrito_id=distrito.id)
                res.write(value)
