from django import template

register = template.Library()

@register.filter(name='formata_moeda')
def formata_moeda(value):
    try:
        valor = float(value)
        return f"{valor:.2f}".replace('.', ',')
    except (ValueError, TypeError):
        return value
