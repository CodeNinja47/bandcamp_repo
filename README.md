# Bandcamp - Music Publishing Platform

A simplified self-hosted music publishing and streaming platform inspired by Bandcamp.

## Project Overview

This platform allows independent artists to:
- Upload music tracks
- Organize tracks into releases/albums
- Automatically convert audio into multiple formats using FFmpeg
- Manage metadata
- Expose music through a REST API

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Django | Backend framework |
| Django REST Framework | REST API |
| PostgreSQL | Database |
| Redis | Message broker |
| Celery | Background jobs |
| FFmpeg | Audio processing |

## Project Structure

```
bandcamp_repo/
├── bandcamp/         → Project settings and URLs
├── users/            → User authentication and artist profiles
├── music/            → Tracks, genres, audio processing
├── releases/         → Albums, EPs, singles
└── manage.py         → Django management
```

## Setup Instructions

### Prerequisites
- Python 3.12
- PostgreSQL 18
- Redis
- FFmpeg

### Installation

**1. Clone the repository:**
```bash
git clone git@github.com:yourusername/bandcamp_repo.git
cd bandcamp_repo
```

**2. Create virtual environment:**
```bash
python3.12 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Install system dependencies:**
```bash
sudo apt install postgresql postgresql-contrib redis-server ffmpeg -y
```

**5. Setup PostgreSQL:**
```bash
sudo pg_ctlcluster 18 main start
sudo -u postgres psql
```
```sql
CREATE DATABASE bandcamp_db;
CREATE USER bandcamp_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE bandcamp_db TO bandcamp_user;
\connect bandcamp_db
GRANT ALL ON SCHEMA public TO bandcamp_user;
\q
```

**6. Configure settings:**

Update `bandcamp/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bandcamp_db',
        'USER': 'bandcamp_user',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**7. Run migrations:**
```bash
python manage.py migrate
```

**8. Create superuser:**
```bash
python manage.py createsuperuser
```

### Running the Application

**Start Redis:**
```bash
sudo service redis-server start
```

**Start Celery worker:**
```bash
celery -A bandcamp worker --loglevel=info
```

**Start Django server:**
```bash
python manage.py runserver 8080
```

## API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login | No |
| POST | `/api/auth/logout/` | Logout | Yes |
| GET/PUT | `/api/auth/profile/` | View/Update profile | Yes |
| POST | `/api/auth/password/change/` | Change password | Yes |
| POST | `/api/auth/password/reset/` | Request password reset | No |
| POST | `/api/auth/password/reset/confirm/<token>/` | Confirm password reset | No |

### Artist Profiles
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/artists/profile/create/` | Create artist profile | Yes |
| GET | `/api/artists/profile/` | View own profile | Yes |
| PUT | `/api/artists/profile/` | Update profile | Yes |
| DELETE | `/api/artists/profile/delete/` | Delete profile | Yes |
| GET | `/api/artists/` | List all artists | No |
| GET | `/api/artists/<id>/` | View artist | No |

### Music/Tracks
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/music/genres/` | List genres | Yes |
| POST | `/api/music/genres/` | Create genre | Yes |
| GET | `/api/music/tracks/` | List my tracks | Yes |
| POST | `/api/music/tracks/upload/` | Upload track | Yes |
| GET | `/api/music/tracks/<id>/` | Track detail | Yes |
| PUT | `/api/music/tracks/<id>/` | Update track | Yes |
| DELETE | `/api/music/tracks/<id>/` | Delete track | Yes |
| GET | `/api/music/tracks/<id>/metadata/` | Track metadata | Yes |
| GET | `/api/music/tracks/<id>/files/` | Track files | Yes |
| GET | `/api/music/tracks/<id>/jobs/` | Processing jobs | Yes |
| GET | `/api/music/public/tracks/` | Public tracks | No |

### Releases
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/releases/` | List my releases | Yes |
| POST | `/api/releases/create/` | Create release | Yes |
| GET | `/api/releases/<id>/` | Release detail | Yes |
| PUT | `/api/releases/<id>/` | Update release | Yes |
| DELETE | `/api/releases/<id>/` | Delete release | Yes |
| POST | `/api/releases/<id>/add-track/` | Add track | Yes |
| POST | `/api/releases/<id>/remove-track/` | Remove track | Yes |
| POST | `/api/releases/<id>/publish/` | Publish release | Yes |
| POST | `/api/releases/<id>/unpublish/` | Unpublish release | Yes |
| GET | `/api/releases/public/` | Public releases | No |
| GET | `/api/releases/public/<id>/` | Public release detail | No |

### Search
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/search/?q=query` | Search everything | No |
| GET | `/api/search/tracks/?q=query` | Search tracks | No |
| GET | `/api/search/artists/?q=query` | Search artists | No |
| GET | `/api/search/releases/?q=query` | Search releases | No |

## Audio Processing

When a track is uploaded:
1. Original file saved to `media/tracks/original/`
2. Celery creates 3 transcoding jobs (MP3, AAC, OGG)
3. FFmpeg converts audio in background
4. Transcoded files saved to `media/tracks/transcoded/`
5. Metadata extracted using ffprobe

## Supported Upload Formats
- WAV
- MP3
- FLAC
- AIFF

## Output Formats
- MP3 (320kbps)
- AAC (256kbps)
- OGG (192kbps)

## Admin Panel

Access Django admin panel at:
```
http://localhost:8080/admin/
```

Admin can:
- Manage all users
- Monitor transcoding jobs
- Retry failed jobs
- Moderate content
- Manage releases and tracks

## Branch Structure

```
main (stable)
└── dev (integration)
    ├── feature/djangomodels
    ├── feature/user-authentication
    ├── feature/artist-profiles
    ├── feature/track-upload
    ├── feature/audio-processing
    ├── feature/metadata-extraction
    ├── feature/releases-albums
    ├── feature/search
    └── feature/rest-api
```

## Success Criteria

- Artists can upload audio
- Tracks are automatically transcoded
- Releases can be published
- APIs expose music metadata
- Background jobs process media reliably
- Admins can manage the platform successfully



