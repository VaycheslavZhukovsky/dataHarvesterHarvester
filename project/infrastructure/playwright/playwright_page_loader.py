from playwright.async_api import async_playwright, Playwright, BrowserContext
from typing import Optional

from project.domain.interfaces.page_loader import IPageLoader


class PlaywrightPageLoader(IPageLoader):
    def __init__(self, proxy: dict | None = None, cookies: list | None = None):
        self.proxy = proxy
        self.cookies = cookies or []

        self._pw: Optional[Playwright] = None
        self._context: Optional[BrowserContext] = None

    async def start(self) -> None:
        self._pw = await async_playwright().start()

        self._context = await self._pw.chromium.launch_persistent_context(
            headless=True,
            user_data_dir="profile",
            proxy=self.proxy,
        )

        if self.cookies:
            await self._context.add_cookies(self.cookies)

    async def load_dom(self, url: str, timeout: int = 90000) -> str:
        if not self._context:
            raise RuntimeError("PlaywrightPageLoader not started")

        page = await self._context.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        html = await page.content()
        await page.close()
        return html

    async def close(self) -> None:
        if self._context:
            await self._context.close()
            self._context = None

        if self._pw:
            await self._pw.stop()
            self._pw = None


async def main():
    url = "https://lemanapro.ru/catalogue/oboi-pod-pokrasku/"

    root = Path(__file__).resolve().parent.parent
    path_to_the_cache = root / "cookies.txt"

    cookies_obj = CookiesManager().build(path_to_the_cache)

    loader = PlaywrightPageLoader(cookies=cookies_obj.cookies)

    await loader.start()
    html = await loader.load_dom(url)
    await loader.close()

    print(html)


if __name__ == "__main__":

    import asyncio
    from pathlib import Path

    from project.infrastructure.playwright.cookies_manager import CookiesManager

    asyncio.run(main())
