# 💱 FX Rate Ingestion Data Pipeline

This project ingests foreign exchange (FX) rate data using a **Python** script and transforms it using **dbt (Data Build Tool)**. It ensures clean, deduplicated FX rates with automated data quality checks. The data is stored locally in **DuckDB**.

---

## 🔁 Workflow

1. **Ingestion (Python):**
   - `ingest.py` fetches FX rate data from [Open Exchange Rates](https://openexchangerates.org/) using their free API.
   - The API returns rates with **USD as the base currency**.
   - The data is normalized into rows and inserted into the `raw_fx_rates_usd_base` table in DuckDB.

2. **Deduplication (dbt):**
   - dbt processes the raw data in the `stg_fx_rates_usd_base` model.
   - If the script runs multiple times a day, only the **latest record per currency** is retained.

3. **Transformation (dbt):**
   - The client requires FX rates with **CAD as the base currency**.
   - The transformation is handled in the `fx_rates_cad_base` model.
   - This is an **incremental model**, where:
     - New dates are inserted.
     - If the same date-currency pair already exists but with a **new rate**, the row is **updated**.
   - `fx_date` and `currency` are used as **unique keys**.

4. **Testing (dbt):**
   - Data quality tests are added to:
     - Ensure `currency` codes are 3 characters.
     - Validate `rate` is not null and positive.
     - Ensure uniqueness of `(fx_date, currency)` in the final model.

---

## 🚀 How to Run

1. **Set API Key:**
   - Sign up at [openexchangerates.org](https://openexchangerates.org/) and generate a free API key.
   - Set it as an environment variable:
   ```bash
   export API_KEY="your_api_key"
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Python Ingestion Script**:

    ```bash
    python ingest.py
    ```

4. **Run dbt Models and Tests**:

    ```bash
    cd dbt
    dbt deps
    dbt run
    dbt test
    ```

5. **View Final Table**:

    The cleaned and transformed FX rates will be available in the fx_rates_cad_base table in local fx_data.duckdb database.
