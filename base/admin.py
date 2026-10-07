from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Person, Property, Attribute, City


# ---------- Person ----------
@admin.register(Person)
class PersonAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'phone',
        'gender', 'external_id', 'is_staff', 'is_active',
    )
    list_filter = ('gender', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'phone', 'external_id')
    ordering = ('-date_joined',)

    # Add your custom fields to the edit form
    fieldsets = UserAdmin.fieldsets + (
        (
            'اطلاعات تکمیلی',
            {
                'fields': ('phone', 'gender', 'external_id'),
            },
        ),
    )

    # Add your custom fields to the "create user" form
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            'اطلاعات تکمیلی',
            {
                'fields': ('phone', 'gender', 'external_id'),
            },
        ),
    )


# ---------- City ----------
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    ordering = ('title',)


# ---------- Attribute ----------
@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_included')
    list_filter = ('is_included',)
    list_editable = ('is_included',)
    search_fields = ('title',)
    ordering = ('title',)


# ---------- Property ----------
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'type_display', 'deal_type_display',
        'city', 'area', 'rooms', 'price_display',
        'parking', 'created_at',
    )
    list_filter = (
        'type', 'deal_type', 'parking',
        'city', 'created_at',
        'Attributes',
    )
    search_fields = ('title', 'rooms', 'backyard', 'city__title')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    filter_horizontal = ('Attributes',)  # nicer M2M widget

    # Use raw_id_fields for large datasets, but for small ones a dropdown is fine
    # raw_id_fields = ('city',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (
            'اطلاعات اصلی',
            {
                'fields': (
                    'title',
                    'type',
                    'deal_type',
                    'price',
                ),
            },
        ),
        (
            'مشخصات ملک',
            {
                'fields': (
                    'area',
                    'rooms',
                    'parking',
                    'backyard',
                    'city',
                ),
            },
        ),
        (
            'ویژگی‌ها',
            {
                'fields': ('Attributes',),
            },
        ),
        (
            'تاریخ‌ها',
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
            },
        ),
    )

    # ---------- Custom columns with Persian formatting ----------

    @admin.display(description='نوع ملک', ordering='type')
    def type_display(self, obj):
        return obj.get_type_display()

    @admin.display(description='نوع معامله', ordering='deal_type')
    def deal_type_display(self, obj):
        return obj.get_deal_type_display()

    @admin.display(description='قیمت (تومان)', ordering='price')
    def price_display(self, obj):
        if obj.price is None:
            return '-'
        # Format with thousand separators and convert to Persian digits
        return self._to_persian(f'{obj.price:,}')

    # ---------- Helper ----------

    @staticmethod
    def _to_persian(text):
        return str(text).translate(
            str.maketrans('0123456789,', '۰۱۲۳۴۵۶۷۸۹٬')
        )


# ---------- Optional: customize admin site branding ----------
admin.site.site_header = 'پنل مدیریت املاک'
admin.site.site_title = 'مدیریت املاک'
admin.site.index_title = 'به پنل مدیریت خوش آمدید'