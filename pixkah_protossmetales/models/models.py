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

    name = fields.Char(compute='_compute_name', string="Ticket")

    scale_id = fields.Many2one('pixkah_protossmetales.scale', string="Scale")
    folio = fields.Char(string="Folio", required=True)

    picking_id = fields.Many2one('stock.picking', string='Transfer reference', index=True)    
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle")
    first_date = fields.Date(string="Date")
    first_weight = fields.Float(string="Weight (kg)")
    second_date = fields.Date(string="Date")
    second_weight = fields.Float(string="Weight (kg)")
    net_weight = fields.Float(compute='_compute_net_weight')

    @api.multi
    def _compute_net_weight(self):
      for record in self:
          record.net_weight = abs(record.second_weight - record.first_weight)

    @api.onchange('first_weight', 'second_weight')
    def _autocompute_net_weight(self):
      self._compute_net_weight()

    @api.depends('folio', 'scale_id')
    def _autocompute_name(self):
      self._compute_name()

    @api.multi
    def _compute_name(self):
      for record in self:
          name = record.scale_id.short_name if record.scale_id else ""
          record.name = name + '-' + record.folio if record.folio else ""

class Picking(models.Model):
    _inherit = "stock.picking"

    scale_tickets = fields.One2many('pixkah_protossmetales.scale_ticket', 'picking_id', string="Scale Tickets")
    scale_ticket_id = fields.Many2one('pixkah_protossmetales.scale_ticket', string="Scale Ticket")
    driver_id = fields.Many2one('hr.employee', string="Driver")

    @api.onchange('scale_ticket_id')
    def _autocompute_done(self):
      for record in self:
        if record.scale_ticket_id:
          for move in record.move_lines:
            move.quantity_done = record.scale_ticket_id.net_weight