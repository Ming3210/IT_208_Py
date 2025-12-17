from odoo import models, fields

class Demo(models.Model):
    _name = 'demo'
    _description = 'Demo Hello World Model'
    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')


class createTableDemo(models.Model):
    _name = 'bat.dong.san'
    _description = 'Bat_dong_san'
    name = fields.Char(string='Tên', type='char', required=True)
    description = fields.Text(string='Mô tả', type='text')
    postcode = fields.Char(string='Mã bưu điện', type='char')
    date_availablity = fields.Date(string='Ngày có sẵn', type='date', default=fields.Date.today)
    expected_price = fields.Float(string='Giá dự kiến', type='float', required=True)
    selling_price = fields.Float(string='Giá bán thực tế', type='float', readonly=True)

class createTableHouseDetail(models.Model):
    _name = 'chi.tiet.nha'
    _description = 'Chi_tiet_nha'
    bedrooms = fields.Integer(string='Số phòng ngủ', type='int', default=2)
    living_area = fields.Integer(string='Diện tích phòng khách', type='int')
    facades = fields.Integer(string='Mặt tiền', type='int')
    garage = fields.Integer(string='Số garage', type='bool', default=False)
    garden = fields.Boolean(string='Có vườn', type='bool', default=False)
    garden_area = fields.Integer(string='Diện tích vườn', type='int')
    garden_orientation = fields.Selection(
        string='Hướng vườn',
        selection=[
            ('north', 'Bắc'),
            ('south', 'Nam'),
            ('east', 'Đông'),
            ('west', 'Tây')
        ],
        type='selection'
    )

    


