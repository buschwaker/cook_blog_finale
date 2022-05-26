from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from mptt.admin import MPTTModelAdmin

from . import models


class RecipeInline(admin.StackedInline):
    model = models.Recipe
    extra = 1


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "author", "category", "create_at", "id"]
    inlines = [RecipeInline]
    save_as = True
    save_on_top = True


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ["name", "prep_time", "cook_time", "post"]


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "website", "created_at", "id"]


@admin.register(models.MyUser)
class MyUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'avatar')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'email', 'get_image', 'is_staff')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.avatar.url} width="50" height="50">')


admin.site.register(models.Category, MPTTModelAdmin)
admin.site.register(models.Tag)
