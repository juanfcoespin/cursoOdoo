# -*- coding: utf-8 -*-

from odoo import models, fields


class Vehicle(models.Model):
    _name = 'taller.vehiculo'
    _description = 'Gestion Vehiculos Odoo'

    name = fields.Char(string="Name", help="Introduce el nombre", size=20)
    active = fields.Boolean(string="Active", default=True)
    matricula= fields.Char("Placa")
    propietario = fields.Char("Dueño")
    color = fields.Char("Color", default="")


