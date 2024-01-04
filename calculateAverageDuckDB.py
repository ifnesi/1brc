import duckdb


with duckdb.connect() as conn:
    # Import CSV in memory using DuckDB
    data = conn.sql(
        """
        SELECT
            station_name,
            MIN(measurement) AS min_measurement,
            CAST(AVG(measurement) AS DECIMAL(8,1)) AS mean_measurement,
            MAX(measurement) AS max_measurement
        FROM READ_CSV(
            'measurements.txt',
            header=false,
            columns={'station_name':'VARCHAR','measurement':'DECIMAL(8,1)'},
            delim=';',
            parallel=true
        )
        GROUP BY
            station_name
        """
    )

    # Export to dict (it could be done via data.to_df().to_json(orient='records') too)
    results = dict()
    for row in sorted(data.fetchall()):
        results[row[0]] = f"{row[1]}/{row[2]}/{row[3]}"
    print(results)
