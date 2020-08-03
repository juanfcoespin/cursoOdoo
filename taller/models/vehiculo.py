# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions


class Vehicle(models.Model):
    _name = 'taller.vehiculo'
    _description = 'Gestion Vehiculos Odoo'

    name = fields.Char(string="Name", help="Introduce el nombre", size=20)
    active = fields.Boolean(string="Active", default=True)
    matricula = fields.Char("Placa")
    color = fields.Char("Color", default="")

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         "Nombre Duplicado")
    ]

    @api.constrains('matricula')
    def _check_unique_matricula(self):
        # comprobamos que se unica la matricula
        # el domain hace la funcion del where en la bdd para este caso que
        # cumpla las 2 condiciones
        domain = [
            ('matricula', '=', self.matricula),
            ('id', '!=', self.id)
        ]
        vehiculos = self.search(domain)
        if vehiculos:
            raise exceptions.ValidationError("Matrícula Duplicada")
