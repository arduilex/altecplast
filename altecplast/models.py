from django.db import models
from django.utils import timezone
from django.conf import settings
import csv, os


WEIGHING_TYPE_CHOICES = [
    ('referenced_entry', 'Entrée Référencée'),
    ('non_referenced_entry', 'Entrée Non Référencée'),
    ('finished_product_return', 'Retour Produit Fini'),
    ('finished_product_output', 'Sortie Produit Fini'),
    ('waste_output', 'Sortie Déchet'),
    ('merchandise_return', 'Retour Marchandise'),
    ('outsourced_product_output', 'Sortie Produit (sous-traitance)'),
    ('outsourced_product_return', 'Retour Produit (sous-traitance)'),

]

# Choix communs
VEHICLE_TYPE_CHOICES = [
    ('CAMION 10G', 'Camion 10G'),
    ('CAMION 8G', 'Camion 8G'),
    ('CAMION 6G', 'Camion 6G'),
    ('CAMION 5G', 'Camion 5G'),
    ('CAMIONNETTE', 'Camionnette'),
    ('PICK-UP', 'Pick-Up'),
    ('REMORQUE', 'Remorque'),
    ('CONTENEUR', 'Conteneur'),
    ('TRAFFIC', 'Traffic'),
    ('AUTRE', 'Autre'),
]

# Choix spécifiques aux fournisseurs (Entrée référencée)
SUPPLIER_PRODUCT_CHOICES = [
    ('PLASTIQUE', 'Plastique'),
    ('PURGES', 'Purges'),
    ('CARTON', 'Carton'),
    ('BOIS', 'Bois'),
    ('FERREUX', 'Ferreux'),
    ('AUTRE', 'Autre'),
]

SUPPLIER_PRODUCT_TYPE_CHOICES = [
    ('PELD', 'PELD'),
    ('PP', 'PP'),
    ('PET', 'PET'),
    ('PEHD', 'PEHD'),
    ('PS CHOC', 'PS Choc'),
    ('PALETTE', 'Palette'),
    ('BOIS CASSE', 'Bois Cassé'),
    ('ALUMINIUM', 'Aluminium'),
    ('FERRAILLE', 'Ferraille'),
    ('AUTRE', 'Autre'),
]

SUPPLIER_FORM_CHOICES = [
    ('BRUT', 'Brut'),
    ('DECHET', 'Déchet'),
    ('BROYE', 'Broyé'),
    ('GRANULES', 'Granulés'),
    ('DENSIFIE', 'Densifié'),
    ('AUTRE', 'Autre'),
]

SUPPLIER_COLOR_QUALITY_CHOICES = [
    ('BEURRE', 'Beurre'),
    ('FRAICH', 'Fraîch'),
    ('SERRE', 'Serre'),
    ('DOUBLE FACE', 'Double Face'),
    ('PAILLAGE', 'Paillage'),
    ('TRIE BLANC', 'Trié Blanc'),
    ('TRIE COULEURS', 'Trié Couleur'),
    ('TRIE BLANC COULEUR', 'Trié Blanc+Couleur'),
    ('POST INDUS PROPRE', 'Post Indus Propre'),
    ('POST INDUS SALE', 'Post Indus Sale'),
    ('DECHARGE', 'Décharge'),
    ('TRIE BLANC+COULEURS', 'Trié (Blanc+couleur)'),
    ('AUTRE', 'Autre'),
]

SUPPLIER_PACKAGING_CHOICES = [
    ('VRAC', 'Vrac'),
    ('BALLE LOCAL', 'Balle Local'),
    ('BALLE IMPORT', 'Balle Import'),
    ('COLIS', 'Colis'),
    ('SAC', 'Sac'),
    ('BIG_BAG', 'Big-bag'),
    ('AUTRE', 'Autre'),
]

# Choix spécifiques aux clients (Sortie produit fini)
CLIENT_PRODUCT_CHOICES = [
    ('PLASTIQUE', 'Plastique'),
    ('PURGES', 'Purges'),
    ('CARTON', 'Carton'),
    ('BOIS', 'Bois'),
    ('FERREUX', 'Ferreux'),
    ('AUTRE', 'Autre'),
]

CLIENT_PRODUCT_TYPE_CHOICES = [
    ('PELD', 'PELD'),
    ('PP', 'PP'),
    ('PET', 'PET'),
    ('PEHD', 'PEHD'),
    ('PS CHOC', 'PS Choc'),
    ('PALETTE', 'Palette'),
    ('BOIS CASSE', 'Bois Cassé'),
    ('ALUMINIUM', 'Aluminium'),
    ('FERRAILLE', 'Ferraille'),
    ('AUTRE', 'Autre'),
]

