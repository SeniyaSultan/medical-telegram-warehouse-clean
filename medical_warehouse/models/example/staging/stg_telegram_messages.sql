-- models/staging/stg_telegram_messages.sql
with raw as (

    select *
    from raw.telegram_messages

)

select
    message_id,
    channel_name,
    message_date::timestamp as message_date,
    message_text,
    coalesce(has_media, false) as has_media,
    image_path,
    coalesce(views, 0)::int as views,
    coalesce(forwards, 0)::int as forwards,
    length(message_text) as message_length
from raw
where message_text is not null
