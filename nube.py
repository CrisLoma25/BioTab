from pyairtable.orm import Model
from pyairtable.orm import fields

class Usuario(Model):
    nombre = fields.TextField("nombre")
    apellidopaterno = fields.TextField("apellidopaterno")
    apellidomaterno = fields.TextField("apellidomaterno")
    usuario = fields.TextField("usuario")
    contra = fields.TextField("contra")
    admin = fields.CheckboxField("admin")

    class Meta:
        api_key = "patbC1w6IrUgJ62XA.9a86c75769727f01c30521aebfa00bf71285966c7b3598901dc8f290efb67ed5"
        base_id = "appOuhcRRitcIrg8J"
        table_name = "usuarios"

class Bioenergia(Model):
    cultivo = fields.TextField("cultivo")
    parte = fields.SelectField("parte")
    cantidad = fields.FloatField("cantidad")
    area = fields.FloatField("area")
    humedad = fields.FloatField("humedad")
    municipio = fields.SelectField("municipio")
    latitud = fields.FloatField("latitud")
    longitud= fields.FloatField("longitud")
    
    class Meta:
        api_key = "patbC1w6IrUgJ62XA.9a86c75769727f01c30521aebfa00bf71285966c7b3598901dc8f290efb67ed5"
        base_id = "appOuhcRRitcIrg8J"
        table_name = "bioenergia" 
