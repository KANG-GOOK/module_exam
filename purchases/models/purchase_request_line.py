from odoo import models, fields, api
import datetime
from odoo.exceptions import ValidationError


class PurchaseRequestLine(models.Model):
    _name = "purchase.request.line"

    # product_id = fields.Char(string='id')
    product_id = fields.Many2one('product.product', string='Product')
    product_uom_id = fields.Many2one("uom.uom", string="Đơn vị tính",related='product_id.uom_id')
    requests_quantity = fields.Integer(string="Reqests of quantity", required=True)  # số lượng yêu cầu
    estimated_unit_price = fields.Integer(string="Estimated unit price")  # Đơn giá dự kiến
    estimated_subtotal = fields.Float(string="Estimated Subtotal", compute='_get_estimated_subtotal',
                                      store=True)  # Chi phí dự kiến
    due_date = fields.Datetime(string="Due date", default=fields.Datetime.now)  # ngày cần cấp
    description = fields.Text(string="Description")
    request_id = fields.Many2one('purchase.request', string='Request', ondelete='cascade', index=True,
                                 copy=False)
    # delivered_quantity = fields.Selection(selection=[('1', 'Approved'), ('0', 'complete')])

    # chi phí dự kiến = Đơn giá * số lượng
    @api.depends('requests_quantity', 'estimated_unit_price')
    def _get_estimated_subtotal(self):
        for i in self:
            i.estimated_subtotal = i.requests_quantity * i.estimated_unit_price

    # Số lượng yêu cầu phải khác 0
    @api.constrains('requests_quantity')
    def validate_quantity(self):
        for vq in self:
            if vq.requests_quantity <= 0:
                raise ValidationError('Giá trị nhập vào phải khác 0')
