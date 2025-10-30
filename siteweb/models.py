from django.db import models

class Loja(models.Model):
    nome = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    imagem = models.TextField(null=True, blank=True)
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
