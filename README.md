# Portfolio Management System

A comprehensive full-stack investment portfolio management application that allows users to track multiple assets, monitor transaction history, analyze portfolio performance, and manage investments in real-time. Built with modern technologies including FastAPI, PostgreSQL, Redis, and Next.js.

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Docker Setup](#-docker-setup)
- [Environment Variables](#-environment-variables)
- [API Documentation](#-api-documentation)
- [Database Schema](#-database-schema)
- [Frontend Features](#-frontend-features)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Authentication & Security
- **JWT-Based Authentication**: Secure token-based authentication with configurable expiration
- **OAuth 2.0 Integration**: Google Sign-In for seamless user onboarding
- **Email Verification**: Confirmation emails for account activation
- **Password Reset**: Secure password recovery via email tokens
- **WebAuthn/Passkey Support**: Biometric authentication for enhanced security
- **Argon2 Password Hashing**: Industry-standard password hashing algorithm

### Portfolio Management
- **Multi-Asset Support**: Track stocks, cryptocurrencies, bonds, ETFs, and more
- **Real-Time Portfolio Tracking**: View current holdings and asset allocation
- **Asset Categories**: Organize investments by type and category
- **Portfolio Overview**: Visual summary of total portfolio value and distribution

### Transaction Management
- **Buy/Sell Transactions**: Record investment purchases and sales
- **Automatic Updates**: Transactions automatically update portfolio metrics
- **Transaction History**: Complete audit trail of all investment activities
- **Realized Gains/Losses**: Automatic calculation of profits and losses
- **Transaction Details**: Store price, quantity, date, and additional remarks

### Analytics & Dashboard
- **Real-Time Dashboard**: Interactive charts and visual portfolio analytics
- **Performance Metrics**: Track overall portfolio performance and returns
- **Asset Performance**: Individual asset profit/loss tracking
- **Interactive Charts**: Recharts-based visualizations for data insights
- **PDF Export**: Download portfolio reports as PDF documents

### Performance Optimization
- **Redis Caching**: In-memory caching for rapid API responses
- **Intelligent Cache Invalidation**: Automatic cache updates on data changes
- **Database Indexing**: Optimized queries for fast data retrieval
- **Async Processing**: Non-blocking operations for improved responsiveness

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** (v0.109.0): Modern, fast Python web framework with automatic API documentation
- **PostgreSQL** (v15): Robust relational database for data persistence
- **Redis** (v7-alpine): In-memory data store for caching and session management
- **SQLAlchemy** (v2.0.25): Powerful ORM for database operations
- **Pydantic** (v2.5.3): Data validation using Python type annotations
- **Alembic** (v1.13.1): Database migration tool
- **Authlib** (v1.3.0): OAuth 2.0 and JWT authentication library
- **python-jose** (v3.3.0): JWT implementation for secure tokens
- **passlib + argon2**: Password hashing and verification

### Frontend
- **Next.js** (v14.1.0): React framework for production applications
- **React** (v18.2.0): UI component library
- **TypeScript** (v5): Type-safe JavaScript development
- **Tailwind CSS** (v3.4.1): Utility-first CSS framework
- **Recharts** (v2.15.4): React charting library for data visualization
- **Axios** (v1.6.5): HTTP client for API communication
- **jsPDF + jsPDF-AutoTable**: PDF generation and table creation

### Infrastructure
- **Docker**: Containerization for consistent deployment
- **Docker Compose**: Multi-container orchestration
- **Uvicorn**: ASGI server for running FastAPI applications

---

## 📁 Project Structure

```
assessment/
├── backend/                      # FastAPI backend application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application initialization
│   │   ├── auth.py              # Authentication utilities
│   │   ├── database.py          # Database configuration and session
│   │   ├── redis_client.py      # Redis connection and caching
│   │   ├── models/              # SQLAlchemy ORM models
│   │   │   ├── user.py          # User model with auth fields
│   │   │   ├── asset.py         # Asset/Investment model
│   │   │   └── transaction.py   # Transaction model
│   │   ├── routers/             # API endpoint routes
│   │   │   ├── auth.py          # Authentication endpoints
│   │   │   ├── assets.py        # Asset management endpoints
│   │   │   ├── transactions.py  # Transaction endpoints
│   │   │   └── portfolio.py     # Portfolio analytics endpoints
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   │   ├── user.py
│   │   │   ├── asset.py
│   │   │   └── transaction.py
│   │   └── utils/               # Utility functions
│   │       ├── email.py         # Email sending functionality
│   │       ├── oauth.py         # OAuth 2.0 integration
│   │       ├── stock_data.py    # Stock price data fetching
│   │       └── stock_search.py  # Stock symbol search
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile               # Docker image for backend
│   ├── migrate_db.py            # Initial database migration
│   ├── backfill_realized_gains.py # Data backfill utility
│   └── [other migrations]       # Additional database migrations
│
├── frontend/                     # Next.js frontend application
│   ├── app/
│   │   ├── layout.tsx           # Root layout component
│   │   ├── page.tsx             # Home/login page
│   │   ├── globals.css          # Global styles
│   │   ├── dashboard/           # Dashboard page
│   │   ├── transactions/        # Transactions page
│   │   ├── profile/             # User profile page
│   │   ├── login/               # Login page
│   │   ├── forgot-password/     # Password recovery page
│   │   ├── reset-password/      # Password reset page
│   │   └── verify-email/        # Email verification page
│   ├── components/              # Reusable React components
│   │   └── TransactionDetailModal.tsx
│   ├── lib/
│   │   ├── api.ts              # API client utilities
│   │   └── pdfExport.ts        # PDF export functionality
│   ├── public/                  # Static assets
│   ├── package.json             # Node.js dependencies
│   ├── tsconfig.json            # TypeScript configuration
│   ├── tailwind.config.js       # Tailwind CSS configuration
│   ├── next.config.js           # Next.js configuration
│   ├── postcss.config.js        # PostCSS configuration
│   ├── Dockerfile               # Docker image for frontend
│   └── next-env.d.ts            # Next.js type definitions
│
├── docker-compose.yml           # Multi-container setup
└── README.md                    # This file
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16+) - For frontend development
- **Python** (v3.9+) - For backend development
- **Docker & Docker Compose** - For containerized deployment
- **PostgreSQL** (v15+) - For database
- **Redis** (v7+) - For caching
- **Git** - For version control

### Optional
- **Postman** or **Insomnia** - For API testing
- **VS Code** with extensions:
  - Python
  - Pylance
  - ESLint
  - Prettier

---

## ⚙️ Installation & Setup

### Backend Setup (Local Development)

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (see [Environment Variables](#-environment-variables))
   ```bash
   cp .env.example .env
   ```

5. **Run database migrations**
   ```bash
   python migrate_db.py
   ```

6. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Frontend Setup (Local Development)

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.local.example .env.local
   ```

4. **Start the development server**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:3000`

---

## 🐳 Docker Setup

The easiest way to run the entire application stack locally is using Docker Compose.

### Prerequisites
- Docker installed and running
- Docker Compose installed

### Running the Application

1. **Clone the repository**
   ```bash
   git clone https://github.com/recycolingbin/Assessment.git
   cd Assessment
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - PostgreSQL database (port 5432)
   - Redis cache (port 6379)
   - Backend API (port 8000)
   - Frontend (port 3000)

3. **Access the application**
   - Frontend: `http://localhost:3000`
   - Backend API: `http://localhost:8000`
   - API Documentation: `http://localhost:8000/docs`

4. **Stop the services**
   ```bash
   docker-compose down
   ```

5. **View logs**
   ```bash
   docker-compose logs -f [service-name]
   # Examples:
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

---

## 🔐 Environment Variables

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=postgresql://portfolio_user:portfolio_pass@localhost:5432/portfolio

# Redis
REDIS_URL=redis://localhost:6379

# JWT Configuration
SECRET_KEY=your-secret-key-here-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
FRONTEND_URL=http://localhost:3000

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# API Keys (Optional)
ALPHA_VANTAGE_API_KEY=your-alpha-vantage-key
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_GOOGLE_CLIENT_ID=your-google-client-id
```

### Obtaining API Credentials

#### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API
4. Create OAuth 2.0 credentials (Web application)
5. Add authorized redirect URIs:
   - `http://localhost:3000/auth/google/callback`
   - `http://localhost:8000/auth/google/callback`

#### Gmail SMTP
1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Use the App Password in `SMTP_PASSWORD`

---

## 📚 API Documentation

### Base URL
- Local: `http://localhost:8000`
- Production: `https://your-api-domain.com`

### Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <your-jwt-token>
```

### Main Endpoints

#### Authentication Routes

- `POST /auth/register` - Register a new user
  ```json
  {
    "email": "user@example.com",
    "username": "username",
    "password": "securepassword"
  }
  ```

- `POST /auth/login` - Login user
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```

- `POST /auth/google` - Google OAuth login
- `POST /auth/forgot-password` - Request password reset
- `POST /auth/reset-password` - Reset password with token
- `POST /auth/verify-email` - Verify email address

#### Asset Routes

- `GET /assets/` - Get all user assets
- `POST /assets/` - Create new asset
  ```json
  {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "category": "stock",
    "quantity": 10,
    "average_price": 150.50
  }
  ```
- `GET /assets/{asset_id}` - Get asset details
- `PUT /assets/{asset_id}` - Update asset
- `DELETE /assets/{asset_id}` - Delete asset

#### Transaction Routes

- `GET /transactions/` - Get all transactions
- `POST /transactions/` - Create new transaction
  ```json
  {
    "asset_id": 1,
    "transaction_type": "buy",
    "quantity": 5,
    "price": 150.00,
    "transaction_date": "2024-01-15",
    "remarks": "Quarterly investment"
  }
  ```
- `GET /transactions/{transaction_id}` - Get transaction details
- `PUT /transactions/{transaction_id}` - Update transaction
- `DELETE /transactions/{transaction_id}` - Delete transaction

#### Portfolio Routes

- `GET /portfolio/summary` - Get portfolio overview
- `GET /portfolio/performance` - Get performance metrics
- `GET /portfolio/asset-breakdown` - Get asset allocation breakdown

### Interactive API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 💾 Database Schema

### Users Table
```
users
├── id (PK)
├── email (UNIQUE)
├── username (UNIQUE)
├── hashed_password
├── is_verified
├── verification_token
├── reset_token
├── google_id
├── oauth_provider
├── full_name
├── phone
├── avatar_url
├── created_at
└── webauthn_credentials
```

### Assets Table
```
assets
├── id (PK)
├── owner_id (FK → users)
├── symbol
├── name
├── category
├── quantity
├── average_price
├── current_price
├── created_at
└── updated_at
```

### Transactions Table
```
transactions
├── id (PK)
├── user_id (FK → users)
├── asset_id (FK → assets)
├── transaction_type (buy/sell)
├── quantity
├── price
├── transaction_date
├── realized_gain_loss
├── remarks
├── created_at
└── updated_at
```

---

## 🎨 Frontend Features

### Pages

1. **Login/Registration Page**
   - Email/password registration
   - Google OAuth integration
   - "Forgot Password" link
   - Responsive design with gradient background

2. **Dashboard**
   - Real-time portfolio summary
   - Asset distribution charts
   - Performance metrics
   - Quick action buttons

3. **Assets Page**
   - View all holdings
   - Add/edit/delete assets
   - Asset details and performance

4. **Transactions Page**
   - View transaction history
   - Add buy/sell transactions
   - Transaction detail modal
   - Filter and search functionality

5. **Profile Page**
   - User information
   - Account settings
   - Preferences
   - Logout functionality

6. **Additional Pages**
   - Email verification page
   - Password reset flow
   - Password recovery page

### UI Components

- **TransactionDetailModal**: Detailed view of transaction information
- **Charts**: Recharts-based visualizations
- **Responsive Layout**: Mobile-friendly design with Tailwind CSS
- **Loading States**: Smooth loading indicators
- **Error Handling**: User-friendly error messages

### PDF Export

Users can export their portfolio report as a PDF including:
- Portfolio summary
- Asset holdings
- Transaction history
- Performance metrics

---

## 🚀 Development

### Code Structure

#### Backend
- **Models**: SQLAlchemy ORM definitions
- **Schemas**: Pydantic validation schemas
- **Routers**: API endpoint definitions
- **Services**: Business logic (in `/services`)
- **Utils**: Helper functions for common tasks

#### Frontend
- **App**: Next.js pages using App Router
- **Components**: Reusable React components
- **Lib**: Utilities for API calls and exports
- **Public**: Static assets

### Running Tests

Backend testing (example):
```bash
cd backend
pytest tests/
```

Frontend testing:
```bash
cd frontend
npm run test
```

### Building for Production

#### Backend
```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm run build
npm start
```

### Database Migrations

To create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
Error: could not connect to server
```
**Solution**:
- Ensure PostgreSQL is running: `docker-compose ps`
- Check DATABASE_URL in .env file
- Verify database credentials

#### 2. CORS Error in Frontend
```
Access to XMLHttpRequest blocked by CORS policy
```
**Solution**:
- Ensure `FRONTEND_URL` in backend .env matches frontend URL
- Check CORS middleware configuration in `app/main.py`

#### 3. Redis Connection Error
```
Error: Cannot connect to Redis
```
**Solution**:
- Ensure Redis is running: `docker-compose ps`
- Check `REDIS_URL` in .env file
- Verify Redis container health: `docker-compose logs redis`

#### 4. Google OAuth Not Working
```
Invalid client ID or client secret
```
**Solution**:
- Verify Google credentials in .env
- Check authorized redirect URIs in Google Cloud Console
- Ensure HTTPS is used in production

#### 5. Port Already in Use
```
Port 8000 is already in use
```
**Solution**:
```bash
# Find process using port
lsof -i :8000
# Kill process
kill -9 <PID>
# Or use different port
uvicorn app.main:app --port 8001
```

### Debug Mode

#### Backend
```bash
cd backend
uvicorn app.main:app --reload --log-level debug
```

#### Frontend
```bash
cd frontend
npm run dev
```

Both support hot-reload during development.

---

## 📝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Commit with clear messages: `git commit -m "Add feature description"`
5. Push to your branch: `git push origin feature/your-feature`
6. Submit a Pull Request

### Code Style

- **Python**: Follow PEP 8 (use `black` for formatting)
- **TypeScript/React**: Follow ESLint configuration
- **Commits**: Use clear, descriptive commit messages

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact the development team
- Check existing documentation

---

## 🔄 Version History

- **v1.0.0** (Current) - Initial release
  - User authentication with JWT and OAuth
  - Portfolio and asset management
  - Transaction tracking
  - Performance analytics
  - PDF export functionality

---

**Last Updated**: May 2026
**Maintained by**: Development Team
- **JWT**: Secure authentication

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **TailwindCSS**: Utility-first CSS framework
- **Recharts**: Data visualization library
- **Axios**: HTTP client

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Ports 3000, 8000, 5432, and 6379 available

### Running the Application

1. Clone the repository:
```bash
git clone <repository-url>
cd assessment
```

2. Start all services with Docker Compose:
```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### First Time Setup

1. Open http://localhost:3000
2. Click "Sign up" to create a new account
3. Login with your credentials
4. Start adding assets and transactions!

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `POST /auth/token` - OAuth2 compatible token endpoint

### Portfolio
- `GET /portfolio/overview` - Get portfolio summary with caching

### Assets
- `GET /assets/` - List all user assets
- `POST /assets/` - Create new asset
- `GET /assets/{id}` - Get specific asset
- `PUT /assets/{id}` - Update asset
- `DELETE /assets/{id}` - Delete asset

### Transactions
- `GET /transactions/` - List transactions (paginated)
- `POST /transactions/` - Create new transaction
- `GET /transactions/{id}` - Get specific transaction

## Architecture Highlights

### Backend Design
- **Async/Await**: FastAPI's async capabilities for high performance
- **Connection Pooling**: Efficient database connections
- **Redis Caching**: 5-minute TTL on portfolio overview
- **Cache Invalidation**: Automatic cache clearing on data changes
- **ACID Transactions**: Guaranteed data consistency

### Frontend Design
- **Client-Side Rendering**: Fast, interactive UI
- **Token-based Auth**: Secure localStorage token management
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Immediate UI updates after actions

### Security Features
- **Password Hashing**: bcrypt for secure password storage
- **JWT Tokens**: Stateless authentication
- **CORS Configuration**: Controlled cross-origin access
- **SQL Injection Prevention**: SQLAlchemy parameterized queries

## Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Database Migrations
The application automatically creates tables on startup. For production, consider using Alembic for migrations.

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://portfolio_user:portfolio_pass@postgres:5432/portfolio
REDIS_URL=redis://redis:6379
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Performance Optimizations

1. **Redis Caching**: Portfolio overview cached for 5 minutes
2. **Database Indexing**: Indexes on user_id, email, symbol
3. **Connection Pooling**: Reused database connections
4. **Async Operations**: Non-blocking I/O operations
5. **Pagination**: Transaction history with skip/limit

## Scalability Considerations

- **Horizontal Scaling**: Stateless backend can scale horizontally
- **Database Replication**: PostgreSQL supports read replicas
- **Redis Cluster**: Can be configured for high availability
- **Load Balancing**: Multiple backend instances behind load balancer
- **CDN**: Static frontend assets can be served via CDN

## Testing

### Manual Testing Flow
1. Register a new user
2. Add assets (e.g., AAPL, BTC, TSLA)
3. Create buy transactions
4. View portfolio overview and charts
5. Create sell transactions
6. Verify profit/loss calculations

### API Testing
Use the interactive API documentation at http://localhost:8000/docs

## Troubleshooting

### Port Already in Use
```bash
# Stop existing containers
docker-compose down

# Check for processes using ports
lsof -i :3000
lsof -i :8000
```

### Database Connection Issues
```bash
# Check PostgreSQL logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Cache Issues
```bash
# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL
```

## Future Enhancements

- Real-time price updates via external API (Alpha Vantage, CoinGecko)
- Advanced charts (line charts for historical performance)
- Export portfolio to CSV/PDF
- Multi-currency support
- Asset allocation recommendations
- Email notifications for price alerts
- Mobile app (React Native)

## License

MIT License

## Contact

For questions or support, please open an issue in the repository.
