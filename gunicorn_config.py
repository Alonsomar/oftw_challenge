# Configuración para mejor manejo de recursos
workers = 1  # Número de workers
threads = 1  # Threads por worker
worker_class = 'gthread'  # Usar threads
worker_connections = 1000
timeout = 300
keepalive = 2