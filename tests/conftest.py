import asyncio
from grafgate import GrafGate
import pytest


@pytest.fixture(scope="session")
def app():
    gg = GrafGate(app_param=400)

    @gg.metric
    async def ts_metric_1():
        return [(100, 1667293172), (101.50, 1667293173)]

    @gg.metric
    async def ts_metric_2():
        return [(200, 1667293172), (201, 1667293173), (203, 1667293174)]

    @gg.metric
    async def ts_metric_3(param1: int):
        return [(param1, 1667293172)]

    @gg.metric
    async def ts_metric_4(app_param: int, param1: int):
        return [(app_param, 1667293172), (param1, 1667293173)]

    @gg.metric
    def ts_metric_5(param1: int, param2):
        return [(param1, 1667293172), (param2, 1667293173)]

    @gg.metric
    async def t_metric_1(column_name: str):
        return [{f"{column_name}": "row 1"}, {f"{column_name}": "row 2"}]

    return gg


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def payload():
    return {
        "targets": [
            {
                "target": "",
                "payload": {}
            }
        ],
        "range": {
            "from": "2022-10-01T10:10:41.040939",
            "to": "2022-11-01T10:10:41.040939"
        }
    }


@pytest.fixture()
def client(event_loop, aiohttp_client, app):
    return event_loop.run_until_complete(aiohttp_client(app.app))
