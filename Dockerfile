# Usar imagen base ligera de Python
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar y instalar dependencias
COPY requirements.in requirements.in
RUN pip install --no-cache-dir -r requirements.in

# Copiar el resto del código
COPY . .

# Exponer el puerto 8050 (interno de Dash)
EXPOSE 8050

# Comando para ejecutar Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "app:server"]