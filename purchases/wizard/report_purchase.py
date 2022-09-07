from odoo import api, fields, models, _


class PurchaseExcel(models.TransientModel):
    _name = 'purchase.xls'
    _description = 'Purchase Excel'

    name = fields.Char(string='test12')
    creation_date = fields.Date(string="Từ ngày", default=fields.Date.today())
    due_date = fields.Date(string="Đến ngày", default=fields.Date.today())
    lines = fields.One2many('purchase.xls.line', 'purchase_xls_id')
    requests_by = fields.Many2one('purchase.request', 'requests_by')

    def view_report(self):
        self.lines.unlink()
        self.create_line()
        return {
            'name': _('Báo cáo'),
            'res_model': 'purchase.xls.line',
            'view_mode': 'tree,graph',
            'view_ids': [(4, self.env.ref('purchases.purchase_xls_line_view_tree').id),
                         (4, self.env.ref('purchases.purchase_xls_line_view_graph').id)],
            'domain': [('purchase_xls_id', '=', self.id)],
            'type': 'ir.actions.act_window',
            'target': 'main'
        }

    def create_line(self):
        if self.env.is_admin():
            self.env.cr.execute(f"""select prl.request_id, pr.requests_by, prl.product_id, pr.creation_date,
                                                    pr.due_date, prl.requests_quantity, prl.estimated_unit_price 
                                                    from purchase_request_line prl
                                                    inner join purchase_request pr
                                                    ON prl.request_id = pr.id
                                                    Where pr.creation_date between %s AND %s
                                                    """,
                                (self.creation_date, self.due_date))
        else:
            self.env.cr.execute(f"""select prl.request_id, pr.requests_by, prl.product_id, pr.creation_date,
                                        pr.due_date, prl.requests_quantity, prl.estimated_unit_price 
                                        from purchase_request_line prl
                                        inner join purchase_request pr
                                        ON prl.request_id = pr.id
                                        Where pr.creation_date between %s AND %s
                                        AND pr.requests_by = %s
                                        """,
                                (self.creation_date, self.due_date, self.env.user.id))
        vals = self._cr.fetchall()
        for val in vals:
            self.env['purchase.xls.line'].create({
                'purchase_xls_id': self.id,
                'requested_id': val[0],
                'product_id': val[2],
                'creation_date': val[3],
                'due_date': val[4],
                'requests_quantity': val[5],
                'estimated_unit_price': val[6]
            })

    def print_report(self):
        self.lines.unlink()
        self.create_line()

        return {
            'type': 'ir.actions.act_url',
            'url': ('/report/xlsx/purchases.report_xlsx_wizard/%s' % self.id),
            'target': 'new',
            'res_id': self.id,
        }
        # self.purchase_request_id.write({
        #     'val_fetch': vals
        # })
        #
        # return self.env.ref('purchaseordered.report_request_stat_xlsx').report_action(self.purchase_request_id)


class PurchaseExcelLine(models.TransientModel):
    _name = 'purchase.xls.line'

    purchase_xls_id = fields.Many2one('purchase.xls')
    product_id = fields.Many2one("product.product", string="Sản phẩm", required=True)
    requested_id = fields.Many2one("purchase.request", string="Đơn yêu cầu")
    product_uom_id = fields.Many2one("uom.uom", related='product_id.uom_id', string="Đơn vị tính")
    creation_date = fields.Date(string="Ngày yêu cầu", default=fields.Date.today())
    due_date = fields.Date(string="Ngày cần cấp", required=True, default=fields.Date.today())
    requests_quantity = fields.Integer(string="Số lượng yêu cầu", required=True)
    # delivered_quantity = fields.Float(string="Số lượng đã đưa", copy=False, readonly=True)
    estimated_unit_price = fields.Float(string="Đơn giá dự kiến")
    estimated_subtotal = fields.Float(string="Chi phí dự kiến")
    # state =
