# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

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

    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(compute='_compute_name', string="Ticket", store=True)

    scale_id = fields.Many2one('pixkah_protossmetales.scale', string="Scale")
    folio = fields.Char(string="Folio", required=True, index=True)

    # Inventory
    stock_move = fields.Many2one('stock.move', string="Stock Move")
    
    # Ticket status regarding stock movements
    move_status = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('audited', 'Audited'),
      ],
      string="Status",
      copy=False, index=True,
      default="new")

    # Invoicing
    invoice_line = fields.Many2one('account.invoice.line', string="Invoice Line")

    # Ticket status regarding invoicing
    invoice_status = fields.Selection([
        ('new', 'New'),
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('paid', 'Paid'),
        ('audited', 'Audited'),
      ],
      string="Status",
      copy=False, index=True,
      default="new")

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

class StockMove(models.Model):
    _inherit = "stock.move"

    scale_ticket = fields.Many2one('pixkah_protossmetales.scale_ticket',
      string="Scale Ticket"
    )

class Picking(models.Model):
    _inherit = "stock.picking"

    @api.onchange('move_lines')
    def _autocompute_done_quantity_from_ticket(self):
      for record in self:
        for move in record.move_lines:
          if move.scale_ticket:
            move.quantity_done = move.scale_ticket.net_weight
            self._cr.execute("""
              update
                pixkah_protossmetales_scale_ticket
              set
                move_status='draft',
                stock_move=%s
              where
                id=%s
            """, [move.id, move.scale_ticket.id])

    @api.multi
    def button_validate(self):
      res = super(Picking, self).button_validate()

      # Update ticket status
      for record in self:
        for move in record.move_lines:
          if move.scale_ticket:
            move.quantity_done = move.scale_ticket.net_weight
            self._cr.execute("""
              update
                pixkah_protossmetales_scale_ticket
              set
                move_status='assigned',
                stock_move=%s
              where
                id=%s
            """, [move.id, move.scale_ticket.id])
      return res


# Invoicing

class AccountInvoiceLine(models.Model):
  _inherit = "account.invoice.line"

  scale_ticket = fields.Many2one('pixkah_protossmetales.scale_ticket',
    string="Scale Ticket"
  )

  merma_porcentaje = fields.Float(string="Merma %")
  merma_kg = fields.Float(string="Merma (kg)")


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.onchange('invoice_line_ids')
    def _compute_line_quantity_from_ticket(self):
      for record in self:
        for line in record.invoice_line_ids:
          if line.scale_ticket:
            quantity = line.scale_ticket.net_weight
            quantity = quantity - quantity*(line.merma_porcentaje/100)
            quantity = quantity - line.merma_kg
            line.quantity = quantity
            self._cr.execute("""
                update
                  pixkah_protossmetales_scale_ticket
                set
                  invoice_status='draft'
                where
                  id=%s
              """, [line.scale_ticket.id])

    @api.multi
    def invoice_validate(self):
      res = super(AccountInvoice, self).invoice_validate()

      # Update ticket status
      for line in self.invoice_line_ids:
        if line.scale_ticket:
          line.quantity = line.scale_ticket.net_weight
          self._cr.execute("""
            update
              pixkah_protossmetales_scale_ticket
            set
              invoice_status='assigned',
              invoice_line=%s
            where
              id=%s
          """, [line.id, line.scale_ticket.id])
      return res