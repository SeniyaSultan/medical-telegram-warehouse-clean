WITH detections AS (
    SELECT
        message_id,
        channel_name,
        detected_object,
        confidence,
        image_category
    FROM raw.image_detections
),

messages AS (
    SELECT
        message_id,
        channel_key,
        date_key
    FROM {{ ref('fct_messages') }}
)

SELECT
    d.message_id,
    m.channel_key,
    m.date_key,
    d.detected_object,
    d.confidence,
    d.image_category
FROM detections d
JOIN messages m
ON d.message_id = m.message_id
