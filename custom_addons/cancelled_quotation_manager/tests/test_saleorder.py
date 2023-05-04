from odoo.tests.common import TransactionCase
from lxml import etree

class TestSaleOrder(TransactionCase):
    
    def test_cancelled_order_opportunity_created(self):
        # Create a test partner
        partner = self.env['res.partner'].create({'name': 'Test Partner'})

        # Create a test sale order with one product
        product = self.env.ref('product.product_product_1')
        order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'name': 'Test Product',
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': 100,
            })]
        })

        # Cancel the sale order
        order.write({'state': 'cancel'})

        # Check if the opportunity is created
        opportunity = self.env['crm.lead'].search([('name', '=', f'Cancelled quote: {order.name}')], limit=1)
        self.assertTrue(opportunity, "Cancelled quote opportunity not created")
        self.assertEqual(opportunity.partner_id, partner, "Opportunity has incorrect partner")
        self.assertEqual(opportunity.stage_id, self.env.ref('crm.stage_lead3'), "Opportunity is not in the correct stage")
        self.assertEqual(opportunity.expected_revenue, order.amount_total, "Opportunity expected revenue is incorrect")
        expected_description = f"Product(s) ordered:\n{', '.join(order.order_line.mapped('name'))}\n\nTotal Amount: {order.amount_total}"
        opportunity_description = etree.HTML(opportunity.description).xpath("string()").strip()
        self.assertEquals(opportunity_description, expected_description, "Opportunity description is incorrect")

    def test_write_cancel_order_no_tag(self):
        # Retrieve a reference to the 'base.res_partner_2' partner record
        partner = self.env.ref('base.res_partner_2')

        # Retrieve a reference to the 'product.product_product_8' product record
        product = self.env.ref('product.product_product_8')

        # Delete any existing 'Quote rejection' tags
        self.env['crm.tag'].search([('name', '=', 'Quote rejection')]).unlink()

        # Create a sale order
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {'product_id': product.id, 'product_uom_qty': 1})],
        })

        # Write the sale order in cancel state
        sale_order.write({'state': 'cancel'})

        opportunities = self.env['crm.lead'].search([])


        # Check that the opportunity has the correct tag
        opportunity = opportunities[0]
        tag = self.env['crm.tag'].search([('name', '=', 'Quote rejection')])
        self.assertEqual(len(tag), 1)
        self.assertIn(tag.id, opportunity.tag_ids.ids)

    def test_cancel_order_high_amount(self):
        # Create a test partner
        partner = self.env['res.partner'].create({'name': 'Test Partner'})

        # Create a test sale order with one product and high amount
        product = self.env.ref('product.product_product_1')
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'name': 'Test Product',
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': 2000,
            })]
        })

        # Cancel the sale order
        sale_order.write({'state': 'cancel'})

        # Check if opportunity is created with a very high priority 
        opportunity = self.env['crm.lead'].search([('name', '=', f'Cancelled quote: {sale_order.name}')], order='id desc', limit=1)
        self.assertEqual(opportunity.priority, '3', "Opportunity priority is not 3")
    
    def test_cancel_order_medium_amount(self):
        # Create a test partner
        partner = self.env['res.partner'].create({'name': 'Test Partner'})

        # Create a test sale order with one product and medium amount
        product = self.env.ref('product.product_product_1')
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'name': 'Test Product',
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': 750,
            })]
        })

        # Cancel the sale order
        sale_order.write({'state': 'cancel'})

        # Check if opportunity is created with a high priority 
        opportunity = self.env['crm.lead'].search([('name', '=', f'Cancelled quote: {sale_order.name}')], order='id desc', limit=1)
        self.assertEqual(opportunity.priority, '2', "Opportunity priority is not 2")

    def test_cancel_order_low_amount(self):
        # Create a test partner
        partner = self.env['res.partner'].create({'name': 'Test Partner'})

        # Create a test sale order with one product and low amount
        product = self.env.ref('product.product_product_1')
        sale_order = self.env['sale.order'].create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'name': 'Test Product',
                'product_id': product.id,
                'product_uom_qty': 1,
                'price_unit': 300,
            })]
        })

        # Cancel the sale order
        sale_order.write({'state': 'cancel'})

        # Check if opportunity is created with a medium priority 
        opportunity = self.env['crm.lead'].search([('name', '=', f'Cancelled quote: {sale_order.name}')], order='id desc', limit=1)
        self.assertEqual(opportunity.priority, '1', "Opportunity priority is not 2")