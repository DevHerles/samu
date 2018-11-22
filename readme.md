# oehealth_renipress

Cliente para mantener atualizados los datos del establecimiento.

# Dependencias

oehealth

# Instalación

Instale el addon `oehealth_renipress`

# Configuración de parámetros de sistema

Llave | Descripción
-----|-----
minsacatalogos_api_host| Direción url del servidor Minsa catálogos
minsacatalogos_api_token | Token


# Uso

```python

res_renipress = self.env["oehealth_fua.eess'].get_numero_fua(codigo_ipress)

```

