from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Supplier, Client, Waste_client, Weighing, Production
from django.conf import settings
import logging
from datetime import datetime, timedelta, date
from .utils.excel_reader import get_dashboard_data

logger = logging.getLogger(__name__)


def home_view(request):
    """Page d'accueil avec date, heure et liens vers les pages"""
    return render(request, 'home.html')

def simulateur_form_view(request):
    """Main simulateur type selection page"""
    return render(request, 'simulateur/simulateur.html')

def weighing_form_view(request):
    """Main weighing type selection page"""
    return render(request, 'weighing/weighing.html')


def referenced_entry_view(request):
    """Entrée Référencée - Referenced entry with supplier selection"""
    if request.method == 'POST':
        # Process form data
        weighing_data = {
            'weighing_type': 'referenced_entry',
            'weighing_number': request.POST.get('weighing_number'),
            'transporter': request.POST.get('transporter'),
            'origin': request.POST.get('origin'),
            'vehicle_type': request.POST.get('vehicle_type'),
            'license_plate': request.POST.get('license_plate'),
            'gross_weight_kg': int(request.POST.get('gross_weight_kg', 0)),
            'tare_weight': int(request.POST.get('tare_weight', 0)),
            'net_weight_1_kg': int(request.POST.get('net_weight_1_kg', 0)),
            'deduction_amount': int(request.POST.get('deduction_amount') or 0),
            'deduction_type': request.POST.get('deduction_type', '%'),
            'net_weight_2_kg': int(request.POST.get('net_weight_2_kg', 0)),
            'product': request.POST.get('product'),
            'product_type': request.POST.get('product_type'),
            'form': request.POST.get('form'),
            'color_quality': request.POST.get('color_quality'),
            'packaging': request.POST.get('packaging'),
            'packaging_quantity': int(request.POST.get('packaging_quantity') or 0),
        }
        
        # Get selected supplier
        supplier_id = request.POST.get('supplier_id')
        if supplier_id:
            supplier = Supplier.objects.get(id=supplier_id)
            
            # Create weighing record
            weighing = Weighing.objects.create(
                company=supplier,
                **weighing_data
            )
            return redirect('weighing')
    
    # GET request - show form
    suppliers = Supplier.objects.all().order_by('company_name')
    return render(request, 'weighing/weighing_type/referenced_entry.html', {
        'suppliers': suppliers
    })


def get_supplier_defaults(request):
    """AJAX endpoint to get supplier default values"""
    supplier_id = request.GET.get('supplier_id')
    if supplier_id:
        try:
            supplier = Supplier.objects.get(id=supplier_id)
            return JsonResponse({
                'default_transporter': supplier.default_transporter,
                'default_origin': supplier.default_origin,
                'default_vehicle_type': supplier.default_vehicle_type,
                'default_license_plate': supplier.default_license_plate,
                'default_product': supplier.default_product,
                'default_product_type': supplier.default_product_type,
                'default_form': supplier.default_form,
                'default_color_quality': supplier.default_color_quality,
                'default_packaging': supplier.default_packaging,
            })
        except Supplier.DoesNotExist:
            pass
    
    return JsonResponse({})


def get_client_defaults(request):
    """AJAX endpoint to get client default values"""
    client_id = request.GET.get('client_id')
    if client_id:
        try:
            client = Client.objects.get(id=client_id)
            return JsonResponse({
                'default_transporter': client.default_transporter,
                'default_vehicle_type': client.default_vehicle_type,
                'default_license_plate': client.default_license_plate,
                'default_product': client.default_product,
                'default_product_type': client.default_product_type,
                'default_form': client.default_form,
                'default_color_quality': client.default_color_quality,
                'default_packaging': client.default_packaging,
            })
        except Client.DoesNotExist:
            pass
    
    return JsonResponse({})


def get_waste_client_defaults(request):
    """AJAX endpoint to get waste client default values"""
    waste_client_id = request.GET.get('waste_client_id')
    if waste_client_id:
        try:
            waste_client = Waste_client.objects.get(id=waste_client_id)
            return JsonResponse({
                'default_transporter': waste_client.default_transporter,
                'default_vehicle_type': waste_client.default_vehicle_type,
                'default_license_plate': waste_client.default_license_plate,
                'default_product': waste_client.default_product,
                'default_product_type': waste_client.default_product_type,
                'default_form': waste_client.default_form,
                'default_color_quality': waste_client.default_color_quality,
                'default_packaging': waste_client.default_packaging,
            })
        except Waste_client.DoesNotExist:
            pass
    
    return JsonResponse({})


