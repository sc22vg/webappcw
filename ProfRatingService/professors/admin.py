from django.contrib import admin
from .models import Professor, Module, Rating, Iteration

admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(Rating)
admin.site.register(Iteration)
