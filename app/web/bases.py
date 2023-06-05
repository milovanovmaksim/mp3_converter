from aiohttp.web import View as AiohttpView
from aiohttp_cors import CorsViewMixin


class View(CorsViewMixin, AiohttpView):
    @property
    def data(self) -> dict:
        return self.request.get("data", {})

    @property
    def query(self) -> dict:
        return self.request.get("querystring", {})
