from django.db import models
from decimal import Decimal

# Create your models here.
class BaseModel(models.Model):
    fecha_creacion = models.DateTimeField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Indica que no se creará una tabla para este modelo


class Producto(BaseModel):
     nombre = models.CharField(max_length=100) 
     precio = models.DecimalField(max_digits=10, decimal_places=2) 
     descripcion = models.TextField(blank=True, null=True)
     def __str__(self):
         return f'Producto: {self.nombre} (${self.precio})' 
     
class Cliente(BaseModel):
     cedula = models.CharField(primary_key=True, max_length=10)
     nombre = models.CharField(max_length=100)
     apellido = models.CharField(max_length=100)
     direccion = models.CharField(max_length=255)
     def __str__(self):
         return f'Cliente : {self.nombre} {self.apellido} - Cédula : {self.cedula}'
     
class Orden(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_totales(self):
        """
        Calcula el subtotal, el IVA y el total basado en los productos asociados.
        """
        subtotal = sum(producto.precio for producto in self.productos.all())
        iva = subtotal * Decimal('0.12')  # IVA 12%
        total = subtotal + iva
        return subtotal, iva, total

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para calcular y asignar los totales
        únicamente si la orden ya existe en la base de datos.
        """
        if self.pk:  # Solo calcular si ya existe un ID
            subtotal, iva, total = self.calcular_totales()
            self.subtotal = subtotal
            self.iva = iva
            self.total = total

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Orden {self.id or 'Sin ID'} - Cliente: {self.cliente.nombre} - Total: ${self.total}"


	 
	
    
  
		   
