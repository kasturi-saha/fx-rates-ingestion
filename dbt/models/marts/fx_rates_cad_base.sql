{{ config(
    materialized='incremental',
    unique_key=['fx_date', 'currency']
) }}

WITH raw AS (
    SELECT * FROM {{ ref('stg_raw_fx_rates_usd_base') }}
),

cad AS (
    SELECT fx_date, rate AS usd_to_cad_rate FROM raw WHERE currency = 'CAD'
),

fx_normalized AS (
    SELECT
        r.fx_date,
        r.currency,
        ROUND(r.rate / c.usd_to_cad_rate, 6) AS cad_rate
    FROM raw r
    INNER JOIN cad c ON r.fx_date = c.fx_date
    WHERE r.currency != 'CAD'
)

SELECT * FROM fx_normalized

{% if is_incremental() %}
WHERE fx_normalized.fx_date > (SELECT MAX(fx_date) FROM {{ this }})
{% endif %}
