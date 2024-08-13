SELECT
  *
FROM (
  SELECT
      geo.country AS country,
      device.mobile_model_name AS mobile_model,
      COUNT(*) AS usage_count
  FROM
      `globelink-395309.analytics_355183230.events_20240811`
  WHERE
      geo.country IS NOT NULL
      AND device.mobile_model_name IS NOT NULL
  GROUP BY
      country,
      mobile_model
)
PIVOT (
  COUNT(usage_count) AS cnt,
  SUM(usage_count) AS total
  FOR mobile_model IN ('iPhone' AS iPhone, 'Samsung' AS Samsung, 'Xiaomi' AS Xiaomi, 'Huawei' AS Huawei, 'OnePlus' AS OnePlus)
)
ORDER BY
  country;
