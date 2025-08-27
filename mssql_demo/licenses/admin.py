# from django.contrib import admin
# from .models_license import Licenseupdation, Updationtype, License, Endorsenumber, Licensevehicle, Vehicletype

# @admin.register(Vehicletype)
# class VehicletypeAdmin(admin.ModelAdmin):
#     list_display = ['vehicletypeid', 'description']
#     search_fields = ['description', 'vehicletypeid']
#     ordering = ['vehicletypeid']
#     list_per_page = 20

# @admin.register(Licensevehicle)
# class LicensevehicleAdmin(admin.ModelAdmin):
#     list_display = ['licenseno', 'vehicletype', 'status', 'get_vehicle_description']
#     list_filter = ['vehicletype', 'status']
#     search_fields = ['licenseno', 'vehicletype__description']
#     ordering = ['licenseno']
#     list_per_page = 20
    
#     def get_vehicle_description(self, obj):
#         return obj.vehicletype.description if obj.vehicletype else 'N/A'
#     get_vehicle_description.short_description = 'Vehicle Description'
#     get_vehicle_description.admin_order_field = 'vehicletype__description'

# @admin.register(Updationtype)
# class UpdationtypeAdmin(admin.ModelAdmin):
#     list_display = ['updationtypeno', 'description']
#     search_fields = ['description']
#     ordering = ['updationtypeno']

# @admin.register(Licenseupdation)
# class LicenseupdationAdmin(admin.ModelAdmin):
#     list_display = ['serialno', 'number', 'updationtypeno', 'status', 'type', 'computerno']
#     list_filter = ['updationtypeno', 'status', 'type']
#     search_fields = ['number', 'computerno', 'enterby']
#     ordering = ['-serialno']
    
#     def get_queryset(self, request):
#         # Use select_related to optimize database queries
#         return super().get_queryset(request).select_related('updationtypeno')

# @admin.register(License)
# class LicenseAdmin(admin.ModelAdmin):
#     list_display = ['serialno', 'licenseno', 'name', 'fathername', 'cnic', 'issuedate', 'expirydate', 'verified']
#     list_filter = ['verified', 'enable', 'issuedate', 'expirydate']
#     search_fields = ['licenseno', 'name', 'fathername', 'cnic']
#     ordering = ['-serialno']

# @admin.register(Endorsenumber)
# class EndorsenumberAdmin(admin.ModelAdmin):
#     list_display = ['serialno', 'number', 'status']
#     list_filter = ['status']
#     search_fields = ['number']
#     ordering = ['-serialno']
