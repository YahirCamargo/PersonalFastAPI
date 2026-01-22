import random
import string
from datetime import datetime

def generar_numero_seguimiento() -> str:
    fecha = datetime.utcnow().strftime("%Y%m%d")
    random_part = ''.join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )
    return f"ENV-{fecha}-{random_part}"