def non_referenced_entry_view(request):
    """Entrée Non Référencée - Non-referenced entry with manual input"""
    if request.method == 'POST':
        # Process form data
        weighing_data = {
            'weighing_type': 'non_referenced_entry',
            'weighing_number': request.POST.get('weighing_number'),
            'company_non_referenced': request.POST.get('supplier_id_non_referenced'),
            'transporter': request.POST.get('transporter'),
            'origin': request.POST.get('origin'),
            'vehicle_type': request.POST.get('vehicle_type'),
            'license_plate': request.POST.get('license_plate'),
            'gross_weight_kg': int(request.POST.get('gross_weight_kg', 0)),
            'tare_weight': int(request.POST.get('tare_weight', 0)),
            'net_weight_1_kg': int(request.POST.get('net_weight_1_kg', 0)),
            'deduction_amount': int(request.POST.get('deduction_amount') or 0),
            'deduction_type': request.POST.get('deduction_type', '%'),
            'net_weight_2_kg': int(request.POST.get('net_weight_2_kg', 0)),
            'product': request.POST.get('product'),
            'product_type': request.POST.get('product_type'),
            'form': request.POST.get('form'),
            'color_quality': request.POST.get('color_quality'),
            'packaging': request.POST.get('packaging'),
            'packaging_quantity': int(request.POST.get('packaging_quantity') or 0),
        }
        
        # Create weighing record without supplier (non-referenced entry)
        # We need to create a dummy supplier or handle this differently
        # Let's create the record with company=None for now and modify the model
        try:
            weighing = Weighing.objects.create(
                company=None,  # This might cause issues - need to handle
                **weighing_data
            )
            return redirect('weighing')
        except Exception as e:
            # Handle the error gracefully
            print(f"Error creating weighing record: {e}")
            return render(request, 'weighing/weighing_type/non_referenced_entry.html', {
                'error': 'Erreur lors de l\'enregistrement'
            })
    
    # GET request - show form
    return render(request, 'weighing/weighing_type/non_referenced_entry.html')


def finished_product_output_view(request):
    """Sortie Produit Fini - Finished product output to client"""
    if request.method == 'POST':
        # Process form data
        weighing_data = {
            'weighing_type': 'finished_product_output',
            'weighing_number': request.POST.get('weighing_number'),
            'transporter': request.POST.get('transporter'),
            'vehicle_type': request.POST.get('vehicle_type'),
            'license_plate': request.POST.get('license_plate'),
            'gross_weight_kg': int(request.POST.get('gross_weight_kg', 0)),
            'tare_weight': int(request.POST.get('tare_weight', 0)),
            'net_weight_1_kg': int(request.POST.get('net_weight_1_kg', 0)),
            'product': request.POST.get('product'),
            'product_type': request.POST.get('product_type'),
            'form': request.POST.get('form'),
            'color_quality': request.POST.get('color_quality'),
            'packaging': request.POST.get('packaging'),
            'packaging_quantity': int(request.POST.get('packaging_quantity') or 0),
        }
        
        # Get selected client
        client_id = request.POST.get('client_id')
        if client_id:
            try:
                client = Client.objects.get(id=client_id)
                
                # Create weighing record
                weighing = Weighing.objects.create(
                    company=None,  # For client-based transactions, we might need a different field
                    client=client,  # We'll need to add this field to the model
                    **weighing_data
                )
                return redirect('weighing')
            except Client.DoesNotExist:
                pass
        
        return render(request, 'weighing/weighing_type/finished_product_output.html', {
            'clients': Client.objects.all(),
            'error': 'Veuillez sélectionner un client valide'
        })
    
    # GET request - show form
    clients = Client.objects.all().order_by('company_name')
    return render(request, 'weighing/weighing_type/finished_product_output.html', {
        'clients': clients
    })


