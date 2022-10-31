import asyncio
from typing import Any, Callable, Dict, List,  Tuple

from aiohttp import web

from .schemas import Column, Payload, Table, Timeseries


class GrafGate:
    def __init__(self, **kwargs) -> None:
        self.tasks: List[Tuple[str, Callable]] = []
        self.metrics: Dict[str, Callable] = {}

        self.app = web.Application(middlewares=[self._add_middleware()])
        self.app.add_routes([
            self._heath(),
            self._search(),
            self._query(),
            self._tag_keys(),
            self._tag_values(),
        ])
        if kwargs:
            for name, val in kwargs.items():
                self.app[name] = val

    def metric(self, func: Callable = None) -> Callable:
        def decorator(func) -> None:
            self.metrics[func.__name__] = func
        return decorator

    def task(self, func: Callable) -> None:
        async def custom_func(*args, **kwargs) -> Any:
            if func.__code__.co_argcount:
                data = await func(*args, **kwargs)
            else:
                data = await func()
            return data
        self.tasks.append((func.__name__, custom_func,))

    def _heath(self):
        """Check for connection on the datasource config page."""
        async def endpoint(req):
            return web.json_response("OK")
        return web.get("/", endpoint)

    def _search(self):
        """
        List available metrics.

        Used by the find metric options on the query tab in panels.
        """
        async def endpoint(req):
            return web.json_response(list(self.metrics.keys()))
        return web.post("/search", endpoint)

    def _query(self):
        """Return metrics data."""
        async def endpoint(req):
            body = await req.json()
            payload = Payload(**body)
            response = []
            for target in payload.targets:
                if target.target in self.metrics:
                    func = self.metrics[target.target]
                    if func.__code__.co_argcount:
                        # Prepare inputs for the method
                        available_inputs = {**req.app, **target.payload, **payload.range.dict()}
                        varnames = {}
                        for varname in func.__code__.co_varnames:
                            if varname in available_inputs:
                                varnames.setdefault(
                                    varname,
                                    available_inputs.get(varname)
                                )
                        data = await func(**varnames)
                    else:
                        data = await func()
                    if data:
                        if not isinstance(data[0], (list, tuple, dict,)):
                            raise ValueError("Not supported type of data")
                        if isinstance(data[0], dict):
                            response.append(
                                Table(
                                    columns=[Column(text=key) for key in data[0].keys()],
                                    rows=[list(row.values()) for row in data]
                                ).dict()
                            )
                        else:
                            response.append(
                                Timeseries(target=target.target, datapoints=data).dict()
                            )
            return web.json_response(response)
        return web.post("/query", endpoint)

    def _tag_keys(self):
        """Keys for ad hoc filters."""
        async def endpoint(req):
            raise Exception("Not implemented")
        return web.post("/tag-keys", endpoint)

    def _tag_values(self):
        """Values for ad hoc filters."""
        async def endpoint(req):
            raise Exception("Not implemented")
        return web.post("/tag-values", endpoint)

    def _add_middleware(self):
        @web.middleware
        async def error_middleware(request, handler):
            try:
                response = await handler(request)
                if response.status != 404:
                    return response
                message = response.message
            except web.HTTPException as ex:
                if ex.status != 404:
                    raise
                message = ex.reason
            except Exception as e:
                message = str(e)
            return web.json_response({'error': message})
        return error_middleware

    async def _tasks(self, app):
        for task in self.tasks:
            app[task[0]] = asyncio.create_task(task[1](app))

    def run(self):
        self.app.on_startup.append(self._tasks)
        web.run_app(self.app)
