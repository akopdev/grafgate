import pytest


@pytest.mark.asyncio
async def test_health(client):
    r = await client.get("/")
    assert r.status == 200


@pytest.mark.asyncio
async def test_single_metric_query(client):
    payload = {
        "targets": [
            {
                "target": "ts_metric_1",
                "payload": {}
            }
        ],
        "range": {
            "from": "2022-10-01T10:10:41.040939",
            "to": "2022-11-01T10:10:41.040939"
        }

    }
    r = await client.post("/query", json=payload)
    assert r.status == 200

    data = await r.json()
    assert len(data) == 1
    assert data[0]["target"] == "ts_metric_1"
    assert data[0]["datapoints"] == [[100, 1667293172], [101.5, 1667293173]]


@pytest.mark.asyncio
async def test_multi_metric_query(client):
    payload = {
        "targets": [
            {
                "target": "ts_metric_1",
                "payload": {}
            },
            {
                "target": "ts_metric_2",
                "payload": {}
            }

        ],
        "range": {
            "from": "2022-10-01T10:10:41.040939",
            "to": "2022-11-01T10:10:41.040939"
        }

    }
    r = await client.post("/query", json=payload)
    assert r.status == 200

    data = await r.json()
    assert len(data) == 2
    assert data[0]["target"] == "ts_metric_1"
    assert data[1]["target"] == "ts_metric_2"


@pytest.mark.asyncio
async def test_metric_with_payload(client):
    payload = {
        "targets": [
            {
                "target": "ts_metric_3",
                "payload": {
                    "param1": 300
                }
            },
        ],
        "range": {
            "from": "2022-10-01T10:10:41.040939",
            "to": "2022-11-01T10:10:41.040939"
        }

    }
    r = await client.post("/query", json=payload)
    # assert r.status == 200

    data = await r.json()
    assert len(data) == 1
    assert data[0]["target"] == "ts_metric_3"
    assert data[0]["datapoints"] == [[300, 1667293172]]


@pytest.mark.asyncio
async def test_server_and_payload_params(client):
    payload = {
        "targets": [
            {
                "target": "ts_metric_4",
                "payload": {
                    "param1": 500
                }
            }
        ],
        "range": {
            "from": "2022-10-01T10:10:41.040939",
            "to": "2022-11-01T10:10:41.040939"
        }

    }
    r = await client.post("/query", json=payload)
    assert r.status == 200

    data = await r.json()
    assert len(data) == 1
    assert data[0]["target"] == "ts_metric_4"
    assert data[0]["datapoints"] == [[400, 1667293172], [500, 1667293173]]


@pytest.mark.asyncio
async def test_table_metric(client):
    payload = {
        "targets": [
            {
                "target": "t_metric_1",
                "payload": {
                    "column_name": "Some column name"
                }
            }
        ],
        "range": {
            "from": "2022-10-01T10:10:41.040939",
            "to": "2022-11-01T10:10:41.040939"
        }

    }
    r = await client.post("/query", json=payload)
    assert r.status == 200

    data = await r.json()
    assert len(data) == 1
    assert data[0]["type"] == "table"
    assert data[0]["columns"] == [{"text": "Some column name", "type": "string"}]
    assert data[0]["rows"] == [["row 1"], ["row 2"]]