def waste_output_view(request):
    """Sortie Déchet - Waste output to waste client"""
    if request.method == 'POST':
        # Process form data
        weighing_data = {
            'weighing_type': 'waste_output',
            'weighing_number': request.POST.get('weighing_number'),
            'transporter': request.POST.get('transporter'),
            'vehicle_type': request.POST.get('vehicle_type'),
            'license_plate': request.POST.get('license_plate'),
            'gross_weight_kg': int(request.POST.get('gross_weight_kg', 0)),
            'tare_weight': int(request.POST.get('tare_weight', 0)),
            'net_weight_1_kg': int(request.POST.get('net_weight_1_kg', 0)),
            'product': request.POST.get('product'),
            'product_type': request.POST.get('product_type'),
            'form': request.POST.get('form'),
            'color_quality': request.POST.get('color_quality'),
            'packaging': request.POST.get('packaging'),
            'packaging_quantity': int(request.POST.get('packaging_quantity') or 0),
        }
        
        # Get selected waste client
        waste_client_id = request.POST.get('waste_client_id')
        if waste_client_id and waste_client_id != 'SELECT':
            try:
                waste_client = Waste_client.objects.get(id=waste_client_id)
                
                # Create weighing record
                weighing = Weighing.objects.create(
                    company=None,
                    waste_client=waste_client,
                    **weighing_data
                )
                return redirect('weighing')
            except Waste_client.DoesNotExist:
                pass
        
        return render(request, 'weighing/weighing_type/waste_output.html', {
            'waste_clients': Waste_client.objects.all(),
            'error': 'Veuillez sélectionner un client déchet valide'
        })
    
    # GET request - show form
    waste_clients = Waste_client.objects.all().order_by('company_name')
    return render(request, 'weighing/weighing_type/waste_output.html', {
        'waste_clients': waste_clients
    })


def finished_product_return_view(request):
    """Retour Produit Fini - Finished product return"""
    if request.method == 'POST':
        # Process form data
        weighing_data = {
            'weighing_type': 'finished_product_return',
            'weighing_number': request.POST.get('weighing_number'),
            'transporter': request.POST.get('transporter'),
            'vehicle_type': request.POST.get('vehicle_type'),
            'license_plate': request.POST.get('license_plate'),
            'gross_weight_kg': int(request.POST.get('gross_weight_kg', 0)),
            'tare_weight': int(request.POST.get('tare_weight', 0)),
            'net_weight_1_kg': int(request.POST.get('net_weight_1_kg', 0)),
            'product': request.POST.get('product'),
            'product_type': request.POST.get('product_type'),
            'form': request.POST.get('form'),
            'color_quality': request.POST.get('color_quality'),
            'packaging': request.POST.get('packaging'),
            'packaging_quantity': int(request.POST.get('packaging_quantity') or 0),
        }
        
        # Get selected client
        client_id = request.POST.get('client_id')
        if client_id and client_id != 'SELECT':
            try:
                client = Client.objects.get(id=client_id)
                
                # Create weighing record
                weighing = Weighing.objects.create(
                    company=None,
                    client=client,
                    **weighing_data
                )
                return redirect('weighing')
            except Client.DoesNotExist:
                pass
        
        return render(request, 'weighing/weighing_type/finished_product_return.html', {
            'clients': Client.objects.all(),
            'error': 'Veuillez sélectionner un client valide'
        })
    
    # GET request - show form
    clients = Client.objects.all().order_by('company_name')
    return render(request, 'weighing/weighing_type/finished_product_return.html', {
        'clients': clients
    })


