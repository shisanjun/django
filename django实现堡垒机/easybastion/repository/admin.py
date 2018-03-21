from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from repository import models

class IDCAdmin(admin.ModelAdmin):
    list_display = ("name",)

class HostAdmin(admin.ModelAdmin):
    list_display = ("hostname","ip_addr","port","idc","enabled")

class HostGroupAdmin(admin.ModelAdmin):
    list_display = ("name",)

class RemoteUserAdmin(admin.ModelAdmin):
    list_display = ("username","auth_type","password")


class BindUserHostsAdmin(admin.ModelAdmin):
    list_display = ("host","host_user")


class TaskAdmin(admin.ModelAdmin):
    list_display = ("id","user","task_type","content","c_time")
    fields = ("user","task_type","content",)

class TaskLogDetailAdmin(admin.ModelAdmin):
    list_display = ("id","task","bind_host","result","status","c_time","end_time")

    # def show_bind_host(self):
    #     return "%s %s" %("bind_host.host.ip_addr","bind_host.user_host.username")
    #
    # show_bind_host.short_description = "bind host"

class RoleAdmin(admin.ModelAdmin):
    list_display = ("name",)

class MenuOneAdmin(admin.ModelAdmin):
    list_display = ("name",)

class MenuTwoAdmin(admin.ModelAdmin):
    list_display = ("name","url_type","url_path","enable","menu_one")

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码 confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ("用户和密码", {'fields': ('email', 'password')}),
        ('个人信息', {'fields': ('name',)}),
        ('权限信息', {'fields': ('is_admin',"is_active")}),
        ('主机信息', {'fields': ('bind_host',"bind_group")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('bind_host',"bind_group")

# Now register the new UserAdmin...
admin.site.register(models.UserProfile, UserAdmin)
admin.site.register(models.IDC, IDCAdmin)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.HostGroup, HostGroupAdmin)
admin.site.register(models.RemoteUser, RemoteUserAdmin)
admin.site.register(models.BindUserHosts, BindUserHostsAdmin)
admin.site.register(models.Tasks, TaskAdmin)
admin.site.register(models.TaskLogDetail, TaskLogDetailAdmin)
admin.site.register(models.Role, RoleAdmin)
admin.site.register(models.MenuOne, MenuOneAdmin)
admin.site.register(models.MenuTwo, MenuTwoAdmin)