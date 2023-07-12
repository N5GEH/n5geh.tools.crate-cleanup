# CrateCleaner

CrateCleaner is a lightweight, containerized Python tool designed to regularly clean up CrateDB tables based on configured intervals. This is particularly useful for managing databases that collect time-series data, where older data may need to be purged regularly to optimize storage and performance.

## Features

- Easy configuration through a JSON file.
- Secure connection to CrateDB using user credentials.
- Adjustable data retention periods for each table.
- Dockerized for easy deployment and scaling.
- Comprehensive logging for tracking cleanup operations.

## Prerequisites

- Docker
- Docker Compose
- Python 3.6 or later
- CrateDB instance accessible to the tool

## Quickstart

1. Clone the repository:

    ```bash
    git clone https://github.com/username/CrateCleaner.git
    ```

2. Navigate to the cloned directory:

    ```bash
    cd CrateCleaner
    ```

3. Modify the `config.json` file to include your tables, their corresponding time indices, and the desired data retention periods. For example:

    ```json
    {
      "mtheat.etpump": {
        "retention": "14d",
        "time-index": "time_index"
      },
      "another_table": {
        "retention": "60m",
        "time-index": "timestamp"
      }
    }
    ```

4. Build the Docker image:

    ```bash
    docker build -t cratedb-cleanup:0.1 .
    ```

5. Create a `docker-compose.yml` file with the necessary environment variables for your CrateDB instance and a volume to mount the `config.json` file. Here's an example:

    ```yaml
    version: '3'
    services:
      cratedb-cleanup:
        image: cratedb-cleanup:0.1
        environment:
          - CRATE_HOST=your_crate_host
          - CRATE_USER=your_crate_user
          - CRATE_PASSWORD=your_crate_password
        volumes:
          - ./config.json:/app/config.json
    ```

6. Start the Docker container using Docker Compose:

    ```bash
    docker-compose up -d
    ```

You can check the logs of the cleanup process by running `docker-compose logs -f`.

## Configuration

The `config.json` file is used to set the table names, time indices, and data retention periods. The format is as follows:

```json
{
  "<table_name>": {
    "retention": "<data_retention_period>",
    "time-index": "<time_index>"
  },
  ...
}
```

- `<table_name>`: The full name of the table in CrateDB (including the schema if applicable).
- `<data_retention_period>`: The maximum age of the data to keep in the table. Older data will be deleted. Format: `"<number><unit>"`, where `<number>` is a positive integer and `<unit>` is either "d" (days), "h" (hours), or "m" (minutes). For example, "14d" means 14 days.
- `<time_index>`: The name of the timestamp column in the table.

Please note that the intervals are based on the `CURRENT_TIMESTAMP` of the CrateDB server.
