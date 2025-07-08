from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import re

app = FastAPI()

async def search_google_shopping(query: str, country: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(locale=country.lower())
        page = await context.new_page()

        search_url = f"https://www.google.com/search?tbm=shop&q={query.replace(' ', '+')}"
        await page.goto(search_url)

        await page.wait_for_selector('div.sh-dgr__grid-result', timeout=10000)
        items = await page.query_selector_all('div.sh-dgr__grid-result')

        results = []
        for item in items[:10]:
            title_el = await item.query_selector('h4 > span')
            price_el = await item.query_selector('span.a8Pemb')
            link_el = await item.query_selector('a')

            title = await title_el.inner_text() if title_el else None
            price_raw = await price_el.inner_text() if price_el else None
            price = float(re.sub(r"[^0-9.]", "", price_raw)) if price_raw else None
            link = await link_el.get_attribute('href') if link_el else None

            if title and price and link:
                results.append({
                    "productName": title,
                    "price": price,
                    "currency": "USD",
                    "link": f"https://www.google.com{link}",
                    "source": "Google Shopping"
                })

        await browser.close()
        return results

@app.post("/search")
async def search_products(req: Request):
    payload = await req.json()
    country = payload.get("country", "US")
    query = payload.get("query")

    if not query:
        return JSONResponse(status_code=400, content={"error": "Missing query"})

    results = await search_google_shopping(query, country)
    sorted_results = sorted(results, key=lambda x: x["price"])
    return sorted_results
