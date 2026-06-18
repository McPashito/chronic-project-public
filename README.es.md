# Chronic Project

[English](README.md) · Español

Aplicación full-stack para seguimiento de glucemias construida con FastAPI, PostgreSQL y Vue.

Chronic Project es una aplicación web full-stack orientada al seguimiento de glucemias.

El proyecto nace como Trabajo de Fin de Grado de DAW y se está preparando también como proyecto público de portfolio para un perfil junior backend / full-stack. El objetivo es mostrar una aplicación realista con autenticación, rutas protegidas, persistencia en PostgreSQL, reglas de negocio, frontend responsive y datos demo preparados para poder probarla.

> Este es un proyecto académico. No es un producto médico certificado y no debe utilizarse como consejo médico, diagnóstico ni herramienta de tratamiento.

## Contexto Del Proyecto

Chronic Project parte de una necesidad habitual en pacientes con patologías crónicas: registrar mediciones, consultar la información de forma ordenada y disponer de un historial claro que pueda ayudar en el seguimiento diario.

La idea inicial era más amplia y contemplaba el seguimiento de distintas patologías crónicas, como diabetes, hipertensión arterial y dislipemias. Para esta versión se decidió acotar el alcance al módulo de glucemias. Esta decisión permite presentar una funcionalidad completa, coherente y defendible, dejando la arquitectura preparada para futuras ampliaciones como tensión arterial, medicación, citas médicas o informes.

El desarrollo se planteó de forma incremental: primero una versión simple funcionando, después una versión técnicamente correcta y finalmente una interfaz clara, legible y usable.

## Funcionalidades Principales

- Registro e inicio de sesión con JWT.
- Contraseñas hasheadas con Passlib/bcrypt.
- Rutas privadas protegidas.
- CRUD de registros de glucemia.
- Registros asociados al usuario autenticado.
- Filtros por fecha y por momento del día.
- Dashboard y tarjetas resumen.
- Lógica demo Standard/Premium:
  - usuarios Standard: acceso al historial reciente;
  - usuarios Premium: acceso al historial completo.
- Perfil de usuario y cambio de contraseña.
- Modo oscuro en la zona privada.
- Diseño responsive para escritorio, tablet y móvil.
- Scripts de datos demo para pruebas locales y despliegue de portfolio.

## Capturas

### Inicio Público Y Dashboard Privado

<p>
  <img src="docs/screenshots/home.png" alt="Página de inicio pública de Chronic Project" width="49%">
  <img src="docs/screenshots/dashboard.png" alt="Dashboard privado con tarjetas de resumen de glucemias" width="49%">
</p>

### Glucemias Y Formulario

<p>
  <img src="docs/screenshots/glucose-records.png" alt="Tabla de glucemias y resumen del periodo seleccionado" width="49%">
  <img src="docs/screenshots/glucose-form.png" alt="Formulario modal para crear una glucemia" width="49%">
</p>

### Perfil Y Modo Oscuro

<p>
  <img src="docs/screenshots/profile.png" alt="Vista de perfil de usuario con resumen de salud" width="49%">
  <img src="docs/screenshots/dark-mode.png" alt="Dashboard en modo oscuro" width="49%">
</p>

### Diseño Responsive

![Vistas responsive en tablet y móvil](docs/screenshots/responsive-showcase.png)

## Stack Tecnológico

**Backend**

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- JWT
- Passlib/bcrypt

**Frontend**

- Vue.js
- Vite
- Vue Router
- JavaScript
- HTML y CSS

**Base de datos**

- PostgreSQL

## Estructura Del Proyecto

