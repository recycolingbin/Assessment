# Portfolio Management System

A full-stack portfolio management application built with FastAPI, PostgreSQL, Redis, and Next.js.

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Portfolio Management**: Track multiple assets (stocks, crypto, bonds, ETFs)
- **Transaction History**: Record buy/sell transactions with automatic portfolio updates
- **Real-time Dashboard**: Visual portfolio overview with charts and statistics
- **Performance Tracking**: Monitor profit/loss for individual assets and overall portfolio
- **Redis Caching**: Fast API responses with intelligent cache invalidation

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **PostgreSQL**: Relational database for data integrity
- **Redis**: In-memory cache for improved performance
- **SQLAlchemy**: ORM for database operations
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
