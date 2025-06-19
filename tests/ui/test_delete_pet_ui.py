import pytest
import allure

from page_objects.owner_information_page import OwnerInformationPage


@pytest.mark.regress
@pytest.mark.ui
class TestDeletePetUI:
    """ """

    @pytest.mark.nondestructive
    @allure.title("Удаление питомца у владельца")
    def test_delete_pet_ui(
        self, driver, base_url, open_owner_information_page_with_pet, cleanup_owner
    ):
        owner_id, owner_data, data_new_pet = open_owner_information_page_with_pet
        owner_list_page = OwnerInformationPage(driver)

        owner_list_page.click_delete_pet_button()

        cleanup_owner(owner_id)

        assert not owner_list_page.pet_table_is_visible()