```text
chronic-project/
|-- backend/
|   |-- app/
|   |   |-- api/routes/
|   |   |-- core/
|   |   |-- db/
|   |   |-- models/
|   |   `-- schemas/
|   |-- alembic/
|   |-- scripts/
|   |-- alembic.ini
|   `-- requirements.txt
|-- frontend/
|   |-- src/
|   |   |-- components/
|   |   |-- layouts/
|   |   |-- router/
|   |   |-- services/
|   |   `-- views/
|   |-- package.json
|   `-- vite.config.js
`-- README.md
```

## Instalación Local

### 1. Clonar El Repositorio

```bash
git clone <repository-url>
cd chronic-project
```

### 2. Backend

```bash
cd backend
python -m venv .venv
```

Activar el entorno virtual.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Crear el archivo `.env` a partir del ejemplo:

```bash
cp .env.example .env
```

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Configurar la conexión local a PostgreSQL en `backend/.env`.

Aplicar migraciones:

```bash
alembic upgrade head
```

Arrancar el backend:

```bash
uvicorn app.main:app --reload
```

API local:

```text
http://127.0.0.1:8000
```

Documentación automática de FastAPI:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend

Abrir una segunda terminal:

```bash
cd frontend
npm install
```

Crear el archivo `.env` a partir del ejemplo:

```bash
cp .env.example .env
```

En Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Arrancar el frontend:

```bash
npm run dev
```

URL habitual:

```text
http://localhost:5173
```

## Variables De Entorno

### Backend

Ver `backend/.env.example`.

```env
DATABASE_URL=postgresql://user:password@localhost:5432/chronic_project_db
SECRET_KEY=change-this-secret-key
```

### Frontend

Ver `frontend/.env.example`.

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Los archivos `.env` reales están ignorados por Git y no deben subirse al repositorio público.

## Datos Demo

El proyecto incluye scripts de datos demo para facilitar pruebas locales y despliegues de portfolio.

Desde la carpeta `backend`, después de aplicar migraciones:

```bash
python scripts/seed_demo_data.py
```

Este comando crea:

- usuarios demo Standard;
- usuarios demo Premium;
- registros antiguos sin `moment_of_day`;
- registros nuevos con `moment_of_day`;
- valores variados para mostrar estados bajos, en rango, elevados y altos en la interfaz.

Credenciales demo:

```text
standard1@demo.com / Demo1234!
premium1@demo.com  / Demo1234!
```

Cuentas disponibles:

```text
standard1@demo.com ... standard10@demo.com
premium1@demo.com  ... premium10@demo.com
```

Los scripts demo están pensados solo para entornos de prueba o demostración. No deben utilizarse con datos reales.

## Comandos Útiles Del Backend

Aplicar migraciones:

```bash
alembic upgrade head
```

Crear datos demo:

```bash
python scripts/seed_demo_data.py
```

Actualizar solo los registros demo recientes:

```bash
python scripts/seed_new_glucose_records.py
```

Arrancar la API:

```bash
uvicorn app.main:app --reload
```

## Comandos Útiles Del Frontend

Instalar dependencias:

```bash
npm install
```

Servidor de desarrollo:

```bash
npm run dev
```

Build de producción:

```bash
npm run build
```

## Resumen De API

Endpoints públicos principales:

- `GET /`
- `GET /health`
- `POST /auth/register`
- `POST /auth/login`

Endpoints privados principales:

- `GET /users/me`
- `PUT /users/edit_user`
- `PUT /users/change_password`
- `POST /glucose-records/`
- `GET /glucose-records/`
- `GET /glucose-records/summary`
- `GET /glucose-records/{record_id}`
- `PUT /glucose-records/{record_id}`
- `DELETE /glucose-records/{record_id}`

La autenticación utiliza JWT:

```text
Authorization: Bearer <token>
```

El login utiliza formulario OAuth2. El frontend envía el email en el campo `username`.

## Decisiones Técnicas

### Registros Asociados Al Usuario

El frontend no envía `user_id` al crear una glucemia. El backend obtiene el usuario autenticado desde el token JWT y asigna la propiedad del registro en servidor.

Todas las consultas de glucemias filtran por usuario autenticado, evitando que un usuario pueda acceder a registros de otro.

### `moment_of_day` Como Campo Evolutivo

El proyecto empezó almacenando glucemias sin `moment_of_day`. Más adelante se añadió este campo mediante una migración de Alembic.

La base de datos permite `NULL` para conservar registros antiguos. Los nuevos registros, en cambio, requieren `moment_of_day` mediante validación de Pydantic.

Esta decisión mantiene compatibilidad histórica sin perder calidad en los datos nuevos.

### Lógica Demo Standard/Premium

La aplicación incluye una lógica sencilla de tipos de cuenta:

- usuarios Standard: pueden consultar registros recientes;
- usuarios Premium: pueden consultar todo el historial.

No hay pagos reales. Es una funcionalidad de portfolio para demostrar reglas de negocio y autorización.

### Simplicidad Visual

La interfaz prioriza tarjetas legibles, tablas filtrables y formularios claros en lugar de gráficas complejas. Esta decisión busca mejorar la lectura inmediata y la accesibilidad para un público amplio.

Las gráficas y exportaciones quedan como mejoras futuras.

## Notas De Despliegue

Despliegue público actual:

- Frontend: Vercel - https://chronic-project-public.vercel.app
- Backend: Render - https://chronic-project-public.onrender.com
- Base de datos: Neon PostgreSQL

Variables de entorno necesarias, sin valores reales:

- Backend en Render: `DATABASE_URL`, `SECRET_KEY`
- Frontend en Vercel: `VITE_API_BASE_URL`

Comando de producción para backend:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Antes del primer uso en una base de datos de despliegue:

```bash
alembic upgrade head
python scripts/seed_demo_data.py
```

Los datos demo recientes se pueden refrescar manualmente desde un entorno local configurado con la URL de la base de datos pública:

```bash
python scripts/seed_new_glucose_records.py
```

Se valoró activar un Render Cron Job diario, pero no se ha habilitado en el despliegue gratuito de portfolio porque añade coste de plataforma. El script queda preparado para ese escenario.

Si el frontend usa un dominio nuevo, el backend debe permitir ese origen en la configuración de CORS.

Más detalles: [Guía de despliegue](docs/deployment.md).

## Limitaciones Actuales

- No es un producto sanitario certificado.
- No hay sistema real de pagos.
- No hay recuperación de contraseña por email.
- Las gráficas y exportaciones CSV/PDF quedan como mejoras futuras.
- Los datos demo son artificiales y solo sirven para pruebas y presentación.

## Mejoras Futuras

- Tests automatizados para reglas principales del backend.
- Recuperación de contraseña.
- Gráficas de evolución glucémica.
- Exportación CSV/PDF.
- Extender el mismo patrón de módulo a otras mediciones relacionadas con patologías crónicas, como tensión arterial o registros vinculados a lípidos.
- Evolucionar el proyecto hacia una aplicación unificada de seguimiento crónico, manteniendo cada módulo simple y mantenible de forma independiente.
- Roles de cuenta más flexibles.
- Pipeline de despliegue y CI.
- Auditoría de accesibilidad más detallada.
