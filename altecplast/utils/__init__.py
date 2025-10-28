# Utils package for weighing app
import os, json, logging, sys, locale


# Configuration du logger
logger = logging.getLogger(__name__)

# définir locale en FR pour récupérer les mois en fr
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

# Charger une seule fois la configuration 
CELLS_PROD = {}
CELLS_PESAGE = {}

def print_error(message, e = None):
    logger.error(message)
    logger.error(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    logger.error(f"Erreur à la ligne >>>>>{exc_tb.tb_lineno}")

def open_cells(file_name):
    try:
        _config_path = os.path.join(os.path.dirname(__file__), file_name)
        with open(_config_path, 'r', encoding='utf-8') as _f:
            return json.load(_f)
    except Exception as e:
        print_error(f"Impossible de charger {file_name} depuis {_config_path}", e)
        return {}

CELLS_PROD = open_cells('cells_prod.json')
CELLS_PESAGE = open_cells('cells_pesage.json')
CELLS_STOCK = open_cells('cells_stock.json')
