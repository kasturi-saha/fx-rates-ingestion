WITH deduped AS (
  {{ dbt_utils.deduplicate(
      relation=source('raw_fx_rates_usd_base', 'raw_fx_rates_usd_base'),
      partition_by='currency',
      order_by='timestamp desc'
  ) }}
)

SELECT
  CAST(TO_TIMESTAMP(timestamp) AS DATE) AS fx_date,
  currency,
  rate,
  TO_TIMESTAMP(timestamp) AS ts
FROM deduped
