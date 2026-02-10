import ipaddress
import socket
from urllib.parse import urlparse

import requests


# Rangos a bloquear
BLOCKED_NETS = [
    ipaddress.ip_network("127.0.0.0/8"),     # loopback
    ipaddress.ip_network("10.0.0.0/8"),      # private
    ipaddress.ip_network("172.16.0.0/12"),   # private
    ipaddress.ip_network("192.168.0.0/16"),  # private
    ipaddress.ip_network("169.254.0.0/16"),  # link-local
    ipaddress.ip_network("::1/128"),         # loopback v6
    ipaddress.ip_network("fc00::/7"),        # unique local v6
    ipaddress.ip_network("fe80::/10"),       # link-local v6
]

ALLOWED_SCHEMES = {"http", "https"}

def _resolve_host_to_ips(hostname: str) -> list[str]:
    # Devuelve IPs A y AAAA resueltas
    infos = socket.getaddrinfo(hostname, None)
    ips = []
    for family, _, _, _, sockaddr in infos:
        if family == socket.AF_INET:
            ips.append(sockaddr[0])
        elif family == socket.AF_INET6:
            ips.append(sockaddr[0])
    return list(sorted(set(ips)))

def _is_blocked_ip(ip_str: str) -> bool:
    ip = ipaddress.ip_address(ip_str)
    return any(ip in net for net in BLOCKED_NETS)

def safe_fetch(url: str) -> dict:
    parsed = urlparse(url)

    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError("Scheme no permitido. Usa http/https.")

    if not parsed.hostname:
        raise ValueError("URL inválida (sin hostname).")

    # Evitar userinfo (http://user:pass@host)
    if parsed.username or parsed.password:
        raise ValueError("URL con credenciales embebidas no permitida.")

    # Resolver DNS y bloquear si cualquier IP cae en rangos internos
    ips = _resolve_host_to_ips(parsed.hostname)
    if not ips:
        raise ValueError("No se pudo resolver el hostname.")

    for ip in ips:
        if _is_blocked_ip(ip):
            raise ValueError(f"Acceso bloqueado: destino resuelve a IP interna ({ip}).")

    # Endurecer request: sin redirects, timeout corto
    r = requests.get(url, timeout=5, allow_redirects=False)

    return {
        "requested_url": url,
        "resolved_ips": ips,
        "status_code": r.status_code,
        "content_type": r.headers.get("content-type"),
        "body_preview": r.text[:2000],
        "note": "Fetch con validación SSRF (bloqueo de IPs internas + sin redirects).",
    }
