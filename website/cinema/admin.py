from django.contrib import admin

from cinema.models import Rede, Cinema, Rede, Filme, Temporada, Sala, Sessao, Horario

class HorarioInline(admin.TabularInline):
    model = Horario

    
class TemporadaAdmin(admin.ModelAdmin):
    inlines = [HorarioInline, ]


class SalaInline(admin.TabularInline):
    model = Sala


class CinemaAdmin(admin.ModelAdmin):
    inlines = [SalaInline, ]

admin.site.register(Rede)
admin.site.register(Cinema, CinemaAdmin)
admin.site.register(Filme)
admin.site.register(Temporada, TemporadaAdmin)
admin.site.register(Sessao)

