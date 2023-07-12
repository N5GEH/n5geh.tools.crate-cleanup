# n5geh.tools.crate-cleanup
This is a Script, which deletes specified data automatically from a table after a specific amount of time.

## Usage
Configure the config.json to specify which data should be regularly deleted. 

Mount it to `/app/config.json`

The config.json expects the tables in JSON-Format.

`"retention"` specifies the amount of time the data is retained. It accepts values for days, hours, minutes and seconds (e.g. `1d`, `24h`, `60m` or `3600s` but no combinations).

`time-index` specifies the name of the column holding the time-stamp (e.g. `time`).

The Script executes every 5 minutes (specified in the crontab-file). 