# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class pixkah_protossmetales(models.Model):
#     _name = 'pixkah_protossmetales.pixkah_protossmetales'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class Scale(models.Model):
    _name = 'pixkah_protossmetales.scale'

    name = fields.Char(string="Name")
    short_name = fields.Char(string="Short name", required=True, size=7)
    active = fields.Boolean('Active', default=True)
    address_id = fields.Many2one(
        'res.partner', 'Address')

    max_weight = fields.Integer(string="Maximum weight")
    location = fields.Char(string="Location")
    serie = fields.Char(string="Serie")



class ScaleTicket(models.Model):
    _name = 'pixkah_protossmetales.scale_ticket'

    name = fields.Char(compute='_compute_name', string="Ticket", store=True)

    scale_id = fields.Many2one('pixkah_protossmetales.scale', string="Scale")
    folio = fields.Char(string="Folio", required=True, index=True)

    driver_id = fields.Many2one('hr.employee', string="Driver")    
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    trailer_id = fields.Many2one('fleet.vehicle', string="Trailer")
    first_date = fields.Date(string="Date")
    first_weight = fields.Float(string="Weight (kg)")
    second_date = fields.Date(string="Date")
    second_weight = fields.Float(string="Weight (kg)")
    net_weight = fields.Float(compute='_compute_net_weight', store=True)

    @api.depends('first_weight', 'second_weight')
    def _compute_net_weight(self):
      for record in self:
          record.net_weight = abs(record.second_weight - record.first_weight)

    @api.depends('folio', 'scale_id')
    def _compute_name(self):
      for record in self:
          name = record.scale_id.short_name if record.scale_id else ""
          record.name = name + '-' + record.folio if record.folio else ""


# Inventory
class Picking(models.Model):
    _inherit = "stock.picking"

    @api.onchange('move_lines')
    def _autocompute_done(self):
      for record in self:
        for move in record.move_lines:
          if move.scale_ticket_id:
            move.quantity_done = move.scale_ticket_id.net_weight

class StockMove(models.Model):
    _inherit = "stock.move"

    scale_ticket_id = fields.Many2one('pixkah_protossmetales.scale_ticket', string="Scale Ticket")

'''
    @api.depends('scale_ticket_id')
    def _autocompute_quantity_done(self):
      for move in self:
        if move.scale_ticket_id:
          move.quantity_done = move.scale_ticket_id.net_weight
'''
