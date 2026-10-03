import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

scenarios("../../features")


@given("I am on the login page")
def open_login(page):
    LoginPage(page).open()


@when(parsers.parse('I log in as "{user}" with password "{pwd}"'))
def do_login(page, user, pwd):
    LoginPage(page).login(user, pwd)


@then(parsers.parse('I should see the "{title}" page'))
def see_page(page, title):
    assert InventoryPage(page).title.inner_text() == title


@then(parsers.parse('I should see the error "{text}"'))
def see_error(page, text):
    assert text in LoginPage(page).error.inner_text()


@pytest.fixture
def ctx():
    return {}


@when(parsers.parse("I request user {uid:d}"))
def request_user(api, ctx, uid):
    ctx["resp"] = api.get(f"/users/{uid}")


@then(parsers.parse("the response status is {code:d}"))
def status_is(ctx, code):
    assert ctx["resp"].status_code == code


@then(parsers.parse("the user id is {uid:d}"))
def user_id_is(ctx, uid):
    assert ctx["resp"].json()["id"] == uid
