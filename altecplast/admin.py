from django.contrib import admin
from django import forms
from .models import Supplier, Client, Waste_client, Weighing


class WeighingAdminForm(forms.ModelForm):
    class Meta:
        model = Weighing
        fields = '__all__'
        widgets = {
            'weighing_number': forms.TextInput(attrs={'size': '20'}),
            'transporter': forms.TextInput(attrs={'size': '20'}),
            'origin': forms.TextInput(attrs={'size': '20'}),
            'vehicle_type': forms.TextInput(attrs={'size': '20'}),
            'license_plate': forms.TextInput(attrs={'size': '15'}),
            'product': forms.TextInput(attrs={'size': '20'}),
            'product_type': forms.TextInput(attrs={'size': '20'}),
            'form': forms.TextInput(attrs={'size': '15'}),
            'color_quality': forms.TextInput(attrs={'size': '15'}),
            'packaging': forms.TextInput(attrs={'size': '15'}),
        }


class SupplierAdminForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = '__all__'
        widgets = {
            'company_name': forms.TextInput(attrs={'size': '30'}),
            'default_transporter': forms.TextInput(attrs={'size': '20'}),
            'default_origin': forms.TextInput(attrs={'size': '20'}),
            'default_vehicle_type': forms.Select(attrs={'style': 'width: auto;'}),
            'default_license_plate': forms.TextInput(attrs={'size': '15'}),
            'default_product': forms.Select(attrs={'style': 'width: auto;'}),
            'default_product_type': forms.Select(attrs={'style': 'width: auto;'}),
            'default_form': forms.Select(attrs={'style': 'width: auto;'}),
            'default_color_quality': forms.Select(attrs={'style': 'width: auto;'}),
            'default_packaging': forms.Select(attrs={'style': 'width: auto;'}),
        }


class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'company_name': forms.TextInput(attrs={'size': '30'}),
            'default_transporter': forms.TextInput(attrs={'size': '20'}),
            'default_vehicle_type': forms.Select(attrs={'style': 'width: auto;'}),
            'default_license_plate': forms.TextInput(attrs={'size': '15'}),
            'default_product': forms.Select(attrs={'style': 'width: auto;'}),
            'default_product_type': forms.Select(attrs={'style': 'width: auto;'}),
            'default_form': forms.Select(attrs={'style': 'width: auto;'}),
            'default_color_quality': forms.Select(attrs={'style': 'width: auto;'}),
            'default_packaging': forms.Select(attrs={'style': 'width: auto;'}),
        }


class WasteClientAdminForm(forms.ModelForm):
    class Meta:
        model = Waste_client
        fields = '__all__'
        widgets = {
            'company_name': forms.TextInput(attrs={'size': '30'}),
            'default_transporter': forms.TextInput(attrs={'size': '20'}),
            'default_vehicle_type': forms.Select(attrs={'style': 'width: auto;'}),
            'default_license_plate': forms.TextInput(attrs={'size': '15'}),
            'default_product': forms.Select(attrs={'style': 'width: auto;'}),
            'default_product_type': forms.Select(attrs={'style': 'width: auto;'}),
            'default_form': forms.Select(attrs={'style': 'width: auto;'}),
            'default_color_quality': forms.Select(attrs={'style': 'width: auto;'}),
            'default_packaging': forms.Select(attrs={'style': 'width: auto;'}),
        }


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    form = SupplierAdminForm
    list_display = ['company_name', 'default_transporter', 'default_product']
    search_fields = ['company_name']
    verbose_name = "Fournisseur"
    verbose_name_plural = "Fournisseurs"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts.verbose_name = "Fournisseur"
        self.opts.verbose_name_plural = "Fournisseurs"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        field_labels = {
            'company_name': 'Nom de l\'Entreprise',
            'default_transporter': 'Transporteur par Défaut',
            'default_origin': 'Origine par Défaut',
            'default_vehicle_type': 'Type de Véhicule par Défaut',
            'default_license_plate': 'Plaque d\'Immatriculation par Défaut',
            'default_product': 'Produit par Défaut',
            'default_product_type': 'Type de Produit par Défaut',
            'default_form': 'Forme par Défaut',
            'default_color_quality': 'Couleur/Qualité par Défaut',
            'default_packaging': 'conditionnement par Défaut'
        }
        for field_name, label in field_labels.items():
            if field_name in form.base_fields:
                form.base_fields[field_name].label = label
        return form


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    list_display = ['company_name', 'default_transporter', 'default_product']
    search_fields = ['company_name']
    verbose_name = "Client"
    verbose_name_plural = "Clients"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts.verbose_name = "Client"
        self.opts.verbose_name_plural = "Clients"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        field_labels = {
            'company_name': 'Nom de l\'Entreprise',
            'default_transporter': 'Transporteur par Défaut',
            'default_vehicle_type': 'Type de Véhicule par Défaut',
            'default_license_plate': 'Plaque d\'Immatriculation par Défaut',
            'default_product': 'Produit par Défaut',
            'default_product_type': 'Type de Produit par Défaut',
            'default_form': 'Forme par Défaut',
            'default_color_quality': 'Couleur/Qualité par Défaut',
            'default_packaging': 'conditionnement par Défaut'
        }
        for field_name, label in field_labels.items():
            if field_name in form.base_fields:
                form.base_fields[field_name].label = label
        return form


