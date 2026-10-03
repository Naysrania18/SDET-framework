import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_valid_login_shows_inventory(page):
    LoginPage(page).open().login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    assert inv.title.inner_text() == "Products"
    assert inv.items.count() == 6


@pytest.mark.parametrize("user,pwd,message", [
    ("locked_out_user", "secret_sauce", "locked out"),
    ("standard_user", "wrong", "do not match"),
    ("", "secret_sauce", "Username is required"),
])
def test_invalid_login_shows_error(page, user, pwd, message):
    LoginPage(page).open().login(user, pwd)
    assert message in LoginPage(page).error.inner_text()


def test_add_to_cart_updates_badge(page):
    LoginPage(page).open().login("standard_user", "secret_sauce")
    inv = InventoryPage(page)
    inv.add_first_item_to_cart()
    assert inv.cart_badge.inner_text() == "1"
