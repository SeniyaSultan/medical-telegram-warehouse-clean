-- tests/assert_no_future_messages.sql
select *
from {{ ref('fct_messages') }}
where message_date > current_date
