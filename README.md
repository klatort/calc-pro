# Calc-Pro - Automatización de calculadora HWC

Desarrollo con Node 20.9 y Python 3.10

## 🚀 Despliegue con Docker

### Opción 1: Docker Compose (Recomendado)

1. Clona el repositorio:
```bash
git clone <repository-url>
cd calc-pro
```

2. Crea un archivo `.env` basado en `.env.example`:
```bash
cp .env.example .env
```

3. Edita `.env` con tus valores personalizados (opcional):
```env
PORT=8000
WORKERS=4
LOG_LEVEL=info
NGINX_PORT=80
```

4. Construye y ejecuta los contenedores:
```bash
docker-compose up -d --build
```

5. Accede a la aplicación:
   - Frontend: http://localhost:80
   - Backend API: http://localhost:8000

### Opción 2: Docker Manual

#### Backend

1. Navega al directorio del backend:
```bash
cd backend
```

2. Construye la imagen:
```bash
docker build -t calc-pro-backend .
```

3. Ejecuta el contenedor con variables de entorno:
```bash
docker run -d \
  -p 8000:8000 \
  -e PORT=8000 \
  -e WORKERS=4 \
  -e LOG_LEVEL=info \
  -e UPLOAD_FOLDER=/app/uploads \
  -e WINDOWS_PRICES_DIR=/app/data/windows_prices.xlsx \
  -e LINUX_PRICES_DIR=/app/data/RI_linux_prices.xlsx \
  -v $(pwd)/data:/app/data \
  --name calc-pro-backend \
  calc-pro-backend
```

#### Frontend

1. Construye la aplicación Angular:
```bash
cd frontend
npm install
npm run build
```

2. Construye la imagen Docker:
```bash
docker build -t calc-pro-frontend .
```

3. Ejecuta el contenedor con variables de entorno:
```bash
docker run -d \
  -p 80:80 \
  -e BACKEND_URL=http://backend:8000 \
  --name calc-pro-frontend \
  calc-pro-frontend
```

## 📋 Variables de Entorno

### Backend

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `PORT` | Puerto donde se ejecuta el backend | `8000` |
| `WORKERS` | Número de workers de Gunicorn | `4` |
| `LOG_LEVEL` | Nivel de logging (debug, info, warning, error) | `info` |
| `UPLOAD_FOLDER` | Directorio para archivos subidos | `/app/uploads` |
| `WINDOWS_PRICES_DIR` | Ruta al archivo de precios Windows | `/app/data/windows_prices.xlsx` |
| `LINUX_PRICES_DIR` | Ruta al archivo de precios Linux | `/app/data/RI_linux_prices.xlsx` |

### Frontend

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `BACKEND_URL` | URL del backend API | `http://localhost:8000` |
| `NGINX_PORT` | Puerto donde se ejecuta Nginx | `80` |

## 🔧 Configuración para Diferentes Entornos

### Desarrollo Local

Crea un archivo `.env`:
```env
PORT=8000
WORKERS=2
LOG_LEVEL=debug
NGINX_PORT=8080
```

### Producción

Crea un archivo `.env.production`:
```env
PORT=8000
WORKERS=8
LOG_LEVEL=warning
NGINX_PORT=80
BACKEND_URL=http://your-backend-domain.com:8000
```

Luego ejecuta:
```bash
docker-compose --env-file .env.production up -d --build
```

## 🌐 Despliegue en Servidor Remoto

1. Actualiza el archivo `.env` con la IP/dominio de tu servidor:
```env
BACKEND_URL=http://101.44.10.234:8000
```

2. Construye y despliega:
```bash
docker-compose up -d --build
```

## 📁 Estructura del Proyecto

```
calc-pro/
├── backend/
│   ├── app.py              # Aplicación Flask principal
│   ├── config.py           # Configuración con soporte para env vars
│   ├── dockerfile          # Dockerfile con variables de entorno
│   ├── requirements.txt    # Dependencias Python
│   ├── data/              # Archivos de datos (precios)
│   ├── routes/            # Endpoints de la API
│   └── services/          # Lógica de negocio
├── frontend/
│   ├── src/               # Código fuente Angular
│   ├── dockerfile         # Dockerfile con variables de entorno
│   ├── default            # Configuración Nginx (template)
│   └── package.json       # Dependencias Node
├── docker-compose.yml     # Orquestación de contenedores
└── .env.example          # Ejemplo de variables de entorno
```

## 🛠️ Comandos Útiles

### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo backend
docker-compose logs -f backend

# Solo frontend
docker-compose logs -f frontend
```

### Detener servicios
```bash
docker-compose down
```

### Reconstruir después de cambios
```bash
docker-compose up -d --build
```

### Limpiar todo (incluyendo volúmenes)
```bash
docker-compose down -v
```

## 🔒 Notas de Seguridad

- Nunca commitees archivos `.env` con valores de producción
- Usa `.env.example` como plantilla
- Cambia los valores por defecto en producción
- Considera usar Docker secrets para datos sensibles

## 💡 Beneficios de Esta Configuración

✅ **Portabilidad**: Ejecuta en cualquier entorno solo cambiando variables  
✅ **Flexibilidad**: Ajusta configuración sin modificar código  
✅ **Seguridad**: Separa configuración sensible del código  
✅ **Escalabilidad**: Fácil de ajustar workers y recursos  
✅ **Desarrollo**: Diferentes configuraciones para dev/staging/prod

---

¡Disfruta no tirarte un día en calculadoras! 🎉