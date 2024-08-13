WITH user_data AS (
 SELECT
   user_id,
   COUNT(IF(type = 'TV', object_id, NULL)) AS tv_watch,
   COUNT(IF(type != 'TV', object_id, NULL)) AS other_watch,
   SUM(w_duration) / 60 / 60 AS w_duration_h,
   COUNT(DISTINCT DATE(event_date)) AS days_used
 FROM da-dataset-426715.junior_data_set.watching_data
 WHERE w_duration > 30
 GROUP BY user_id
)
SELECT
 user_id,
 CASE
   WHEN tv_watch > 0 AND other_watch = 0 THEN 'TV'
   WHEN tv_watch = 0 AND other_watch > 0 THEN 'VIDEO'
   ELSE 'TV+VIDEO'
 END AS content_type_group,
 CASE
   WHEN w_duration_h <= 1 THEN '0-1 hours'
   WHEN w_duration_h > 1 AND w_duration_h <= 10 THEN '1-10 hours'
   WHEN w_duration_h > 10 AND w_duration_h <= 50 THEN '10-50 hours'
   WHEN w_duration_h > 50 AND w_duration_h <= 100 THEN '50-100 hours'
   WHEN w_duration_h > 100 AND w_duration_h <= 500 THEN '100-500 hours'
   ELSE '500+ hours'
 END AS w_hours_group,
 CASE
   WHEN days_used = 1 THEN '1 day'
   WHEN days_used > 1 AND days_used <= 7 THEN '1-7 days'
   WHEN days_used > 7 AND days_used <= 14 THEN '7-14 days'
   WHEN days_used > 14 AND days_used <= 30 THEN '14-30 days'
   WHEN days_used > 30 AND days_used <= 60 THEN '30-60 days'
   ELSE '60+ days'
 END AS days_group
FROM user_data
ORDER BY user_id;


