import base64
import pytest
import pytest_html
from pytest_html import extras
from playwright.sync_api import Playwright

from wizz_main.functions.common.common import Common
from wizz_main.constants.config import BASE_URL
from utilities.excel_reader import read_excel_row

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        extra = getattr(rep, "extra", [])
        if hasattr(item, "screenshot_path"):
            # Read the image and convert to base64
            with open(item.screenshot_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            extra.append(pytest_html.extras.image(encoded, mime_type="image/png"))
        rep.extra = extra

@pytest.fixture
def loadData(request):
    file_name, sheet_name, row_index = request.param
    return read_excel_row(file_name, sheet_name, row_index)


@pytest.fixture(scope="function")
def set_up(playwright: Playwright, request):

    browser = playwright.chromium.launch(slow_mo=1000, headless=False, args=['--start-maximized'])
    context = browser.new_context(
        permissions=["geolocation"],
        geolocation={"latitude": 0, "longitude": 0},
        no_viewport=True
    )
    page = context.new_page()
    page.goto(BASE_URL)
    page.set_default_timeout(150000)

    yield page

    page.close()
    context.close()
    browser.close()


@pytest.fixture(scope="function")
def common(set_up, request):
    return Common(page=set_up)