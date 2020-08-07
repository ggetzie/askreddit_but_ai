from django.contrib import admin

from main.models import GeneratedQ, About

@admin.register(GeneratedQ)
class GeneratedQAdmin(admin.ModelAdmin):
    date_hierarchy = "displayed"
    list_display = ("text", "votes")
    list_filter = ("tweeted",)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    fields = ["text", "published"]
    