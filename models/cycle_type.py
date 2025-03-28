from odoo import models, fields, api

class CycleTypeVapor(models.Model):
    _inherit = 'afr.cycle.type'

    is_vapor = fields.Boolean('É Autoclave Vapor', default=False)
 