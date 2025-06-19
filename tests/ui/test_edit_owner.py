import pytest
import allure

from page_objects.edit_owner_page import EditOwnerPage
from page_objects.owner_information_page import OwnerInformationPage


@pytest.mark.regress
@pytest.mark.ui
class TestEditOwner:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Редактирование владельца питомца")
    def test_edit_pets_owner(
        self,
        driver,
        base_url,
        open_owner_information_page_without_pet,
        cleanup_owner,
        generate_owner_data,
    ):
        owner_id, owner_data_before_test = open_owner_information_page_without_pet
        owner_data_after_test = generate_owner_data
        first_name = owner_data_after_test.get("firstName")
        last_name = owner_data_after_test.get("lastName")
        address = owner_data_after_test.get("address")
        city = owner_data_after_test.get("city")
        telephone = owner_data_after_test.get("telephone")
        owner_list_page = OwnerInformationPage(driver)
        edit_owner_page = EditOwnerPage(driver)
        owner_information_page = OwnerInformationPage(driver)

        owner_list_page.click_edit_owner_button()
        edit_owner_page.set_owner_data(first_name, last_name, address, city, telephone)
        edit_owner_page.click_update_owner_button()

        owner_information = owner_information_page.get_owner_information()

        cleanup_owner(owner_id)

        assert owner_data_after_test.get("firstName") in owner_information
        assert owner_data_after_test.get("lastName") in owner_information
        assert owner_data_after_test.get("address") in owner_information
        assert owner_data_after_test.get("telephone") in owner_information

    @pytest.mark.nondestructive
    @allure.title("Возврат на страницу информации без редактирования")
    def test_back_button_returns_to_owner_information_page(
        self,
        driver,
        base_url,
        open_owner_information_page_without_pet,
        cleanup_owner,
        generate_owner_data,
    ):
        owner_id, owner_data_before_test = open_owner_information_page_without_pet
        owner_data_after_test = generate_owner_data
        first_name = owner_data_after_test.get("firstName")
        last_name = owner_data_after_test.get("lastName")
        address = owner_data_after_test.get("address")
        city = owner_data_after_test.get("city")
        telephone = owner_data_after_test.get("telephone")
        owner_list_page = OwnerInformationPage(driver)
        edit_owner_page = EditOwnerPage(driver)
        owner_information_page = OwnerInformationPage(driver)

        owner_list_page.click_edit_owner_button()
        edit_owner_page.set_owner_data(first_name, last_name, address, city, telephone)
        edit_owner_page.click_back_button()

        owner_information = owner_information_page.get_owner_information()

        cleanup_owner(owner_id)

        assert owner_data_before_test.get("firstName") in owner_information
        assert owner_data_before_test.get("lastName") in owner_information
        assert owner_data_before_test.get("address") in owner_information
        assert owner_data_before_test.get("telephone") in owner_information
