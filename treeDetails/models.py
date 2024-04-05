from django.db import models

# Create your models here.
class TreeSpeciesDetail(models.Model):
    specie_name = models.CharField(max_length=20)
    # specie_info = models.TextField()
    specie_growth_factor = models.DecimalField(max_digits=3, decimal_places=2)
