from odoo import models, fields, api
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)

        if vals.get('state') == 'cancel':
            for order in self:
                crm_stage = self.env.ref('crm.stage_lead3')

                # Check if the "Quote rejection" tag exists, and create it if it doesn't
                tag = self.env['crm.tag'].search(
                    [('name', '=', 'Quote rejection')], limit=1)
                if not tag:
                    tag = self.env['crm.tag'].create(
                        {'name': 'Quote rejection'})

                # Set the priority based on the expected revenue
                if order.amount_total < 500:
                    priority = '1'
                elif order.amount_total < 1000:
                    priority = '2'
                else:
                    priority = '3'

                closing_date = (datetime.today() +
                                timedelta(days=7)).strftime('%Y-%m-%d')
                opportunity_vals = {
                    'name': f'Cancelled quote: {order.name}',
                    'type': 'opportunity',
                    'stage_id': crm_stage.id,
                    'partner_id': order.partner_id.id,
                    'expected_revenue': order.amount_total,
                    'date_deadline': closing_date,
                    'description': f"Product(s) ordered:\n{', '.join(order.order_line.mapped('name'))}\n\nTotal Amount: {order.amount_total}",
                    'tag_ids': [(4, tag.id)],
                    'priority': priority,
                    'probability': 50  # probability is 50%
                }
                opportunity = self.env['crm.lead'].create(opportunity_vals)

        return res
