import pytest
import allure

from page_objects.owner_list_page import OwnerListPage


@pytest.mark.smoke
class TestFindOwner:
    """ """

    @pytest.mark.test
    @pytest.mark.nondestructive
    @allure.title("Поиск владельца питомца в таблице")
    def test_search_pets_owner_in_table(self, driver, base_url, create_owner, cleanup_owner):
        owner_id, owner_data = create_owner
        owner_name = owner_data.get('firstName') + ' ' + owner_data.get('lastName')
        owner_list_page = OwnerListPage(driver)
        owner_list_page.open(base_url)

        owner_list_page.click_owners_button()
        owner_list_page.click_search_button()

        cleanup_owner(owner_id)

        assert owner_list_page.owner_header_is_visible()
        assert owner_list_page.owner_table_is_visible()
        assert owner_list_page.owner_in_table_is_visible(owner_name)

    @pytest.mark.test
    @pytest.mark.nondestructive
    @allure.title("Поиск владельца питомца через строку поиска")
    def test_search_pets_owner_via_search_field(self, driver, base_url, create_owner, cleanup_owner):
        owner_id, owner_data = create_owner
        owner_last_name = owner_data.get('lastName')
        owner_name = owner_data.get('firstName') + ' ' + owner_data.get('lastName')
        owner_list_page = OwnerListPage(driver)

        owner_list_page.open(base_url)
        owner_list_page.click_owners_button()
        owner_list_page.click_search_button()
        owner_list_page.set_lastname_owner_to_search_field(owner_last_name)
        owner_list_page.click_find_owner_button()

        cleanup_owner(owner_id)

        assert owner_list_page.owner_table_is_visible()
        assert owner_list_page.owner_in_table_is_visible(owner_name)

        owners = owner_list_page.owners_in_table_by_name(owner_name)
        for owner in owners:
            assert owner.text == owner_name



