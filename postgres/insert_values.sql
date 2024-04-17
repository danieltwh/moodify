-- Insert values into users
INSERT INTO videos
	(video_id, video_name, video_status, date_created, predictions)
	VALUES
    ('test', 'video.mp4', 'completed','2023-03-13 20:46:43.90241', '
    {"aggregates": {
    "speech_data": {
      "preds_str": ["positive"],
      "interps": [
        {
          "positive": 0.0076,
          "neutral": -0.0306,
          "negative": -0.0481
        }
      ]
    },
    "face_emotion": {
      "preds_str": ["neutral"],
      "interps": [
        {
          "positive": -0.0306,
          "neutral": 0.0379,
          "negative": -0.0496
        }
      ]
    }
  },
  "speech_data": {
    "preds_str": [
      "positive",
      "positive",
      "neutral",
      "neutral",
      "positive",
      "positive",
      "neutral",
      "neutral",
      "positive",
      "positive",
      "neutral"
    ],
    "interps": [
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      }
    ]
  },
  "text": " So its two weeks from prom and you dont have a date. What are you going to do? Or maybe you have a job interview for that dream job and you really want to win the employer over.",
  "face_emotion": {
    "preds_str": [
      "positive",
      "positive",
      "neutral",
      "neutral",
      "positive",
      "positive",
      "neutral",
      "neutral",
      "positive",
      "positive",
      "neutral"
    ],
    "interps": [
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": 0.0076,
        "neutral": -0.0306,
        "negative": -0.0481
      },
      {
        "positive": -0.0306,
        "neutral": 0.0379,
        "negative": -0.0496
      }
    ]
  }
}'),
     ('c8dd5351-0653-4929-a177-f8a23892d88d', 'video.mp4', 'processing','2023-03-13 20:46:43.90241', '')
		
	ON CONFLICT (video_id) DO UPDATE
	SET
		video_name = excluded.video_name,
		video_status = excluded.video_status,
		date_created = excluded.date_created,
		predictions = excluded.predictions
;
