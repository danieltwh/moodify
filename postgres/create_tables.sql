
-- Create videos table
DROP TABLE IF EXISTS videos CASCADE;

CREATE TABLE videos (
	video_id VARCHAR PRIMARY KEY,
    video_name VARCHAR NOT NULL,
    video_status VARCHAR NOT NULL,
    date_created timestamp without time zone DEFAULT (now() at time zone 'utc'),
    predictions VARCHAR  NOT NULL
);

