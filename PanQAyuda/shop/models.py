from django.db import models
<<<<<<< HEAD

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
=======
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_list_by_category',
                           args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
            return reverse('shop:product_detail',
                           args=[self.id, self.slug])
>>>>>>> Social_login
