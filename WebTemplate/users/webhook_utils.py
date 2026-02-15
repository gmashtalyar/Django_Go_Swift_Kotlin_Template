"""
YooKassa webhook utilities for SimpleBoard.

Provides IP validation to verify webhook requests originate from YooKassa servers.
"""
import ipaddress
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# YooKassa IP ranges from official documentation
# https://yookassa.ru/developers/using-api/webhooks#ip
YOOKASSA_IP_RANGES = [
    '185.71.76.0/27',
    '185.71.77.0/27',
    '77.75.153.0/25',
    '77.75.156.224/28',
    '2a02:5180::/32',
]


def get_client_ip(request):
    """
    Extract client IP address from request, handling reverse proxies.

    Checks X-Forwarded-For header first (for requests through Nginx/load balancer),
    then falls back to REMOTE_ADDR.

    Args:
        request: Django HttpRequest object

    Returns:
        str: Client IP address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Take first IP (original client) from comma-separated list
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_valid_yookassa_ip(ip_string):
    """
    Check if IP address is from YooKassa's known ranges.

    In DEBUG mode, all IPs are accepted to facilitate local testing.

    Args:
        ip_string: IP address as string

    Returns:
        bool: True if IP is valid YooKassa source, False otherwise
    """
    # Skip validation in DEBUG mode for local testing
    if settings.DEBUG:
        logger.debug(f"DEBUG mode: Skipping IP validation for {ip_string}")
        return True

    try:
        client_ip = ipaddress.ip_address(ip_string)
        for cidr in YOOKASSA_IP_RANGES:
            if client_ip in ipaddress.ip_network(cidr):
                return True
        return False
    except ValueError as e:
        logger.warning(f"Invalid IP address format: {ip_string} - {e}")
        return False
