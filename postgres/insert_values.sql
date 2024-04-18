-- Insert values into users
INSERT INTO videos
	(video_id, video_name, video_status, date_created, predictions)
	VALUES
    ('test', 'video.mp4', 'completed','2023-03-13 20:46:43.90241', '
    {"aggregates": {"speech_data": {"preds_str": ["neutral"], "interps": [{"negative": 0.0, "neutral": 1.0, "positive": 0.6977787143843402}]}, "face_emotion": {"preds_str": ["neutral"], "interps": [{"negative": 0.06245409033726901, "neutral": 0.6418068896979093, "positive": 0.29573904583230615}]}}, "speech_data": {"preds_str": ["neutral", "neutral", "neutral", "neutral", "neutral", "positive", "neutral", "neutral", "neutral", "neutral"], "interps": [{"negative": 0.0, "neutral": 1.0, "positive": 0.6596407539714637}, {"negative": 0.0, "neutral": 1.0, "positive": 0.6357616739438667}, {"negative": 0.0, "neutral": 1.0, "positive": 0.628641874798095}, {"negative": 0.0, "neutral": 1.0, "positive": 0.6414428223486458}, {"negative": 0.13784637261460234, "neutral": 1.0, "positive": 0.0}, {"negative": 0.0, "neutral": 0.45749575842854895, "positive": 1.0}, {"negative": 0.0, "neutral": 1.0, "positive": 0.6321887212972885}, {"negative": 0.0, "neutral": 1.0, "positive": 0.8335152788975972}, {"negative": 0.0, "neutral": 1.0, "positive": 0.8032968904694467}, {"negative": 0.0, "neutral": 1.0, "positive": 0.8558936497399517}]}, "text": " So its two weeks from prom and you dont have a date. What are you going to do? Or maybe you have a job interview for that dream job and you really want to win the employer over.", "face_emotion": {"preds_str": ["positive", "neutral", "neutral", "neutral", "neutral", "neutral", "positive", "neutral", "neutral", "neutral"], "interps": [{"negative": 0.04577834904193878, "neutral": 0.35891926288604736, "positive": 0.5953024625778198}, {"negative": 0.05461568385362625, "neutral": 0.7158809304237366, "positive": 0.22950342297554016}, {"negative": 0.0181313194334507, "neutral": 0.7696577906608582, "positive": 0.21221093833446503}, {"negative": 0.02674958109855652, "neutral": 0.8359024524688721, "positive": 0.1373479813337326}, {"negative": 0.22277861833572388, "neutral": 0.3959798514842987, "positive": 0.3812415897846222}, {"negative": 0.00030910084024071693, "neutral": 0.9876264929771423, "positive": 0.01206445787101984}, {"negative": 0.2399393767118454, "neutral": 0.05213240906596184, "positive": 0.7079281806945801}, {"negative": 0.0034146204125136137, "neutral": 0.7175450325012207, "positive": 0.2790403962135315}, {"negative": 0.00245971092954278, "neutral": 0.7777352929115295, "positive": 0.21980495750904083}, {"negative": 0.010364542715251446, "neutral": 0.8066893815994263, "positive": 0.1829460710287094}]}}'),
     ('c8dd5351-0653-4929-a177-f8a23892d88d', 'video.mp4', 'processing','2023-03-13 20:46:43.90241', '')
		
	ON CONFLICT (video_id) DO UPDATE
	SET
		video_name = excluded.video_name,
		video_status = excluded.video_status,
		date_created = excluded.date_created,
		predictions = excluded.predictions
;
