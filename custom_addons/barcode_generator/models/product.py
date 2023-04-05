from odoo import api, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self, vals):
        if not vals.get('barcode'):
            barcode = self.env['ir.sequence'].next_by_code('product.barcode')
            vals['barcode'] = barcode
        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        if not vals.get('barcode'):
            barcode = self.env['ir.sequence'].next_by_code('product.barcode')
            vals['barcode'] = barcode
        return super(ProductTemplate, self).write(vals)