def merchandise_return_view(request):
    """Retour Marchandise - Merchandise return to supplier"""
    if request.method == 'POST':
        # Process form data
        weighing_data = {
            'weighing_type': 'merchandise_return',
            'weighing_number': request.POST.get('weighing_number'),
            'transporter': request.POST.get('transporter'),
            'origin': request.POST.get('origin'),
            'vehicle_type': request.POST.get('vehicle_type'),
            'license_plate': request.POST.get('license_plate'),
            'gross_weight_kg': int(request.POST.get('gross_weight_kg', 0)),
            'tare_weight': int(request.POST.get('tare_weight', 0)),
            'net_weight_1_kg': int(request.POST.get('net_weight_1_kg', 0)),
            'deduction_amount': int(request.POST.get('deduction_amount') or 0),
            'deduction_type': request.POST.get('deduction_type', '%'),
            'net_weight_2_kg': int(request.POST.get('net_weight_2_kg', 0)),
            'product': request.POST.get('product'),
            'product_type': request.POST.get('product_type'),
            'form': request.POST.get('form'),
            'color_quality': request.POST.get('color_quality'),
            'packaging': request.POST.get('packaging'),
            'packaging_quantity': int(request.POST.get('packaging_quantity') or 0),
        }
        
        # Get selected supplier
        supplier_id = request.POST.get('supplier_id')
        if supplier_id:
            try:
                supplier = Supplier.objects.get(id=supplier_id)
                
                # Create weighing record
                weighing = Weighing.objects.create(
                    company=supplier,
                    **weighing_data
                )
                return redirect('weighing')
            except Supplier.DoesNotExist:
                pass
        
        return render(request, 'weighing/weighing_type/merchandise_return.html', {
            'suppliers': Supplier.objects.all().order_by('company_name'),
            'error': 'Veuillez sélectionner un fournisseur valide'
        })
    
    # GET request - show form
    suppliers = Supplier.objects.all().order_by('company_name')
    return render(request, 'weighing/weighing_type/merchandise_return.html', {
        'suppliers': suppliers
    })


def outsourced_product_output_view(request):
    """ Sortie Produit (sous-traitance) - Outsourced product output to client """
    if request.method == 'POST':
        # Process form data
        weighing_data = {
            'weighing_type': 'outsourced_product_output',
            'weighing_number': request.POST.get('weighing_number'),
            'transporter': request.POST.get('transporter'),
            'vehicle_type': request.POST.get('vehicle_type'),
            'license_plate': request.POST.get('license_plate'),
            'gross_weight_kg': int(request.POST.get('gross_weight_kg', 0)),
            'tare_weight': int(request.POST.get('tare_weight', 0)),
            'net_weight_1_kg': int(request.POST.get('net_weight_1_kg', 0)),
            'product': request.POST.get('product'),
            'product_type': request.POST.get('product_type'),
            'form': request.POST.get('form'),
            'color_quality': request.POST.get('color_quality'),
            'packaging': request.POST.get('packaging'),
            'packaging_quantity': int(request.POST.get('packaging_quantity') or 0),
        }
        
        # Get selected client
        client_id = request.POST.get('client_id')
        if client_id:
            try:
                client = Client.objects.get(id=client_id)
                
                # Create weighing record
                weighing = Weighing.objects.create(
                    company=None,  # For client-based transactions, we might need a different field
                    client=client,  # We'll need to add this field to the model
                    **weighing_data
                )
                return redirect('weighing')
            except Client.DoesNotExist:
                pass
        
        return render(request, 'weighing/weighing_type/outsourced_product_output.html', {
            'clients': Client.objects.all(),
            'error': 'Veuillez sélectionner un client valide'
        })
    
    # GET request - show form
    clients = Client.objects.all().order_by('company_name')
    return render(request, 'weighing/weighing_type/outsourced_product_output.html', {
        'clients': clients
    })


def outsourced_product_return_view(request):
    """Retour Produit (sous-traitance) - Outsourced product return"""
    if request.method == 'POST':
        # Process form data
        weighing_data = {
            'weighing_type': 'outsourced_product_return',
            'weighing_number': request.POST.get('weighing_number'),
            'transporter': request.POST.get('transporter'),
            'vehicle_type': request.POST.get('vehicle_type'),
            'license_plate': request.POST.get('license_plate'),
            'gross_weight_kg': int(request.POST.get('gross_weight_kg', 0)),
            'tare_weight': int(request.POST.get('tare_weight', 0)),
            'net_weight_1_kg': int(request.POST.get('net_weight_1_kg', 0)),
            'product': request.POST.get('product'),
            'product_type': request.POST.get('product_type'),
            'form': request.POST.get('form'),
            'color_quality': request.POST.get('color_quality'),
            'packaging': request.POST.get('packaging'),
            'packaging_quantity': int(request.POST.get('packaging_quantity') or 0),
        }
        
        # Get selected client
        client_id = request.POST.get('client_id')
        if client_id and client_id != 'SELECT':
            try:
                client = Client.objects.get(id=client_id)
                
                # Create weighing record
                weighing = Weighing.objects.create(
                    company=None,
                    client=client,
                    **weighing_data
                )
                return redirect('weighing')
            except Client.DoesNotExist:
                pass
        
        return render(request, 'weighing/weighing_type/outsourced_product_return.html', {
            'clients': Client.objects.all(),
            'error': 'Veuillez sélectionner un client valide'
        })
    
    # GET request - show form
    clients = Client.objects.all().order_by('company_name')
    return render(request, 'weighing/weighing_type/outsourced_product_return.html', {
        'clients': clients
    })



