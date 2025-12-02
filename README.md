# NextShare 📸

A modern social media platform for sharing images and videos with a clean, intuitive interface. Built with FastAPI backend and Streamlit frontend, featuring user authentication, media uploads, and a real-time feed.

## ✨ Features

- **User Authentication**: Secure JWT-based authentication with registration, login, and password reset
- **Media Sharing**: Upload and share images and videos with captions
- **Real-time Feed**: View posts from all users in chronological order
- **Media Processing**: Automatic image/video optimization using ImageKit
- **User Management**: Profile management and post ownership controls
- **Responsive UI**: Clean, modern interface built with Streamlit

## 🛠️ Tech Stack

### Backend

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM with async support
- **FastAPI Users**: Complete user management system
- **SQLite**: Lightweight database (easily switchable to PostgreSQL)
- **ImageKit**: Cloud-based image and video optimization
- **Uvicorn**: ASGI server for running the FastAPI application

### Frontend

- **Streamlit**: Interactive web app framework
- **Requests**: HTTP library for API communication

## 📁 Project Structure

```
NextShare/
├── app/
│   ├── app.py          # Main FastAPI application
│   ├── db.py           # Database models and configuration
│   ├── schemas.py      # Pydantic schemas for API
│   ├── users.py        # User authentication and management
│   └── images.py       # ImageKit configuration
├── frontend.py         # Streamlit frontend application
├── main.py            # Application entry point
├── pyproject.toml     # Project dependencies and metadata
├── .env               # Environment variables (not in repo)
└── README.md          # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- ImageKit account (for media processing)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd NextShare
   ```

2. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync

   # Or using pip
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   Create a `.env` file in the root directory:

   ```env
   # ImageKit Configuration
   IMAGEKIT_PRIVATE_KEY=your_imagekit_private_key
   IMAGEKIT_PUBLIC_KEY=your_imagekit_public_key
   IMAGEKIT_URL=your_imagekit_url_endpoint

   # JWT Secret (generate a secure random string)
   SECRET=your_jwt_secret_key
   ```

4. **Run the backend server**

   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

5. **Run the frontend (in a separate terminal)**
   ```bash
   streamlit run frontend.py
   ```
   The web app will be available at `http://localhost:8501`

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint                | Description               |
| ------ | ----------------------- | ------------------------- |
| POST   | `/auth/register`        | Register a new user       |
| POST   | `/auth/jwt/login`       | Login and get JWT token   |
| POST   | `/auth/jwt/logout`      | Logout (invalidate token) |
| POST   | `/auth/forgot-password` | Request password reset    |
| POST   | `/auth/reset-password`  | Reset password with token |

### User Management

| Method | Endpoint           | Description                 |
| ------ | ------------------ | --------------------------- |
| GET    | `/users/me`        | Get current user profile    |
| PATCH  | `/users/me`        | Update current user profile |
| GET    | `/users/{user_id}` | Get user by ID              |

### Posts & Media

| Method | Endpoint           | Description                          |
| ------ | ------------------ | ------------------------------------ |
| POST   | `/upload`          | Upload image/video with caption      |
| GET    | `/feed`            | Get all posts in chronological order |
| DELETE | `/posts/{post_id}` | Delete a post (owner only)           |

### Example API Usage

**Register a new user:**

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
```

**Login:**

```bash
curl -X POST "http://localhost:8000/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword"
```

**Upload media:**

```bash
curl -X POST "http://localhost:8000/upload" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@image.jpg" \
  -F "caption=My awesome photo!"
```

## 🗄️ Database Schema

### Users Table

- `id`: UUID (Primary Key)
- `email`: String (Unique)
- `hashed_password`: String
- `is_active`: Boolean
- `is_superuser`: Boolean
- `is_verified`: Boolean

### Posts Table

- `id`: UUID (Primary Key)
- `user_id`: UUID (Foreign Key to Users)
- `caption`: Text
- `url`: String (ImageKit URL)
- `file_type`: String ("image" or "video")
- `file_name`: String
- `created_at`: DateTime

## 🔧 Configuration

### Environment Variables

| Variable               | Description                      | Required |
| ---------------------- | -------------------------------- | -------- |
| `IMAGEKIT_PRIVATE_KEY` | ImageKit private API key         | Yes      |
| `IMAGEKIT_PUBLIC_KEY`  | ImageKit public API key          | Yes      |
| `IMAGEKIT_URL`         | ImageKit URL endpoint            | Yes      |
| `SECRET`               | JWT secret key for token signing | Yes      |

### Database Configuration

By default, the application uses SQLite (`nextshare.db`). To use PostgreSQL:

1. Update the `DATABASE_URL` in `app/db.py`:

   ```python
   DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/nextshare"
   ```

2. Install PostgreSQL dependencies:
   ```bash
   pip install asyncpg psycopg2-binary
   ```

## 🎨 Frontend Features

The Streamlit frontend provides:

- **Authentication UI**: Login and registration forms
- **Upload Interface**: Drag-and-drop file upload with caption input
- **Feed Display**: Scrollable feed with media thumbnails and captions
- **User Controls**: Delete posts, logout functionality
- **Responsive Design**: Works on desktop and mobile devices

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt password hashing
- **User Verification**: Email verification system (configurable)
- **CORS Protection**: Configurable CORS settings
- **File Validation**: Media type and size validation
- **User Permissions**: Users can only delete their own posts

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use secure environment variable management
2. **Database**: Switch to PostgreSQL for production
3. **File Storage**: Consider using cloud storage for uploaded files
4. **SSL/TLS**: Enable HTTPS in production
5. **Rate Limiting**: Implement rate limiting for API endpoints
6. **Monitoring**: Add logging and monitoring

### Docker Deployment (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "main.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

**ImageKit Upload Fails**

- Verify your ImageKit credentials in `.env`
- Check file size limits (ImageKit has upload limits)
- Ensure file types are supported

**Database Connection Issues**

- Check if `nextshare.db` file has proper permissions
- For PostgreSQL, verify connection string and database exists

**Frontend Not Loading**

- Ensure backend is running on port 8000
- Check if Streamlit is installed correctly
- Verify API endpoints are accessible

## 📞 Support

For support and questions:

- Create an issue in the repository
- Check the API documentation at `http://localhost:8000/docs`
- Review the logs for error details

---

Built with ❤️ using FastAPI and Streamlit
