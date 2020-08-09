# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
import logging
import base64
import csv
import io
from odoo import models, fields, api, exceptions

# para que se muestre en el log lo que se está haciendo
# __name__ es una variable de muestra el nombre de la función desde la que se envoca
_logger = logging.getLogger(__name__)


class MrpImportBom(models.TransientModel):
    _name = "mrp.import.bom.wizard"

    file_type = fields.Selection(
        selection=[
            ('csv', 'Archivo Csv')
        ],
        default='csv',
        required=True,
        string="Tipo de Archivo"
    )
    product_id = fields.Many2one(
        'product.template',
        string='Producto'
    )
    routing_id = fields.Many2one(
        'mrp.routing',
        string='Ruta'
    )
    file_data = fields.Binary('Archivo', required=True)

    # carga por defecto en el product_id el producto desde el cual se lanza el wizard
    @api.model
    def default_get(self, fields_list):
        res = super(MrpImportBom, self).default_get(fields_list)
        if self._context.get("active_id"):
            res.update(product_id=self._context.get("active_id"))
        return res

    def import_bom(self):
        bom = self.env['mrp.bom']
        product = self.env['product.product']

        try:
            decoded_data = base64.decodebytes(self.file_data). \
                replace(b'\xef\xbb\xbf', b'').replace(b';', b',')
            f = io.TextIOWrapper(io.BytesIO(decoded_data), encoding='utf-8')
            reader = csv.DictReader(f, delimiter=',')
        except Exception as err:
            raise ValidationError(
                'Error: {}  El archivo debe de ser del tipo {}'.format(err, self.file_type.upper())
            )
        bom_ids = []
        for row in reader:
            cols = dict(row)

            product_code = cols.get('Code', False)
            cantidad = cols.get('Cantidad', False)

            if not product_code or not cantidad:
                raise ValidationError(
                    'El archivo no contiene una lista de materiales válida')

            pro = product.search([('default_code', '=', product_code)])
            if pro:
                # se añade el registro
                '''
                    bom_ids es un campo del tipo one2many
                    (0,4) => 
                        0 es un registro nuevo que se va a crear; 
                        4 para modificar cuando ya existe una lista de items,
                          ya no recibe una tupla sino solo los ids
                      
                    0 => entiende como un false para este caso revisar:
                
                https://www.odoo.com/documentation/13.0/reference/orm.html#related-fields
                '''
                bom_ids.append((
                    0, 0,
                    {
                        'product_id': pro.id,
                        'product_qty': cantidad,
                        'product_uom_id': pro.uom_id.id
                    }
                ))
            else:
                raise ValidationError(
                    'El producto con codigo {} no existe'.format(
                        product_code)
                )
        # fin for
        if bom_ids:
            bom_to_create = {
                # 'product_id': self.product_id.product_variant_id.id,
                'product_tmpl_id': self.product_id.id,
                'product_uom_id': self.product_id.uom_id.id,
                'product_qty': 1.0,
                'routing_id': self.routing_id.id,
                'type': 'normal',
                'ready_to_produce': 'asap',
                'bom_line_ids': bom_ids
            }

        else:
            raise ValidationError(
                'El archivo csv proporcionado no ha generado'
                ' ninguna lista de materiales'
            )
        res = bom.create(bom_to_create)
        _logger.info('Se ha creado la lista de materiales {} para el producto {}'
                     .format(res.id, self.product_id.name))
        return {}
