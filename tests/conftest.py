"""Conftest file for pytest."""
from _pytest.fixtures import FixtureRequest
import pytest
from selenium import webdriver


def pytest_addoption(parser):
    """Pytest function that would addoption."""
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--head", action="store", default="1")
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture(scope="class")
def browser_driver(request: FixtureRequest):
    """Create the browser driver with the right request.
    Creates the browser driver for uses in diffrent test.
    Args:
        request (FixtureRequest): For the config given by
        the users.
    """
    driver: webdriver
    match request.config.option.browser:
        case "chrome":
            options = webdriver.ChromeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
        case "edge":
            options = webdriver.EdgeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
        case "chromium":
            options = webdriver.ChromeOptions()
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.ChromiumEdge(options=options)
        case _:
            options = webdriver.FirefoxOptions()
            print(request.config.option.headless)
            if request.config.option.head == "1":
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
    yield driver
    driver.close()
