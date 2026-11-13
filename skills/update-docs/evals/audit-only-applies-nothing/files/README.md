# lakefront-api

Serves Lake Erie tide readings as JSON.

## Run it

```bash
npm install
npm run start:dev
```

The server listens on `PORT` (default 3000).

## Endpoints

- `GET /tides`: today's tide table.

## Configuration

- `LAKE_API_KEY`: key for the NOAA buoy feed.
