
-- ================================================
-- Bandcamp Database Schema
-- ================================================

-- Drop tables if they exist (clean start)
DROP TABLE IF EXISTS music_processingjob CASCADE;
DROP TABLE IF EXISTS music_trackfile CASCADE;
DROP TABLE IF EXISTS music_track CASCADE;
DROP TABLE IF EXISTS music_release_genre CASCADE;
DROP TABLE IF EXISTS music_release CASCADE;
DROP TABLE IF EXISTS music_genre CASCADE;
DROP TABLE IF EXISTS users_artistprofile CASCADE;
DROP TABLE IF EXISTS users_user CASCADE;

-- 1. USERS TABLE
CREATE TABLE users_user (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    username VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    role VARCHAR(10) NOT NULL DEFAULT 'artist',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Constraints
    CONSTRAINT role_choices CHECK (role IN ('artist', 'admin')),
    CONSTRAINT email_format CHECK (email LIKE '%@%.%')
);

-- 2. ARTIST PROFILE TABLE
CREATE TABLE users_artistprofile (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT UNIQUE NOT NULL,
    artist_name VARCHAR(255) NOT NULL,
    bio TEXT,
    profile_image VARCHAR(255),
    social_links JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Constraints
    FOREIGN KEY (user_id)
        REFERENCES users_user(id)
        ON DELETE CASCADE
);

-- Trigger to enforce only artists can have profiles
CREATE OR REPLACE FUNCTION check_artist_role()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT role FROM users_user WHERE id = NEW.user_id) != 'artist' THEN
        RAISE EXCEPTION 'Only users with artist role can have an artist profile!';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_artist_role
    BEFORE INSERT OR UPDATE ON users_artistprofile
    FOR EACH ROW
    EXECUTE FUNCTION check_artist_role();

-- 3. GENRE TABLE
CREATE TABLE music_genre (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,

    -- Constraints
    CONSTRAINT name_not_empty CHECK (LENGTH(TRIM(name)) > 0),
    CONSTRAINT slug_not_empty CHECK (LENGTH(TRIM(slug)) > 0)
);

-- 4. RELEASE TABLE
CREATE TABLE music_release (
    id BIGSERIAL PRIMARY KEY,
    artist_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    release_type VARCHAR(10) NOT NULL DEFAULT 'album',
    release_date DATE,
    cover_artwork VARCHAR(255),
    visibility VARCHAR(10) NOT NULL DEFAULT 'private',
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Constraints
    FOREIGN KEY (artist_id)
        REFERENCES users_artistprofile(id)
        ON DELETE CASCADE,
    CONSTRAINT release_type_choices CHECK (
        release_type IN ('album', 'ep', 'single')
    ),
    CONSTRAINT visibility_choices CHECK (
        visibility IN ('public', 'private')
    ),
    CONSTRAINT unique_release_per_artist UNIQUE (artist_id, title),
    CONSTRAINT title_not_empty CHECK (LENGTH(TRIM(title)) > 0)
);

-- 5. RELEASE GENRE TABLE (ManyToMany)
CREATE TABLE music_release_genre (
    id BIGSERIAL PRIMARY KEY,
    release_id BIGINT NOT NULL,
    genre_id BIGINT NOT NULL,

    -- Constraints
    FOREIGN KEY (release_id)
        REFERENCES music_release(id)
        ON DELETE CASCADE,
    FOREIGN KEY (genre_id)
        REFERENCES music_genre(id)
        ON DELETE CASCADE,
    CONSTRAINT unique_release_genre UNIQUE (release_id, genre_id)
);

-- 6. TRACK TABLE
CREATE TABLE music_track (
    id BIGSERIAL PRIMARY KEY,
    release_id BIGINT NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    duration DECIMAL(10, 2),
    track_number INTEGER,
    original_file VARCHAR(255),
    file_size BIGINT,
    transcoding_status VARCHAR(20) NOT NULL DEFAULT 'pending',
    visibility VARCHAR(10) NOT NULL DEFAULT 'private',
    upload_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Constraints
    FOREIGN KEY (release_id)
        REFERENCES music_release(id)
        ON DELETE CASCADE,
    CONSTRAINT transcoding_status_choices CHECK (
        transcoding_status IN ('pending', 'processing', 'completed', 'failed')
    ),
    CONSTRAINT visibility_choices CHECK (
        visibility IN ('public', 'private')
    ),
    CONSTRAINT track_number_positive CHECK (track_number > 0),
    CONSTRAINT duration_positive CHECK (duration > 0),
    CONSTRAINT file_size_limit CHECK (
        file_size <= 524288000
    ),
    CONSTRAINT title_not_empty CHECK (LENGTH(TRIM(title)) > 0)
);

-- 7. TRACK FILE TABLE
CREATE TABLE music_trackfile (
    id BIGSERIAL PRIMARY KEY,
    track_id BIGINT NOT NULL,
    file VARCHAR(255) NOT NULL,
    format VARCHAR(10) NOT NULL,
    bitrate INTEGER,
    file_size BIGINT,
    sample_rate INTEGER,
    codec VARCHAR(50),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Constraints
    FOREIGN KEY (track_id)
        REFERENCES music_track(id)
        ON DELETE CASCADE,
    CONSTRAINT format_choices CHECK (
        format IN ('mp3', 'aac', 'ogg')
    ),
    CONSTRAINT bitrate_positive CHECK (bitrate > 0),
    CONSTRAINT file_size_positive CHECK (file_size > 0),
    CONSTRAINT sample_rate_positive CHECK (sample_rate > 0)
);

-- 8. PROCESSING JOB TABLE
CREATE TABLE music_processingjob (
    id BIGSERIAL PRIMARY KEY,
    track_id BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    format VARCHAR(10) NOT NULL,
    error_log TEXT,
    retries INTEGER NOT NULL DEFAULT 0,
    max_retries INTEGER NOT NULL DEFAULT 3,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    -- Constraints
    FOREIGN KEY (track_id)
        REFERENCES music_track(id)
        ON DELETE CASCADE,
    CONSTRAINT status_choices CHECK (
        status IN ('pending', 'processing', 'completed', 'failed')
    ),
    CONSTRAINT format_choices CHECK (
        format IN ('mp3', 'aac', 'ogg')
    ),
    CONSTRAINT retries_non_negative CHECK (retries >= 0),
    CONSTRAINT max_retries_limit CHECK (max_retries <= 5),
    CONSTRAINT retries_within_limit CHECK (retries <= max_retries)
);
