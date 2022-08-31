from odoo import models, fields, api, _
import datetime
from odoo.exceptions import ValidationError


class PurchaseRequest(models.Model):
    _name = "purchase.request"

    name = fields.Char(string="Votes Number", readonly=True, required=True, copy=False, default='New')
    requests_by = fields.Many2one('res.users', string='Request by', required=True,
                                  default=lambda self: self.env.user)  # người tao
    department = fields.Many2one('res.users', string='Department', required=True,
                                 default=lambda self: self.env.user)  # Bộ phận
    cost_total = fields.Float(string="Cost Total", compute='get_cost_total',
                              store=True)  # Tổng chi phí ??? Tổng các sản phẩm chọn dưới phần list
    creation_date = fields.Datetime(string="Creation date", default=fields.Datetime.now)  # Ngày yêu cầu
    due_date = fields.Datetime(string="Due date", default=fields.Datetime.now)  # Ngày cần cấp
    approved_date = fields.Datetime(string="Approved date", readonly=True)  # (Ngày phê duyệt)
    company = fields.Many2one('res.company', string='Company', required=True,
                              ondelete='cascade')  # mặc đih user công ty
    reject_reason = fields.Text(string="Reject Reason")  # Lý do từ chối
    state = fields.Selection(
        selection=[('1', 'Dự thảo'), ('2', 'Chờ duyệt'), ('3', 'Đã duyệt'), ('4', 'Hoàn thành'),
                   ('5', 'Từ chối'),
                   ('6', 'Hủy')],
        string='State', default='1')
    request_line = fields.One2many('purchase.request.line', 'request_id', string='Request Lines')
    # purchase_id = fields.One2many('wizard.import.purchase.request.line')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'New'
        # vals['user_id'] = self.env.uid
        result = super(PurchaseRequest, self).create(vals)
        return result

    # dự thảo => chờ duyệt
    def request_approval(self):
        self.state = '2'

    # chờ duyệt => đã duyệt
    def phe_duyet(self):
        self.state = '3'
        self.approved_date = datetime.datetime.now()

    # chờ duyệt => từ chối
    def tu_choi(self):
        # elf.st  sate = '5'
        self.approved_date = datetime.datetime.now()
        view_id = self.env.ref('purchases.product_in_wizard_form_view')
        return {
            'name': _('ly do tu choi'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'reject.reason',
            'views': [(view_id.id, 'form')],
            'view_id': view_id.id,
            'target': 'new',
            'context': {
                'default_purchase_request_id': self.id
            }
        }

    # đã duyệt => hoàn thành
    def hoan_thanh(self):
        self.state = '4'

    def cancel_(self):
        self.state = '6'

    # từ chối => dự thảo
    def chuyen_ve_du_thao(self):
        self.state = '1'

    @api.depends('request_line.estimated_subtotal')
    def get_cost_total(self):
        for c in self:
            c.cost_total = sum(c.mapped('request_line.estimated_subtotal'))

    def button_open_wizard_import_purchase_request(self):
        self.ensure_one()
        return {
            'name': _(''),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.import.purchase.request.line',
            'no_destroy': True,
            'target': 'new',
            'view_id': self.env.ref('purchases.wizard_import_purchase_request_line_view_form') and self.env.ref(
                'purchases.wizard_import_purchase_request_line_view_form').id or False,
            'context': {'default_purchase_id': self.id},
        }
