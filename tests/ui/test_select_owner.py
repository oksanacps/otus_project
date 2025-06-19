import pytest
import allure

from page_objects.owner_list_page import OwnerListPage
from page_objects.owner_information_page import OwnerInformationPage


@pytest.mark.smoke
@pytest.mark.ui
class TestSelectOwner:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Выбор владельца питомца в таблице без назначенных питомцев")
    def test_select_pets_owner_without_pets(
        self, driver, base_url, open_owner_information_page_without_pet, cleanup_owner
    ):
        owner_id, owner_data = open_owner_information_page_without_pet
        owner_information_page = OwnerInformationPage(driver)
        owner_information = owner_information_page.get_owner_information()

        cleanup_owner(owner_id)

        assert owner_data.get("firstName") in owner_information
        assert owner_data.get("lastName") in owner_information
        assert owner_data.get("address") in owner_information
        assert owner_data.get("telephone") in owner_information
        assert owner_information_page.pet_header_is_visible()
        assert not owner_information_page.pet_table_is_visible()

    @pytest.mark.nondestructive
    @allure.title("Выбор владельца питомца в таблице c назначенными питомцами")
    def test_select_pets_owner_without_visits(
        self, driver, base_url, open_owner_information_page_with_pet, cleanup_owner
    ):
        owner_id, owner_data, data_new_pet = open_owner_information_page_with_pet
        owner_information_page = OwnerInformationPage(driver)
        owner_information = owner_information_page.get_owner_information()
        pet_information = owner_information_page.get_pet_information()

        cleanup_owner(owner_id)

        assert owner_data.get("firstName") in owner_information
        assert owner_data.get("lastName") in owner_information
        assert owner_data.get("address") in owner_information
        assert owner_data.get("telephone") in owner_information
        assert owner_information_page.pet_header_is_visible()
        assert owner_information_page.pet_table_is_visible()
        assert data_new_pet.get("name") in pet_information
        assert data_new_pet.get("birthDate") in pet_information
        assert data_new_pet.get("type").get("name") in pet_information

    @pytest.mark.nondestructive
    @allure.title("Выбор владельца питомца в таблице c назначенными питомцами")
    def test_select_pets_owner_with_pet_and_visits(
        self,
        driver,
        base_url,
        open_owner_information_page_with_pet_and_visit,
        cleanup_owner,
    ):
        owner_id, owner_data, data_new_pet, visit_data = (
            open_owner_information_page_with_pet_and_visit
        )
        owner_information_page = OwnerInformationPage(driver)
        owner_information = owner_information_page.get_owner_information()
        pet_information = owner_information_page.get_pet_information()
        visit_information = owner_information_page.get_visit_information()

        cleanup_owner(owner_id)

        assert owner_data.get("firstName") in owner_information
        assert owner_data.get("lastName") in owner_information
        assert owner_data.get("address") in owner_information
        assert owner_data.get("telephone") in owner_information
        assert owner_information_page.pet_header_is_visible()
        assert owner_information_page.pet_table_is_visible()
        assert data_new_pet.get("name") in pet_information
        assert data_new_pet.get("birthDate") in pet_information
        assert data_new_pet.get("type").get("name") in pet_information
        assert visit_data.get("date") in visit_information
        assert visit_data.get("description") in visit_information

    @pytest.mark.nondestructive
    @allure.title("Возврат на страницу со списком владельцев")
    def test_back_button_returns_to_owner_list_page(
        self, driver, base_url, open_owner_information_page_without_pet, cleanup_owner
    ):
        owner_id, owner_data = open_owner_information_page_without_pet
        owner_list_page = OwnerListPage(driver)
        owner_information_page = OwnerInformationPage(driver)

        owner_information_page.click_back_button()

        cleanup_owner(owner_id)

        assert owner_list_page.owner_table_is_visible()
