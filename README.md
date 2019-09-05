


POST - store event

curl http://localhost:5000/api/event -XPOST -d '{"timestamp":1567690200, "name":"some_event", "source_ip":"0.0.0.0", "extra_data":{"foo": "bar"}}' -H "Content-Type: application/json"


GET - retrieve events

curl "http://localhost:5000/api/event?from=1567690200&to=1567690200&location=London"
curl "http://localhost:5000/api/event?from=1567690200&to=1567690200&location=London"
curl "http://localhost:5000/api/event?from=1567690200&to=1567690200"
curl "http://localhost:5000/api/event?to=1567690200&location=London"
curl "http://localhost:5000/api/event?location=London"
curl "http://localhost:5000/api/event?from=1567690200"
curl "http://localhost:5000/api/event?to=1567690200"
