class MockPageLoader:
    def __init__(self, html: str = "<html></html>"):
        self.html = html
        self.started = False
        self.closed = False
        self.loaded_urls = []

    async def start(self):
        self.started = True

    async def load_dom(self, url: str, timeout: int = 90000):
        self.loaded_urls.append(url)
        return self.html

    async def close(self):
        self.closed = True
