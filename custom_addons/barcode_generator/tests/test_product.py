from odoo.tests.common import TransactionCase

class TestProductTemplate(TransactionCase):

    def setUp(self):
        super().setUp()

        # Create a test record
        self.product = self.env['product.template'].create({
            'name': 'Test Product',
            'list_price': 100.00
        })

    def test_product_creation(self):
        # Check if barcode is generated automatically on create
        self.assertTrue(self.product.barcode, "Barcode not generated on create")

    def  test_product_update(self):
        # Check if barcode is generated automatically on write
        self.product.write({'name': 'Updated Test Product'})
        self.assertTrue(self.product.barcode, "Barcode not generated on write")