def dashboard_login_view(request):
    """Page de connexion pour accéder au dashboard"""
    if request.method == 'POST':
        code = request.POST.get('code', '')
        if code == settings.DASHBOARD_PASSWORD:
            request.session['dashboard_access'] = True
            return redirect('dashboard')
        else:
            return render(request, 'dashboard_login.html', {
                'error': 'Code incorrect. Veuillez réessayer.'
            })

    return render(request, 'dashboard_login.html')

def dashboard_view(request):
    """Dashboard avec KPIs"""
    # Vérifier si l'utilisateur a accès au dashboard
    if not request.session.get('dashboard_access', False):
        return redirect('dashboard_login')

    return render(request, 'dashboard.html')


def dashboard_data_view(request):
    """API endpoint pour récupérer les données du dashboard selon le mois"""
    # Vérifier si l'utilisateur a accès au dashboard
    if not request.session.get('dashboard_access', False):
        return JsonResponse({'error': 'Accès non autorisé'}, status=403)
    # Récupérer le mois demandé
    set_date = request.GET.get('date', date.today().strftime("%Y-%m"))
    try:
        # Récupérer les données depuis le fichier Excel pour le mois demandé
        excel_data = get_dashboard_data(set_date)
        if excel_data is None:
            return JsonResponse({'error': 'Données non disponibles pour le mois demandé'}, status=404)

        return JsonResponse(excel_data)

    except Exception as e:
        logger.error(f"Erreur lors de la récupération des données pour le mois {set_date}: {e}")
        return JsonResponse({'error': 'Erreur lors du chargement des données'}, status=500)


