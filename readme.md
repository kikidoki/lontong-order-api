# Lontong Order API

A Django REST API for managing lontong (rice cake) orders with JWT authentication and WhatsApp integration. 
Built to assist my mom and her team in managing customer orders and communication around Eid Adha 2025.
🔗 Planned frontend integration: https://lontongjembatan.vercel.app

## Features

- JWT authentication for admin access
- CRUD operations for orders
- Automatic price calculation
- WhatsApp integration for order communication
- PostgreSQL database (Railway)
- Deployed on Vercel

## API Endpoints

### Authentication

- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

### Orders

- `GET /api/orders/`: List all orders (admin only)
- `POST /api/orders/`: Create a new order (public)
- `GET /api/orders/{id}/`: Retrieve an order (admin only)
- `PUT /api/orders/{id}/`: Update an order (admin only)
- `DELETE /api/orders/{id}/`: Delete an order (admin only)
- `POST /api/orders/{id}/send_whatsapp/`: Generate WhatsApp link (admin only)

## Local Development

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file based on `.env.example`
6. Run migrations: `python manage.py makemigrations orders` and `python manage.py migrate`
7. Create admin user: `python manage.py create_admin`
8. Run the development server: `python manage.py runserver`

## Deployment

This project is configured for deployment on Vercel with a PostgreSQL database on Railway.

### Railway Setup

1. Create a PostgreSQL database on Railway
2. Get the connection URL

### Vercel Setup

1. Connect this GitHub repository to Vercel
2. Add the following environment variables:
   - `DATABASE_URL`: Your Railway PostgreSQL connection URL
   - `SECRET_KEY`: A secure random string
   - `ADMIN_USERNAME`: Admin username
   - `ADMIN_EMAIL`: Admin email
   - `ADMIN_PASSWORD`: Admin password
3. Deploy!
\`\`\`

## Step 9: Deployment Instructions

Now that we have all the files ready, here's how to deploy the project:

1. **Set up Railway PostgreSQL Database**:
   - Create an account on [Railway](https://railway.app/)
   - Create a new project
   - Add a PostgreSQL database
   - Get the connection URL from the "Connect" tab

2. **Create a GitHub Repository**:
   - Create a new repository on GitHub
   - Push all this files to the repository

3. **Deploy to Vercel**:
   - Create an account on [Vercel](https://vercel.com/)
   - Import your GitHub repository
   - Add the following environment variables:
     - `DATABASE_URL`: Your Railway PostgreSQL connection URL
     - `SECRET_KEY`: A secure random string
     - `ADMIN_USERNAME`: Admin username
     - `ADMIN_EMAIL`: Admin email
     - `ADMIN_PASSWORD`: Admin password
   - Deploy the project

4. **Test the API**:
   - Get JWT token: `POST https://your-vercel-url.vercel.app/api/token/`
   - Create an order: `POST https://your-vercel-url.vercel.app/api/orders/`
   - List orders (with JWT): `GET https://your-vercel-url.vercel.app/api/orders/`

## Example API Usage

### Create an Order (Public)

\`\`\`bash
curl -X POST https://your-vercel-url.vercel.app/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "+6281234567890",
    "name": "John Doe",
    "address": "123 Main St, Jakarta",
    "total_lontong_large": 2,
    "total_lontong_small": 3
  }'
\`\`\`

### Get JWT Token (Admin)

\`\`\`bash
curl -X POST https://your-vercel-url.vercel.app/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "your-admin-password"
  }'
\`\`\`

### List All Orders (Admin)

\`\`\`bash
curl -X GET https://your-vercel-url.vercel.app/api/orders/ \
  -H "Authorization: Bearer your-jwt-token"
\`\`\`

This completes the setup of your Django REST API with JWT authentication, Railway PostgreSQL database, and Vercel deployment!

