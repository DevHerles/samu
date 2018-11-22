# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError

DOC_TYPE_SELECTION_DNI = '01'
DOC_TYPE_SELECTION_PASSPORT = '02'

DOC_TYPE_SELECTION = [
    (DOC_TYPE_SELECTION_DNI, 'DNI'),
    (DOC_TYPE_SELECTION_PASSPORT, 'PASAPORTE'),
]


class OehealthSamuCarroceria(models.Model):
    """docstring for OehealthSamuCarroceria"""

    _name = 'oehealth.samu.carroceria'
    _description = 'OehealthSamuCarroceria description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuCondition(models.Model):
    """docstring for OehealthSamuCondition"""

    _name = 'oehealth.samu.condition'
    _description = 'OehealthSamuCondition description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuCombustible(models.Model):
    """docstring for OehealthSamuCombustible"""

    _name = 'oehealth.samu.combustible'
    _description = 'OehealthSamuCombustible description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuModel(models.Model):
    """docstring for OehealthSamuModel"""

    _name = 'oehealth.samu.model'
    _description = 'OehealthSamuModel description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuMantainance(models.Model):
    """docstring for OehealthSamuMantainance"""

    _name = 'oehealth.samu.mantainance'
    _description = 'OehealthSamuMantainance description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuBrand(models.Model):
    """docstring for OehealthSamuBrand"""

    _name = 'oehealth.samu.brand'
    _description = 'OehealthSamuBrand description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')


class OehealthSamuCombustible(models.Model):
    """docstring for OehealthSamuCombustible"""

    _name = 'oehealth.samu.combustible'
    _description = 'OehealthSamuCombustible description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')

class UnidadesMoviles(models.Model):
    """docstring for UnidadesMoviles"""

    _name = 'oehealth.samu.unidadesmoviles'
    _description = 'UnidadesMoviles description'

    name = fields.Char(string='Unidad movil')
    carroceria_id = fields.Many2one('oehealth.samu.carroceria', u'Carrocería')
    condition_id = fields.Many2one('oehealth.samu.condition', u'Condición')
    has_gps = fields.Boolean(string='¿Tiene GPS?')
    kilometraje = fields.Integer(string='Kilometraje')
    combustible_id = fields.Many2one('oehealth.samu.combustible', 'Combustible')
    codigo_patrimonial = fields.Char(u'Código patrimonial')
    modelo_id = fields.Many2one('oehealth.samu.model', 'Modelo')
    mantainance_id = fields.Many2one('oehealth.samu.mantainance', 'Mantenimiento cada')
    placa = fields.Char(string='Placa', help='Placa de unidad movil')
    brand_id = fields.Many2one(comodel_name='oehealth.samu.brand', string='Marca de la unidad movil')
    image = fields.Binary('Foto')
    line_ids = fields.One2many(comodel_name='oehealth.samu.unidadesmoviles.line', inverse_name='line_id', string=u'Imágenes')

class UnidadesMovilesLinea(models.Model):
    """docstring for UnidadesMovilesLinea"""

    _name = 'oehealth.samu.unidadesmoviles.line'
    _description = 'UnidadesMovilesLinea description'

    name = fields.Char('Nombre')
    line_id = fields.Many2one(comodel_name='oehealth.samu.unidadesmoviles', string='Imágenes', help='Help note')
    image = fields.Binary('Foto')


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


class HrEmployee(models.Model):
    """Sincronización de datos de establecimiento."""

    _inherit = 'hr.employee'

    doc_type = fields.Selection(DOC_TYPE_SELECTION, 'Tipo de documento', default=DOC_TYPE_SELECTION_DNI)
    instruction_id = fields.Many2one('oehealth.samu.instruction', u'Instrucción')
    profile_id = fields.Many2one(comodel_name='oehealth.samu.profile', string='Perfil')

    @api.onchange('identification_id', 'doc_type')
    def onchange_identification_id(self):
        for record in self:
            if record.doc_type == DOC_TYPE_SELECTION_DNI:
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

    doc_type = fields.Selection(DOC_TYPE_SELECTION, 'Tipo de documento', default=DOC_TYPE_SELECTION_DNI)
    identification_id = fields.Char(u'Número de documento')


class ResUsers(models.Model):
    _inherit = 'res.users'
    doc_type = fields.Selection(DOC_TYPE_SELECTION, 'Tipo de documento', default=DOC_TYPE_SELECTION_DNI)
    identification_id = fields.Char(u'Número de documento')
    state_id = fields.Many2one('res.country.state', u'Región')
    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
    address = fields.Char(string='Dirección')

    @api.onchange('identification_id', 'doc_type')
    def onchange_identification_id(self):
        for record in self:
            if record.doc_type == DOC_TYPE_SELECTION_DNI:
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


EMERGENCY_TYPE_INPERTENENT = 0
EMERGENCY_TYPE_PERTINENT = 1

EMERGENCY_TYPE_SELECCTION = [
    (EMERGENCY_TYPE_PERTINENT, 'Pertinente'),
    (EMERGENCY_TYPE_INPERTENENT, 'Impertinente'),
    ]


class OehealthSamuLlamada(models.Model):
    """docstring for OehealthSamuLlamadas"""

    _name = 'oehealth.samu.llamada'
    _description = 'OehealthSamuLlamadas description'

    code = fields.Char(u'Código')
    name = fields.Char('Nombre')
    emergency_type = fields.Selection(EMERGENCY_TYPE_SELECCTION, 'Tipo de emergencia')
    calldetail_id = fields.Many2one('oehealth.samu.calldetail', 'Detalle de llamada')
    motivoimpertinente_id = fields.Many2one('oehealth.samu.motivoimpertinente', 'Motivo impertinente')
    observation = fields.Text(u'Observación')
    state_id = fields.Many2one('res.country.state', 'Departamento')
    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
    doc_type = fields.Selection(DOC_TYPE_SELECTION, 'Tipo de documento')
    identification_id = fields.Char(u'Número')
    patient_id = fields.Many2one('res.partner', 'Paciente')
    motivollamada_id = fields.Many2one('oehealth.samu.motivollamada', 'Motivo de llamada')


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
