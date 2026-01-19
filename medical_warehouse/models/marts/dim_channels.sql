with c as (
    select distinct channel_name
    from {{ ref('stg_telegram_messages') }}
)

select
    row_number() over() as channel_key,
    channel_name,
    'Medical' as channel_type, -- or map dynamically if needed
    min(message_date) as first_post_date,
    max(message_date) as last_post_date,
    count(*) as total_posts,
    avg(views) as avg_views
from c
left join {{ ref('stg_telegram_messages') }} m using(channel_name)
group by channel_name
