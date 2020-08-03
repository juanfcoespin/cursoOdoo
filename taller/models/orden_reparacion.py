# -*- coding: utf-8 -*-

from odoo import models, fields, api


class OrdenReparacion(models.Model):
    _name = 'taller.orden.reparacion'
    _description = 'Gestion Orden Reparacion'

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(
        string="Name",
        help="Introduce el nombre",
        default="OR_"
    )
    partner_id = fields.Many2one("res.partner", string="Cliente")
    raparacion_line_ids = fields.One2many(
        comodel_name="taller.orden.reparacion.linea",
        inverse_name="reparacion_id",
        string="Lineas Reparación"
    )

    # vals son todos los atributos de la clase
    # que se van a insertar en la tabla

    @api.model
    def create(self, vals):
        # inserta la secuencia en el campo name de la tabla
        seq_name = self.env['ir.sequence'].next_by_code(
            'orden.reparacion') or 'New'
        vals.update(name=seq_name)

        # la funcion create hace un insert en la tabla
        res = super(OrdenReparacion, self).create(vals)
        return res

    class OrdenReparacionLinea(models.Model):
        _name = 'taller.orden.reparacion.linea'
        _description = 'Gestion de lineas de reparacion'

        active = fields.Boolean(string="Active", default=True)
        vehicle_id = fields.Many2one("taller.vehiculo", string="Vehículo")
        descripcion = fields.Text(
            string="Descripción",
            help="Introduce el detalle del trabajo en el vehículo",

        )
        reparacion_id = fields.Many2one("taller.orden.reparacion")
        




