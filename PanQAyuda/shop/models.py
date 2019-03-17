from django.db import models

# Create your models here.
class Categoria(models.Model):
	id_categoria = models.IntegerField(db_index=True)
	nombre_categoria = models.CharField(max_length=200)
	descripcion_categoria = models.TextField(blank=True)
	slug = models.SlugField(max_length=200, unique=True)
	
	class Meta:
		ordering = ('nombre_categoria', 'id_categoria',)
		verbose_name = 'Categoría'
		verbose_name_plural = 'Categorías'
	
	def __str__(self):
		return self.nombre_categoria

class Producto(models.Model):
	id_producto = models.IntegerField(db_index=True)
	nombre_producto = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	descripcion = models.TextField(blank=True)
	id_categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)
	imagen = models.ImageField(upload_to='productos/%Y/%m/%d', blank=True)
	precio = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.IntegerField()
	disponible = models.BooleanField(default=True)
	eliminado = models.BooleanField(default=False)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('id_producto',)

	def __str__(self):
		return self.nombre_producto