@admin.register(Waste_client)
class WasteClientAdmin(admin.ModelAdmin):
    form = WasteClientAdminForm
    list_display = ['company_name', 'default_transporter', 'default_product']
    search_fields = ['company_name']
    verbose_name = "Client Déchet"
    verbose_name_plural = "Clients Déchets"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts.verbose_name = "Client Déchet"
        self.opts.verbose_name_plural = "Clients Déchets"

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        field_labels = {
            'company_name': 'Nom de l\'Entreprise',
            'default_transporter': 'Transporteur par Défaut',
            'default_vehicle_type': 'Type de Véhicule par Défaut',
            'default_license_plate': 'Plaque d\'Immatriculation par Défaut',
            'default_product': 'Produit par Défaut',
            'default_product_type': 'Type de Produit par Défaut',
            'default_form': 'Forme par Défaut',
            'default_color_quality': 'Couleur/Qualité par Défaut',
            'default_packaging': 'conditionnement par Défaut'
        }
        for field_name, label in field_labels.items():
            if field_name in form.base_fields:
                form.base_fields[field_name].label = label
        return form


@admin.register(Weighing)
class WeighingAdmin(admin.ModelAdmin):
    form = WeighingAdminForm
    list_display = ['weighing_number', 'weighing_date', 'weighing_hours', 'weighing_type', 'transporter', 'gross_weight_kg', 'tare_weight', 'net_weight_2_kg', 'product']
    list_filter = ['weighing_date', 'weighing_type', 'company', 'company_non_referenced']
    search_fields = ['weighing_number', 'company__company_name']
    date_hierarchy = 'weighing_date'
    list_per_page = 50
    verbose_name = "Pesée"
    verbose_name_plural = "Pesées"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.opts.verbose_name = "Pesée"
        self.opts.verbose_name_plural = "Pesées"
    
    # Configuration pour afficher tous les champs sur une seule page
    fieldsets = (
        ('Informations de Base', {
            'fields': (('weighing_date', 'weighing_hours'), ('weighing_type', 'weighing_number'), ('company', 'company_non_referenced')),
            'classes': ('collapse',)
        }),
        ('Transport', {
            'fields': (('transporter', 'origin'), ('vehicle_type', 'license_plate')),
            'classes': ('collapse',)
        }),
        ('Poids', {
            'fields': (('gross_weight_kg', 'tare_weight', 'net_weight_1_kg'),
                      ('deduction_amount', 'deduction_type', 'net_weight_2_kg')),
            'classes': ('collapse',)
        }),
        ('Produit', {
            'fields': (('product', 'product_type'), ('form', 'color_quality'),
                      ('packaging', 'packaging_quantity')),
            'classes': ('collapse',)
        }),
    )

    # Traduction des noms de champs
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Traductions des labels des champs
        field_labels = {
            'weighing_number': 'Numéro de Pesée',
            'weighing_date': 'Date de Pesée',
            'weighing_hours': 'Heure de Pesée',
            'weighing_type': 'Type de Pesée',
            'company': 'Entreprise',
            'company_non_referenced': 'Entreprise Non Référencée',
            'transporter': 'Transporteur',
            'origin': 'Origine',
            'vehicle_type': 'Type de Véhicule',
            'license_plate': 'Plaque d\'Immatriculation',
            'gross_weight_kg': 'Poids Brut (Kg)',
            'tare_weight': 'Tare (Kg)',
            'net_weight_1_kg': 'Poids Net 1 (Kg)',
            'deduction_amount': 'Montant de Déduction',
            'deduction_type': 'Type de Déduction',
            'net_weight_2_kg': 'Poids Net 2 (Kg)',
            'product': 'Produit',
            'product_type': 'Type de Produit',
            'form': 'Forme',
            'color_quality': 'Couleur/Qualité',
            'packaging': 'Emballage',
            'packaging_quantity': 'Quantité d\'Emballage',
            'client': 'Client',
            'waste_client': 'Client Déchet'
        }

        for field_name, label in field_labels.items():
            if field_name in form.base_fields:
                form.base_fields[field_name].label = label

        return form
    
    readonly_fields = ['weighing_date', 'weighing_hours', 'net_weight_1_kg', 'net_weight_2_kg']