def production_view(request):
    """Page de production"""
    def prod_time_calculus(request, id_prefix):
        """
        Calcule la durée entre deux heures récupérées depuis le POST (par leur name/id).
        Retourne (start_time, stop_time, durée_en_heures) ou None si valeurs manquantes.
        Gère le passage de minuit.
        """
        start_id = f"{id_prefix}_debut"
        stop_id = f"{id_prefix}_fin"

        start_str = request.POST.get(start_id)
        stop_str = request.POST.get(stop_id)

        start_time = datetime.strptime(start_str, "%H:%M").time() if start_str else None
        stop_time = datetime.strptime(stop_str, "%H:%M").time() if stop_str else None

        if not start_time or not stop_time:
            return None, None, None

        today = datetime.today().date()
        debut_dt = datetime.combine(today, start_time)
        fin_dt = datetime.combine(today, stop_time)

        # Si la fin est avant le début → passage minuit
        if fin_dt < debut_dt:
            fin_dt += timedelta(days=1)

        duree = fin_dt - debut_dt
        duree = round(duree.total_seconds() / 3600, 2)

        return start_time, stop_time, duree

    if request.method == 'POST':
        try:
            # Créer l'objet Production
            production = Production()

            production.date =       request.POST.get('date')
            production.rempli_par = request.POST.get('rempli_par')
            production.meteo =      request.POST.get('meteo')

            # Lavage - Production totale
            production.lavage_production_totale = request.POST.get('lavage_production_totale') or 0

            # Lavage Poste Jour - Couleurs 
            production.lavage_jour_noir_c = int(request.POST.get('lavage_jour_noir_c') or 0)
            production.lavage_jour_noir_nc = int(request.POST.get('lavage_jour_noir_nc') or 0)
            production.lavage_jour_blanc_c = int(request.POST.get('lavage_jour_blanc_c') or 0)
            production.lavage_jour_blanc_nc = int(request.POST.get('lavage_jour_blanc_nc') or 0)
            production.lavage_jour_bleu_c = int(request.POST.get('lavage_jour_bleu_c') or 0)
            production.lavage_jour_bleu_nc = int(request.POST.get('lavage_jour_bleu_nc') or 0)

            # Lavage Poste Jour - Heures prod
            production.lavage_jour_heure_w_debut, \
            production.lavage_jour_heure_w_fin, \
            production.lavage_jour_heure_w_nombre = prod_time_calculus(request, 'lavage_jour_heure_w')

            # Lavage Poste Jour - Heures Arret 1
            production.lavage_jour_heure_a1_debut, \
            production.lavage_jour_heure_a1_fin, \
            production.lavage_jour_heure_a1_nombre = prod_time_calculus(request, 'lavage_jour_heure_a1')

            # Lavage Poste Jour - Heures Arret 2
            production.lavage_jour_heure_a2_debut, \
            production.lavage_jour_heure_a2_fin, \
            production.lavage_jour_heure_a2_nombre = prod_time_calculus(request, 'lavage_jour_heure_a2')

            # Lavage Poste Jour - Motif Arrêt 1 et 2
            production.lavage_jour_motif_arret1 = request.POST.get('lavage_jour_motif_arret1')
            production.lavage_jour_motif_arret2 = request.POST.get('lavage_jour_motif_arret2')

            # Lavage Poste Nuit - Couleurs
            production.lavage_nuit_noir_c = int(request.POST.get('lavage_nuit_noir_c') or 0)
            production.lavage_nuit_noir_nc = int(request.POST.get('lavage_nuit_noir_nc') or 0)
            production.lavage_nuit_blanc_c = int(request.POST.get('lavage_nuit_blanc_c') or 0)
            production.lavage_nuit_blanc_nc = int(request.POST.get('lavage_nuit_blanc_nc') or 0)
            production.lavage_nuit_bleu_c = int(request.POST.get('lavage_nuit_bleu_c') or 0)
            production.lavage_nuit_bleu_nc = int(request.POST.get('lavage_nuit_bleu_nc') or 0)

            # Lavage Poste Nuit - Heures prod
            production.lavage_nuit_heure_w_debut, \
            production.lavage_nuit_heure_w_fin, \
            production.lavage_nuit_heure_w_nombre = prod_time_calculus(request, 'lavage_nuit_heure_w')

            # Lavage Poste Nuit - Heures Arret 1
            production.lavage_nuit_heure_a1_debut, \
            production.lavage_nuit_heure_a1_fin, \
            production.lavage_nuit_heure_a1_nombre = prod_time_calculus(request, 'lavage_nuit_heure_a1')

            # Lavage Poste Nuit - Heures Arret 2
            production.lavage_nuit_heure_a2_debut, \
            production.lavage_nuit_heure_a2_fin, \
            production.lavage_nuit_heure_a2_nombre = prod_time_calculus(request, 'lavage_nuit_heure_a2')

            # Lavage Poste Nuit - Motif Arrêt 1 et 2
            production.lavage_nuit_motif_arret1 = request.POST.get('lavage_nuit_motif_arret1')
            production.lavage_nuit_motif_arret2 = request.POST.get('lavage_nuit_motif_arret2')

            # Lavage - Purge
            production.lavage_purge_jour = int(request.POST.get('lavage_purge_jour') or 0)
            production.lavage_purge_nuit = int(request.POST.get('lavage_purge_nuit') or 0)
            production.lavage_non_conforme = int(request.POST.get('lavage_non_conforme') or 0)

            # Préalpina - Production totale
            production.prealpina_production_totale = int(request.POST.get('production_totale_prealpina') or 0)

            # Préalpina Poste Jour
            production.prealpina_jour_bigbag_noir = int(request.POST.get('prealpina_jour_bigbag_noir') or 0)
            production.prealpina_jour_bigbag_blanc = int(request.POST.get('prealpina_jour_bigbag_blanc') or 0)
            production.prealpina_jour_sacs_blanc = int(request.POST.get('prealpina_jour_sacs_blanc') or 0)
            production.prealpina_jour_sacs_bleu = int(request.POST.get('prealpina_jour_sacs_bleu') or 0)
            production.prealpina_jour_sacs_noir = int(request.POST.get('prealpina_jour_sacs_noir') or 0)
            production.prealpina_jour_autre = int(request.POST.get('prealpina_jour_autre') or 0)

            # prealpina Poste Jour - Heures prod
            production.prealpina_jour_heure_w_debut, \
            production.prealpina_jour_heure_w_fin, \
            production.prealpina_jour_heure_w_nombre = prod_time_calculus(request, 'prealpina_jour_heure_w')

            # prealpina Poste Jour - Heures Arret 1
            production.prealpina_jour_heure_a1_debut, \
            production.prealpina_jour_heure_a1_fin, \
            production.prealpina_jour_heure_a1_nombre = prod_time_calculus(request, 'prealpina_jour_heure_a1')

            # prealpina Poste Jour - Heures Arret 2
            production.prealpina_jour_heure_a2_debut, \
            production.prealpina_jour_heure_a2_fin, \
            production.prealpina_jour_heure_a2_nombre = prod_time_calculus(request, 'prealpina_jour_heure_a2')

            # prealpina Poste Jour - Motif Arrêt 1 et 2
            production.prealpina_jour_motif_arret1 = request.POST.get('prealpina_jour_motif_arret1')
            production.prealpina_jour_motif_arret2 = request.POST.get('prealpina_jour_motif_arret2')

            # Préalpina Poste Nuit
            production.prealpina_nuit_bigbag_noir = int(request.POST.get('prealpina_nuit_bigbag_noir') or 0)
            production.prealpina_nuit_bigbag_blanc = int(request.POST.get('prealpina_nuit_bigbag_blanc') or 0)
            production.prealpina_nuit_sacs_blanc = int(request.POST.get('prealpina_nuit_sacs_blanc') or 0)
            production.prealpina_nuit_sacs_bleu = int(request.POST.get('prealpina_nuit_sacs_bleu') or 0)
            production.prealpina_nuit_sacs_noir = int(request.POST.get('prealpina_nuit_sacs_noir') or 0)
            production.prealpina_nuit_autre = int(request.POST.get('prealpina_nuit_autre') or 0)

            # prealpina Poste Nuit - Heures prod
            production.prealpina_nuit_heure_w_debut, \
            production.prealpina_nuit_heure_w_fin, \
            production.prealpina_nuit_heure_w_nombre = prod_time_calculus(request, 'prealpina_nuit_heure_w')

            # prealpina Poste Nuit - Heures Arret 1
            production.prealpina_nuit_heure_a1_debut, \
            production.prealpina_nuit_heure_a1_fin, \
            production.prealpina_nuit_heure_a1_nombre = prod_time_calculus(request, 'prealpina_nuit_heure_a1')

            # prealpina Poste Nuit - Heures Arret 2
            production.prealpina_nuit_heure_a2_debut, \
            production.prealpina_nuit_heure_a2_fin, \
            production.prealpina_nuit_heure_a2_nombre = prod_time_calculus(request, 'prealpina_nuit_heure_a2')

            # prealpina Poste Nuit - Motif Arrêt 1 et 2
            production.prealpina_nuit_motif_arret1 = request.POST.get('prealpina_nuit_motif_arret1')
            production.prealpina_nuit_motif_arret2 = request.POST.get('prealpina_nuit_motif_arret2')

            # Préalpina - Purge
            production.prealpina_purge_jour = int(request.POST.get('prealpina_purge_jour') or 0)
            production.prealpina_purge_nuit = int(request.POST.get('prealpina_purge_nuit') or 0)
            production.prealpina_non_conforme = int(request.POST.get('prealpina_nc') or 0)


            # Matière première - Fields
            production.matiere_vrac = int(request.POST.get('matiere_vrac') or 0)
            production.matiere_agadir = int(request.POST.get('matiere_agadir') or 0)
            production.matiere_fromage = int(request.POST.get('matiere_fromage') or 0)
            production.matiere_balle_beurre = int(request.POST.get('matiere_balle_beurre') or 0)
            production.matiere_marrakech = int(request.POST.get('matiere_marrakech') or 0)
            production.matiere_paillage = int(request.POST.get('matiere_paillage') or 0)
            production.matiere_serre = int(request.POST.get('matiere_serre') or 0)
            production.matiere_autre = int(request.POST.get('matiere_autre') or 0)
            production.matiere_broye = int(request.POST.get('matiere_broye') or 0)
            production.matiere_net_trie = int(request.POST.get('matiere_net_trie') or 0)

            # Sauvegarder (l'export CSV sera automatique)
            production.save()

            return JsonResponse({'success': True, 'message': 'Production enregistrée avec succès'})

        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement de la production: {str(e)}")
            return JsonResponse({'success': False, 'message': f'Erreur: {str(e)}'}, status=400)

    return render(request, 'production.html')

def admin_page(request):
    """Affiche la page admin de django"""
    return redirect('/admin/')