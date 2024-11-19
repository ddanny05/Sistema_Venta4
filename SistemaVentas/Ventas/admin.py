from django.contrib import admin
from .models import Cliente,Orden,Producto

# Register your models here.
#admin.site.register(Producto)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'cedula', 'direccion', 'fecha_creacion')
    search_fields = ('nombre', 'apellido', 'cedula')

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'subtotal', 'iva', 'total', 'fecha_creacion')
    filter_horizontal = ('productos',)
    readonly_fields = ('subtotal', 'iva', 'total')

    def save_model(self, request, obj, form, change):
        """
        Calcula los totales antes de guardar la orden.
        """
        obj.save()

    def save_related(self, request, form, formsets, change):
        """
        Calcula los totales después de relacionar los productos.
        """
        super().save_related(request, form, formsets, change)
        form.instance.subtotal, form.instance.iva, form.instance.total = form.instance.calcular_totales()
        form.instance.save(update_fields=['subtotal', 'iva', 'total'])