CLIENT_FORM_CHOICES = [
    ('GRANULES', 'Granulés'),
    ('DENSIFIE', 'Densifié'),
    ('BRUT', 'Brut'),
    ('BROYE', 'Broyé'),
    ('AUTRE', 'Autre'),
]

CLIENT_COLOR_QUALITY_CHOICES = [
    ('BLANC 1ere', 'Blanc 1ère'),
    ('BLANC 2eme', 'Blanc 2eme'),
    ('NOIR', 'Noir'),
    ('BLEU', 'Bleu'),
    ('VERT', 'Vert'),
    ('AUTRE', 'Autre'),
]

CLIENT_PACKAGING_CHOICES = [
    ('BIG-BAG', 'Big-bag'),
    ('SAC', 'Sac'),
    ('VRAC', 'Vrac'),
    ('BALLE', 'Balle'),
    ('COLIS', 'Colis'),
    ('AUTRE', 'Autre'),
]

# Choix spécifiques aux clients déchets (Sortie déchet)
WASTE_CLIENT_VEHICLE_TYPE_CHOICES = [
    ('CAMION', 'Camion'),
    ('CAMION AMPLI', 'Camion Ampli'),
    ('CAMION 10G', 'Camion 10G'),
    ('CAMION 8G', 'Camion 8G'),
    ('CAMION 6G', 'Camion 6G'),
    ('CAMION 5G', 'Camion 5G'),
    ('CAMIONNETTE', 'Camionnette'),
    ('PICK-UP', 'Pick-Up'),
    ('REMORQUE', 'Remorque'),
    ('CONTENEUR', 'Conteneur'),
    ('TRAFFIC', 'Traffic'),
    ('AUTRE', 'Autre'),
]

WASTE_CLIENT_PRODUCT_CHOICES = [
    ('DECHETS', 'Déchet'),
]

WASTE_CLIENT_PRODUCT_TYPE_CHOICES = [
    ('SOLIDE', 'Solide'),
    ('LIQUIDE', 'Liquide'),
    ('BOUE', 'Boue'),
    ('CARTON', 'Carton'),
]

WASTE_CLIENT_FORM_CHOICES = [
    ('BRUT', 'Brut'),
]

WASTE_CLIENT_PACKAGING_CHOICES = [
    ('BENNE', 'Benne'),
    ('CITERNE', 'Citerne'),
]


