from typing import Any

from debug_toolbar.utils import SafeString
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.utils.safestring import mark_safe

from .models import Category, Women


class MarriedFilter(admin.SimpleListFilter):
    title = "Статус женщин"
    parameter_name = "status"
    
    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("married", "Замужем"),
            ("single", "Не замужем"),
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "married":
             return queryset.filter(husband__isnull=False)
        if self.value() == "single":
             return queryset.filter(husband__isnull=True)
    
@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    fields = ["title", "content", "photo", "post_photo", "slug", "cat", "husband", "tags"]
    # exclude = ["tags", "is_pulished"]
    readonly_fields = ["post_photo"]
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("id", "title", "post_photo", "time_create", "is_published", "cat", "brief_info")
    list_display_links = ("title", )
    ordering = ("-time_create", "title")
    list_editable = ("is_published", )
    list_per_page = 5
    actions = ("set_published", "set_draft")
    search_fields = ("title", "cat__name")
    list_filter = (MarriedFilter, "cat__name", "is_published")
    save_on_top = True
    
    @admin.display(description="Краткое описание")
    def brief_info(self, women: Women) -> str:
        return f"Описание {len(women.content)} символов."
    
    @admin.display(description="Фото")
    def post_photo(self, women: Women) -> SafeString:
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"
    
    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"Изменено {count} записей.", messages.WARNING)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")