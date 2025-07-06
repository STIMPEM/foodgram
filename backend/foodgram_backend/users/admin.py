from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'username',
        'get_full_name',
        'email',
        'get_avatar_preview',
        'get_recipes_count',
        'get_subscriptions_count',
        'get_followers_count',
        'is_staff',
        'is_active',
    )

    search_fields = ('username', 'email')

    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'groups',
    )

    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {
            'fields': ('first_name', 'last_name', 'email', 'avatar')
        }),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups',
                       'user_permissions'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name',
                       'last_name', 'avatar', 'is_staff',
                       'is_superuser', 'groups',
                       'user_permissions'),
        }),
    )

    @admin.display(description='ФИО')
    def get_full_name(self, user):
        return f'{user.first_name} {user.last_name}'

    @admin.display(description='Аватар')
    def get_avatar_preview(self, user):
        if user.avatar:
            return mark_safe(f'<img src="{user.avatar.url}" width="40" height="40" style="object-fit:cover; border-radius:50%;" />')
        return '-'

    @admin.display(description='Рецептов')
    def get_recipes_count(self, user):
        return user.recipes.count()

    @admin.display(description='Подписок')
    def get_subscriptions_count(self, user):
        return user.subscriptions.count()

    @admin.display(description='Подписчиков')
    def get_followers_count(self, user):
        return user.subscribers.count()