class Supplier(models.Model):
    company_name = models.TextField()
    default_transporter = models.TextField(blank=True, null=True)
    default_origin = models.TextField(blank=True, null=True)
    default_vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, blank=True, null=True)
    default_license_plate = models.TextField(blank=True, null=True)
    default_product = models.CharField(max_length=20, choices=SUPPLIER_PRODUCT_CHOICES, blank=True, null=True)
    default_product_type = models.CharField(max_length=20, choices=SUPPLIER_PRODUCT_TYPE_CHOICES, blank=True, null=True)
    default_form = models.CharField(max_length=20, choices=SUPPLIER_FORM_CHOICES, blank=True, null=True)
    default_color_quality = models.CharField(max_length=30, choices=SUPPLIER_COLOR_QUALITY_CHOICES, blank=True, null=True)
    default_packaging = models.CharField(max_length=20, choices=SUPPLIER_PACKAGING_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.company_name


class Client(models.Model):
    company_name = models.TextField()
    default_transporter = models.TextField(blank=True, null=True)
    default_vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES, blank=True, null=True)
    default_license_plate = models.TextField(blank=True, null=True)
    default_product = models.CharField(max_length=20, choices=CLIENT_PRODUCT_CHOICES, blank=True, null=True)
    default_product_type = models.CharField(max_length=20, choices=CLIENT_PRODUCT_TYPE_CHOICES, blank=True, null=True)
    default_form = models.CharField(max_length=20, choices=CLIENT_FORM_CHOICES, blank=True, null=True)
    default_color_quality = models.CharField(max_length=20, choices=CLIENT_COLOR_QUALITY_CHOICES, blank=True, null=True)
    default_packaging = models.CharField(max_length=20, choices=CLIENT_PACKAGING_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.company_name


class Waste_client(models.Model):
    company_name = models.TextField()
    default_transporter = models.TextField(blank=True, null=True)
    default_vehicle_type = models.CharField(max_length=20, choices=WASTE_CLIENT_VEHICLE_TYPE_CHOICES, blank=True, null=True)
    default_license_plate = models.TextField(blank=True, null=True)
    default_product = models.CharField(max_length=20, choices=WASTE_CLIENT_PRODUCT_CHOICES, blank=True, null=True)
    default_product_type = models.CharField(max_length=20, choices=WASTE_CLIENT_PRODUCT_TYPE_CHOICES, blank=True, null=True)
    default_form = models.CharField(max_length=20, choices=WASTE_CLIENT_FORM_CHOICES, blank=True, null=True)
    default_color_quality = models.CharField(max_length=20, choices=CLIENT_COLOR_QUALITY_CHOICES, blank=True, null=True)
    default_packaging = models.CharField(max_length=20, choices=WASTE_CLIENT_PACKAGING_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.company_name


class Weighing(models.Model):

    
    DEDUCTION_TYPE_CHOICES = [
        ('%', '%'),
        ('kg', 'kg'),
    ]

    weighing_date = models.DateField(default=timezone.now)
    weighing_hours = models.TimeField(default=timezone.now)
    weighing_type = models.CharField(max_length=50, choices=WEIGHING_TYPE_CHOICES)
    weighing_number = models.TextField()
    company = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    company_non_referenced = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    waste_client = models.ForeignKey(Waste_client, on_delete=models.CASCADE, blank=True, null=True)
    transporter = models.TextField(blank=True, null=True)
    origin = models.TextField(blank=True, null=True)
    vehicle_type = models.TextField(blank=True, null=True)
    license_plate = models.TextField(blank=True, null=True)
    gross_weight_kg = models.IntegerField(default=0)
    tare_weight = models.IntegerField()
    net_weight_1_kg = models.IntegerField(default=0)
    deduction_amount = models.IntegerField(blank=True, null=True)
    deduction_type = models.CharField(max_length=2, choices=DEDUCTION_TYPE_CHOICES, default='%', blank=True)
    net_weight_2_kg = models.IntegerField(default=0)
    product = models.TextField()
    product_type = models.TextField()
    form = models.TextField(blank=True, null=True)
    color_quality = models.TextField(blank=True, null=True)
    packaging = models.TextField(blank=True, null=True)
    packaging_quantity = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.company:
            company_name = self.company.company_name
        elif self.client:
            company_name = self.client.company_name
        elif self.waste_client:
            company_name = self.waste_client.company_name
        else:
            company_name = self.company_non_referenced or "Non référencé"
        return f"{self.weighing_number} - {company_name}"
    
    def save(self, *args, **kwargs):
        # is_new = self._state.adding
        # super().save(*args, **kwargs)
        
        # if is_new:
        self.export_to_csv()
    
    def export_to_csv(self):
        """Exporte cette pesée vers le fichier CSV de façon additive"""
        csv_file_path = getattr(settings, 'WEIGHING_EXPORT_CSV_PATH', 'excel_app_communication/pesee_app_export.csv')
        
        # Créer le dossier parent s'il n'existe pas
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        
        # Vérifier si le fichier existe pour ajouter les en-têtes
        file_exists = os.path.isfile(csv_file_path)
        
        # Déterminer le nom de la compagnie
        if self.company:
            company_name = self.company.company_name
        elif self.client:
            company_name = self.client.company_name
        elif self.waste_client:
            company_name = self.waste_client.company_name
        else:
            company_name = self.company_non_referenced or ""
        
        # Mapper le type de pesée vers le français
        type_mapping = {
            'referenced_entry': 'Entrée référencée',
            'non_referenced_entry': 'Entrée non référencée',
            'finished_product_output': 'Sortie PF',
            'finished_product_return': 'Retour PF',
            'waste_output': 'Sortie déchets',
            'merchandise_return': 'Retour marchandise',
            'outsourced_product_output': 'Sortie produit (sous-traitance)',
            'outsourced_product_return': 'Retour produit (sous-traitance)'
        }
        
        with open(csv_file_path, 'a', newline='', encoding='windows-1256') as csvfile:
            fieldnames = [
                'TYPE DE PESEE', 'DATE', 'HEURE', 'N° PESEE/BL', 'FOURNISSEUR/CLIENT',
                'TRANSPORTEUR', 'IMMAT', 'POIDS BRUT', 'POIDS TARE', 'POIDS NET 1',
                '%TAGE ENLEVE', 'POIDS NET 2', 'TYPE DE VEHICULE', 'ORIGINE',
                'PRODUITS', 'TYPE DE PRODUITS', 'FORME', 'CONDITIONNEMENT',
                'NBRE DE CONDT', 'QUALITE/COULEUR'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
            
            # Écrire les en-têtes seulement si le fichier est nouveau
            if not file_exists:
                writer.writeheader()
            
            # Écrire les données de cette pesée
            writer.writerow({
                'TYPE DE PESEE': type_mapping.get(self.weighing_type, self.weighing_type),
                'DATE': self.weighing_date.strftime('%d/%m/%Y') if self.weighing_date else '',
                'HEURE': self.weighing_hours.strftime('%H:%M:%S') if self.weighing_hours else '',
                'N° PESEE/BL': self.weighing_number,
                'FOURNISSEUR/CLIENT': company_name,
                'TRANSPORTEUR': self.transporter or '',
                'IMMAT': self.license_plate or '',
                'POIDS BRUT': f"{self.gross_weight_kg:,}".replace(',', ' ') if self.gross_weight_kg else '',
                'POIDS TARE': f"{self.tare_weight:,}".replace(',', ' ') if self.tare_weight else '',
                'POIDS NET 1': f"{self.net_weight_1_kg:,}".replace(',', ' ') if self.net_weight_1_kg else '',
                '%TAGE ENLEVE': self.deduction_amount if self.deduction_amount else '',
                'POIDS NET 2': f"{self.net_weight_2_kg:,}".replace(',', ' ') if self.net_weight_2_kg else '',
                'TYPE DE VEHICULE': self.vehicle_type or '',
                'ORIGINE': self.origin or '',
                'PRODUITS': self.product or '',
                'TYPE DE PRODUITS': self.product_type or '',
                'FORME': self.form or '',
                'CONDITIONNEMENT': self.packaging or '',
                'NBRE DE CONDT': self.packaging_quantity if self.packaging_quantity else '',
                'QUALITE/COULEUR': self.color_quality or ''
            })


class Production(models.Model):
    WEATHER_CHOICES = [
        ('soleil', 'Soleil'),
        ('pluie', 'Pluie'),
    ]

    FILLED_BY_CHOICES = [
        ('Nezha', 'Nezha'),
        ('Autre', 'Autre'),
    ]

    MOTIF_CHOICES = [
        ('arr_mp', 'Arrêt MP'),
        ('arr_mce', 'Arrêt Maintenance'),
        ('arr_ntt', 'Arrêt Nettoyage'),
    ]

    # Common fields
    date = models.DateField(default=timezone.now)
    rempli_par = models.CharField(max_length=20, choices=FILLED_BY_CHOICES, blank=True, null=True)
    meteo = models.CharField(max_length=20, choices=WEATHER_CHOICES, blank=True, null=True)

    # Lavage production totals
    lavage_production_totale = models.IntegerField(blank=True, null=True, default=0)

    # Lavage Poste Jour - Colors (Kg)
    lavage_jour_noir_c = models.IntegerField(blank=True, null=True, default=0)
    lavage_jour_noir_nc = models.IntegerField(blank=True, null=True, default=0)
    lavage_jour_blanc_c = models.IntegerField(blank=True, null=True, default=0)
    lavage_jour_blanc_nc = models.IntegerField(blank=True, null=True, default=0)
    lavage_jour_bleu_c = models.IntegerField(blank=True, null=True, default=0)
    lavage_jour_bleu_nc = models.IntegerField(blank=True, null=True, default=0)
    # Lavage Poste Jour - Time fields
    lavage_jour_heure_w_debut = models.TimeField(blank=True, null=True)
    lavage_jour_heure_w_fin = models.TimeField(blank=True, null=True)
    lavage_jour_heure_w_nombre = models.FloatField(blank=True, null=True)
    # Lavage Poste Jour - Heures Arret 1
    lavage_jour_heure_a1_debut = models.TimeField(blank=True, null=True)
    lavage_jour_heure_a1_fin = models.TimeField(blank=True, null=True)
    lavage_jour_heure_a1_nombre = models.FloatField(blank=True, null=True)
    # Lavage Poste Jour - Heures Arret 2
    lavage_jour_heure_a2_debut = models.TimeField(blank=True, null=True)
    lavage_jour_heure_a2_fin = models.TimeField(blank=True, null=True)
    lavage_jour_heure_a2_nombre = models.FloatField(blank=True, null=True)
    # Lavage Poste Jour - Motifs
    lavage_jour_motif_arret1 = models.CharField(max_length=20, choices=MOTIF_CHOICES, blank=True, null=True)
    lavage_jour_motif_arret2 = models.CharField(max_length=20, choices=MOTIF_CHOICES, blank=True, null=True)

    # Lavage Poste Nuit - Colors (Kg)
    lavage_nuit_noir_c = models.IntegerField(blank=True, null=True, default=0)
    lavage_nuit_noir_nc = models.IntegerField(blank=True, null=True, default=0)
    lavage_nuit_blanc_c = models.IntegerField(blank=True, null=True, default=0)
    lavage_nuit_blanc_nc = models.IntegerField(blank=True, null=True, default=0)
    lavage_nuit_bleu_c = models.IntegerField(blank=True, null=True, default=0)
    lavage_nuit_bleu_nc = models.IntegerField(blank=True, null=True, default=0)
    # Lavage Poste Nuit - Time fields
    lavage_nuit_heure_w_debut = models.TimeField(blank=True, null=True)
    lavage_nuit_heure_w_fin = models.TimeField(blank=True, null=True)
    lavage_nuit_heure_w_nombre = models.FloatField(blank=True, null=True)
    # Lavage Poste Nuit - Heures Arret 1
    lavage_nuit_heure_a1_debut = models.TimeField(blank=True, null=True)
    lavage_nuit_heure_a1_fin = models.TimeField(blank=True, null=True)
    lavage_nuit_heure_a1_nombre = models.FloatField(blank=True, null=True)
    # Lavage Poste Nuit - Heures Arret 2
    lavage_nuit_heure_a2_debut = models.TimeField(blank=True, null=True)
    lavage_nuit_heure_a2_fin = models.TimeField(blank=True, null=True)
    lavage_nuit_heure_a2_nombre = models.FloatField(blank=True, null=True)
    # Lavage Poste Nuit - Motifs
    lavage_nuit_motif_arret1 = models.CharField(max_length=20, choices=MOTIF_CHOICES, blank=True, null=True)
    lavage_nuit_motif_arret2 = models.CharField(max_length=20, choices=MOTIF_CHOICES, blank=True, null=True)

    # Lavage - Purge fields
    lavage_purge_jour = models.IntegerField(blank=True, null=True, default=0)
    lavage_purge_nuit = models.IntegerField(blank=True, null=True, default=0)
    lavage_non_conforme = models.IntegerField(blank=True, null=True, default=0)

    #### PREALPINA ####

    # Préalpina production totals
    prealpina_production_totale = models.IntegerField(blank=True, null=True, default=0)

    # Prealpina Poste Jour - Colors (Kg)
    prealpina_jour_bigbag_noir = models.IntegerField(blank=True, null=True, default=0)
    prealpina_jour_bigbag_blanc = models.IntegerField(blank=True, null=True, default=0)
    prealpina_jour_sacs_blanc = models.IntegerField(blank=True, null=True, default=0)
    prealpina_jour_sacs_bleu = models.IntegerField(blank=True, null=True, default=0)
    prealpina_jour_sacs_noir = models.IntegerField(blank=True, null=True, default=0)
    prealpina_jour_autre = models.IntegerField(blank=True, null=True, default=0)
    # Prealpina Poste Jour - Time fields
    prealpina_jour_heure_w_debut = models.TimeField(blank=True, null=True)
    prealpina_jour_heure_w_fin = models.TimeField(blank=True, null=True)
    prealpina_jour_heure_w_nombre = models.FloatField(blank=True, null=True)
    # Prealpina Poste Jour - Heures Arret 1
    prealpina_jour_heure_a1_debut = models.TimeField(blank=True, null=True)
    prealpina_jour_heure_a1_fin = models.TimeField(blank=True, null=True)
    prealpina_jour_heure_a1_nombre = models.FloatField(blank=True, null=True)
    # Prealpina Poste Jour - Heures Arret 2
    prealpina_jour_heure_a2_debut = models.TimeField(blank=True, null=True)
    prealpina_jour_heure_a2_fin = models.TimeField(blank=True, null=True)
    prealpina_jour_heure_a2_nombre = models.FloatField(blank=True, null=True)
    # Prealpina Poste Jour - Motifs
    prealpina_jour_motif_arret1 = models.CharField(max_length=20, choices=MOTIF_CHOICES, blank=True, null=True)
    prealpina_jour_motif_arret2 = models.CharField(max_length=20, choices=MOTIF_CHOICES, blank=True, null=True)

    # Prealpina Poste Nuit - Colors (Kg)
    prealpina_nuit_bigbag_noir = models.IntegerField(blank=True, null=True, default=0)
    prealpina_nuit_bigbag_blanc = models.IntegerField(blank=True, null=True, default=0)
    prealpina_nuit_sacs_blanc = models.IntegerField(blank=True, null=True, default=0)
    prealpina_nuit_sacs_bleu = models.IntegerField(blank=True, null=True, default=0)
    prealpina_nuit_sacs_noir = models.IntegerField(blank=True, null=True, default=0)
    prealpina_nuit_autre = models.IntegerField(blank=True, null=True, default=0)
    # Prealpina Poste Nuit - Time fields
    prealpina_nuit_heure_w_debut = models.TimeField(blank=True, null=True)
    prealpina_nuit_heure_w_fin = models.TimeField(blank=True, null=True)
    prealpina_nuit_heure_w_nombre = models.FloatField(blank=True, null=True)
    # Prealpina Poste Nuit - Heures Arret 1
    prealpina_nuit_heure_a1_debut = models.TimeField(blank=True, null=True)
    prealpina_nuit_heure_a1_fin = models.TimeField(blank=True, null=True)
    prealpina_nuit_heure_a1_nombre = models.FloatField(blank=True, null=True)
    # Prealpina Poste Nuit - Heures Arret 2
    prealpina_nuit_heure_a2_debut = models.TimeField(blank=True, null=True)
    prealpina_nuit_heure_a2_fin = models.TimeField(blank=True, null=True)
    prealpina_nuit_heure_a2_nombre = models.FloatField(blank=True, null=True)
    # Prealpina Poste Nuit - Motifs
    prealpina_nuit_motif_arret1 = models.CharField(max_length=20, choices=MOTIF_CHOICES, blank=True, null=True)
    prealpina_nuit_motif_arret2 = models.CharField(max_length=20, choices=MOTIF_CHOICES, blank=True, null=True)
    # Prealpina - Purge fields
    prealpina_purge_jour = models.IntegerField(blank=True, null=True, default=0)
    prealpina_purge_nuit = models.IntegerField(blank=True, null=True, default=0)
    prealpina_non_conforme = models.IntegerField(blank=True, null=True, default=0)


    #### MATIERE PREMIERE ####
    # Matière première fields
    matiere_vrac = models.IntegerField(blank=True, null=True, default=0)
    matiere_agadir = models.IntegerField(blank=True, null=True, default=0)
    matiere_fromage = models.IntegerField(blank=True, null=True, default=0)
    matiere_balle_beurre = models.IntegerField(blank=True, null=True, default=0)
    matiere_marrakech = models.IntegerField(blank=True, null=True, default=0)
    matiere_paillage = models.IntegerField(blank=True, null=True, default=0)
    matiere_serre = models.IntegerField(blank=True, null=True, default=0)
    matiere_autre = models.IntegerField(blank=True, null=True, default=0)
    matiere_broye = models.IntegerField(blank=True, null=True, default=0)
    matiere_net_trie = models.IntegerField(blank=True, null=True, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # is_new = self._state.adding
        # super().save(*args, **kwargs)
        # if is_new:
        self.export_to_csv()

    def _format_number(self, value):
        """Helper pour formater les nombres avec espaces comme séparateurs"""
        return value if value else ''

    def _format_decimal(self, value):
        """Helper pour formater les décimaux"""
        return str(value) if value else ''

    def _get_date_parts(self):
        """Helper pour obtenir les parties de la date"""
        date_obj = self.date
        if isinstance(self.date, str):
            try:
                from datetime import datetime
                date_obj = datetime.strptime(self.date, '%Y-%m-%d').date()
            except:
                date_obj = None

        if date_obj:
            # Mapping des mois en français
            mois_francais = {
                1: 'Janvier', 2: 'Février', 3: 'Mars', 4: 'Avril',
                5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Août',
                9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Décembre'
            }
            mois_nom = mois_francais.get(date_obj.month, '')
            annee = date_obj.strftime('%Y')
            mois_format = f"{mois_nom} {annee}" if mois_nom else ''

            return {
                'date': date_obj.strftime('%d/%m/%Y'),
                'mois': mois_format,
                'annee': date_obj.strftime('%Y')
            }
        return {'date': '', 'mois': '', 'annee': ''}

    def export_to_csv(self):
        """Exporte cette production vers le fichier CSV de façon additive"""
        csv_file_path = getattr(settings, 'PRODUCTION_EXPORT_CSV_PATH', 'excel_app_communication/production_app_export.csv')

        # Créer le dossier parent s'il n'existe pas
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        # Vérifier si le fichier existe pour ajouter les en-têtes
        file_exists = os.path.isfile(csv_file_path)

        with open(csv_file_path, 'a', newline='', encoding='windows-1256') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')

            # Calculer les totaux
            lavage_jour_total = sum([
                self.lavage_jour_noir_c or 0, self.lavage_jour_noir_nc or 0,
                self.lavage_jour_blanc_c or 0, self.lavage_jour_blanc_nc or 0,
                self.lavage_jour_bleu_c or 0, self.lavage_jour_bleu_nc or 0
            ])

            lavage_nuit_total = sum([
                self.lavage_nuit_noir_c or 0, self.lavage_nuit_noir_nc or 0,
                self.lavage_nuit_blanc_c or 0, self.lavage_nuit_blanc_nc or 0,
                self.lavage_nuit_bleu_c or 0, self.lavage_nuit_bleu_nc or 0
            ])

            prealpina_jour_total = sum([
                self.prealpina_jour_bigbag_noir or 0, self.prealpina_jour_bigbag_blanc or 0,
                self.prealpina_jour_sacs_blanc or 0, self.prealpina_jour_sacs_bleu or 0,
                self.prealpina_jour_sacs_noir or 0, self.prealpina_jour_autre or 0
            ])

            prealpina_nuit_total = sum([
                self.prealpina_nuit_bigbag_noir or 0, self.prealpina_nuit_bigbag_blanc or 0,
                self.prealpina_nuit_sacs_blanc or 0, self.prealpina_nuit_sacs_bleu or 0,
                self.prealpina_nuit_sacs_noir or 0, self.prealpina_nuit_autre or 0
            ])


            def heure_prod_excel_style(start, end):
                return f"{str(start)[:-3]} >> {str(end)[:-3]}" if start and end else ''

            # Obtenir les parties de la date
            date_parts = self._get_date_parts()

            # Construire le dictionnaire de données
            row_data = [
                # En-tête commun
                date_parts['date'],              # Date
                date_parts['mois'],              # Mois
                date_parts['annee'],             # Année
                self.meteo or '',                # Météo
                self.rempli_par or '',           # Rempli par

                # Lavage - Production et couleurs jour
                self._format_number(self.lavage_production_totale),  # Prod° (Kg)
                self._format_number(lavage_jour_total),              # Prod° jour (Kg)
                self._format_number(self.lavage_jour_noir_c),        # Noir C
                self._format_number(self.lavage_jour_noir_nc),       # Noir NC
                self._format_number(self.lavage_jour_blanc_c),       # Blanc C
                self._format_number(self.lavage_jour_blanc_nc),     # Blanc NC
                self._format_number(self.lavage_jour_bleu_c),       # Bleu C
                self._format_number(self.lavage_jour_bleu_nc),      # Bleu NC

                # Lavage - Horaires et arrêts jour
                heure_prod_excel_style(self.lavage_jour_heure_w_debut, self.lavage_jour_heure_w_fin) or '', # heure W
                self._format_decimal(self.lavage_jour_heure_w_nombre),                                # Nombre H
                heure_prod_excel_style(self.lavage_jour_heure_a1_debut, self.lavage_jour_heure_a1_fin), #heure arrête 1                     # Arrêt 1
                self._format_decimal(self.lavage_jour_heure_a1_nombre),                               # Arrêt 1 (h)
                heure_prod_excel_style(self.lavage_jour_heure_a2_debut, self.lavage_jour_heure_a2_fin),                      # Arrêt 2
                self._format_decimal(self.lavage_jour_heure_a2_nombre),    # Arrêt 2 (h)
                self.get_lavage_jour_motif_arret1_display(),                # Motif 1
                self.get_lavage_jour_motif_arret2_display(),                # Motif 2

                # Lavage - Production et couleurs nuit
                self._format_number(lavage_nuit_total),             # Prod° nuit (Kg)
                self._format_number(self.lavage_nuit_noir_c),       # Noir C (nuit)
                self._format_number(self.lavage_nuit_noir_nc),      # Noir NC (nuit)
                self._format_number(self.lavage_nuit_blanc_c),      # Blanc C (nuit)
                self._format_number(self.lavage_nuit_blanc_nc),     # Blanc NC (nuit)
                self._format_number(self.lavage_nuit_bleu_c),       # Bleu C (nuit)
                self._format_number(self.lavage_nuit_bleu_nc),      # Bleu NC (nuit)

                heure_prod_excel_style(self.lavage_nuit_heure_w_debut, self.lavage_nuit_heure_w_fin), # heure W (nuit)
                self._format_decimal(self.lavage_nuit_heure_w_nombre),                                # Nombre H (nuit)
                heure_prod_excel_style(self.lavage_nuit_heure_a1_debut, self.lavage_nuit_heure_a1_fin), # heure arrête 1   (nuit)                   # Arrêt 1
                self._format_decimal(self.lavage_nuit_heure_a1_nombre),                               # Arrêt 1 (h) (nuit)
                heure_prod_excel_style(self.lavage_nuit_heure_a2_debut, self.lavage_nuit_heure_a2_fin), # heure Arrêt 2 (nuit)
                self._format_decimal(self.lavage_nuit_heure_a2_nombre),    # Arrêt 2 (h) (nuit)
                self.get_lavage_nuit_motif_arret1_display(),                # Motif 1 (nuit)
                self.get_lavage_nuit_motif_arret2_display(),                # Motif 2 (nuit)

                # Lavage - Purge
                self._format_number(self.lavage_non_conforme),                       # NC
                self._format_number(self.lavage_purge_jour),               # Purge J
                self._format_number(self.lavage_purge_nuit),               # Purge N

                # Préalpina - Production jour
                self._format_number(self.prealpina_production_totale), # Prod° (Kg) (Préalpina)
                self._format_number(prealpina_jour_total),              # Prod° jour (Kg) (Préalpina)
                self._format_number(self.prealpina_jour_bigbag_noir),   # BB noir (jour)
                self._format_number(self.prealpina_jour_bigbag_blanc),  # BB blanc (jour)
                self._format_number(self.prealpina_jour_sacs_blanc),    # sacs blanc (jour)
                self._format_number(self.prealpina_jour_sacs_bleu),     # sacs bleu (jour)
                self._format_number(self.prealpina_jour_sacs_noir),     # sacs noir (jour)
                self._format_number(self.prealpina_jour_autre),         # autre (jour)

                # Préalpina - Horaires et arrêts jour
                heure_prod_excel_style(self.prealpina_jour_heure_w_debut, self.prealpina_jour_heure_w_fin),   # heure W
                self._format_decimal(self.prealpina_jour_heure_w_nombre),                                      # Nombre H
                heure_prod_excel_style(self.prealpina_jour_heure_a1_debut, self.prealpina_jour_heure_a1_fin), # heure arrête 1                     # Arrêt 1
                self._format_decimal(self.prealpina_jour_heure_a1_nombre),                                     # Arrêt 1 (h)
                heure_prod_excel_style(self.prealpina_jour_heure_a2_debut, self.prealpina_jour_heure_a2_fin),   # Arrêt 2
                self._format_decimal(self.prealpina_jour_heure_a2_nombre),                                          # Arrêt 2 (h)
                self.get_prealpina_jour_motif_arret1_display(),                                                             # Motif 1
                self.get_prealpina_jour_motif_arret2_display(),                                                              # Motif 2

                # Préalpina - Production nuit
                self._format_number(prealpina_nuit_total),              # Prod° nuit (Kg) (Préalpina)
                self._format_number(self.prealpina_nuit_bigbag_noir),   # BB noir (nuit)
                self._format_number(self.prealpina_nuit_bigbag_blanc),  # BB blanc (nuit)
                self._format_number(self.prealpina_nuit_sacs_blanc),    # sacs blanc (nuit)
                self._format_number(self.prealpina_nuit_sacs_bleu),     # sacs bleu (nuit)
                self._format_number(self.prealpina_nuit_sacs_noir),     # sacs noir (nuit)
                self._format_number(self.prealpina_nuit_autre),         # autre (nuit)

                # Préalpina - Horaires et arrêts nuit
                heure_prod_excel_style(self.prealpina_nuit_heure_w_debut, self.prealpina_nuit_heure_w_fin),   # heure W
                self._format_decimal(self.prealpina_nuit_heure_w_nombre),                                      # Nombre H
                heure_prod_excel_style(self.prealpina_nuit_heure_a1_debut, self.prealpina_nuit_heure_a1_fin), # heure arrête 1                     # Arrêt 1
                self._format_decimal(self.prealpina_nuit_heure_a1_nombre),                                     # Arrêt 1 (h)
                heure_prod_excel_style(self.prealpina_nuit_heure_a2_debut, self.prealpina_nuit_heure_a2_fin),   # Arrêt 2
                self._format_decimal(self.prealpina_nuit_heure_a2_nombre),                                          # Arrêt 2 (h)
                self.get_prealpina_nuit_motif_arret1_display(),                                                             # Motif 1
                self.get_prealpina_nuit_motif_arret2_display(),       

                # Préalpina - Purge
                self._format_number(self.prealpina_non_conforme),                 # NC (Préalpina)
                self._format_number(self.prealpina_purge_jour),         # Purge J (Préalpina)
                self._format_number(self.prealpina_purge_nuit),         # Purge N (Préalpina)

                # Matière première
                self._format_number(self.matiere_vrac),                 # VRAC
                self._format_number(self.matiere_agadir),               # AGADIR
                self._format_number(self.matiere_fromage),              # FROMAGE
                self._format_number(self.matiere_balle_beurre),         # BALLE BEURRE
                self._format_number(self.matiere_marrakech),            # MARRAKECH
                self._format_number(self.matiere_paillage),             # PAILLAGE
                self._format_number(self.matiere_serre),                # SERRE
                self._format_number(self.matiere_autre),                # AUTRE
                self._format_number(self.matiere_broye),                # BROYE
                self._format_number(self.matiere_net_trie)              # Net trié
            ]

            writer.writerow(row_data)

            

    def __str__(self):
        return f"Production {self.date} - {self.rempli_par or 'Non défini'}"

    class Meta:
        ordering = ['-date', '-created_at']
