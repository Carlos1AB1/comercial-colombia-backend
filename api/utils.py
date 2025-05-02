# api/utils.py

def get_client_ip(request):
    """Obtiene la dirección IP del cliente desde el request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Si hay múltiples IPs (por proxies), toma la primera
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        # Si no, usa la IP de la conexión directa
        ip = request.META.get('REMOTE_ADDR')
    return ip