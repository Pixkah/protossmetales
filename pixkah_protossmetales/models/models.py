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

    scale_id = fields.Many2one('pixkah_protossmetales.scale', string="Scale")
    picking_id = fields.Many2one('stock.picking', string='Transfer reference', index=True)

    name = fields.Char(compute='_compute_name')
    folio = fields.Char(string="folio", required=True)
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

    @api.multi
    def _compute_name(self):
      for record in self:
        record.name = record.scale_id.short_name + '-' + record.folio


class Picking(models.Model):
    _inherit = "stock.picking"

    scale_tickets = fields.One2many('pixkah_protossmetales.scale_ticket', 'picking_id', string="Scale Tickets")
    scale_ticket_id = fields.Many2one('pixkah_protossmetales.scale_ticket', string="Scale Ticket")
    driver_id = fields.Many2one('hr.employee', string="Driver")