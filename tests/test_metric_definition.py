from grafgate import GrafGate
import pytest

app = GrafGate()


@app.metric
async def metric_without_custom_name():
    return [(100, 1667293172)]


@app.metric(name="My another custom metric")
async def metric_with_custom_name():
    return [(101, 1667293172)]


@app.metric
def synchronous_metric():
    return [(102, 1667293172)]


@pytest.fixture()
def client(event_loop, aiohttp_client):
    return event_loop.run_until_complete(aiohttp_client(app.app))


@pytest.mark.asyncio
async def test_metric_without_custom_name(client, payload):
    payload["targets"][0]["target"] = "metric_without_custom_name"
    r = await client.post("/query", json=payload)
    assert r.status == 200

    data = await r.json()
    assert len(data) == 1
    assert data[0]["target"] == "metric_without_custom_name"
    assert data[0]["datapoints"] == [[100, 1667293172]]


@pytest.mark.asyncio
async def test_metric_with_custom_name(client, payload):
    payload["targets"][0]["target"] = "My another custom metric"
    r = await client.post("/query", json=payload)
    assert r.status == 200

    data = await r.json()
    assert len(data) == 1
    assert data[0]["target"] == "My another custom metric"
    assert data[0]["datapoints"] == [[101, 1667293172]]


@pytest.mark.asyncio
async def test_synchronous_metric(client, payload):
    payload["targets"][0]["target"] = "synchronous_metric"
    r = await client.post("/query", json=payload)
    assert r.status == 200

    data = await r.json()
    assert len(data) == 1
    assert data[0]["target"] == "synchronous_metric"
    assert data[0]["datapoints"] == [[102, 1667293172]]
