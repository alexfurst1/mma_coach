-- schema.sql
-- purely to showcase database structure. this was ran on supabase. not meant to be ran by users/testers.

CREATE TABLE video_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cloudflare_key TEXT NOT NULL,
  duration FLOAT,
  video_type TEXT,
  status TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE summaries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id UUID REFERENCES video_data(id),
  feedback TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE timestamps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  video_id UUID REFERENCES video_data(id),
  t_start_seconds NUMERIC,
  t_end_seconds NUMERIC,
  feedback TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);