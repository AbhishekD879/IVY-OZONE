import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C9726293_CMS_Verify_showing_Section_Field_as_Sub_Menu_on_Promotion_in_CMS(Common):
    """
    TR_ID: C9726293
    NAME: [CMS] Verify showing Section Field as Sub Menu on Promotion in CMS
    DESCRIPTION: This test case verifies showing Section Field as Sub Menu on Promotion in CMS
    PRECONDITIONS: Navigate to Oxygen CMS (Coral/Ladbrokes)
    PRECONDITIONS: Go to 'Promotion' page from Navigation menu
    PRECONDITIONS: Add new Promotion with unique Promo ID
    PRECONDITIONS: Back to Main navigation in CMS
    """
    keep_browser_open = True

    def test_001_verify_that_sections_item_is_displayed_as_promotion_sub_menu(self):
        """
        DESCRIPTION: Verify that 'Sections' item is displayed as Promotion Sub Menu
        EXPECTED: User is able to see 'Sections' as Sub Menu
        """
        pass

    def test_002_tap_on_section_item_and_verify_that_user_is_navigated_to_promotions_sections_screen(self):
        """
        DESCRIPTION: Tap on 'Section' item and verify that user is navigated to 'Promotions Sections' screen
        EXPECTED: User is navigated to 'Promotions Sections' screen
        """
        pass

    def test_003___tap_create_a_new_promotions_sections_button_and_enter_promotions_sections_name__tap_save_button(self):
        """
        DESCRIPTION: - Tap 'Create a New Promotions Sections' button and enter Promotions Sections name
        DESCRIPTION: - Tap 'Save' button
        EXPECTED: User is redirected to 'Edit Promotions Sections' screen
        """
        pass

    def test_004___enter_promotion_id_take_promo_id_from_promotion_into_promotions_ids_field__tap_save_changes_button_and_verify_that_new_section_is_created(self):
        """
        DESCRIPTION: - Enter 'Promotion ID' (take Promo ID from Promotion) into 'Promotions Ids' field
        DESCRIPTION: - Tap 'Save changes' button and verify that New Section is created
        EXPECTED: The New Promotion Section is created
        """
        pass

    def test_005_verify_that_sections_in_the_list_of_promotions_sections_in_cms_are_drag_and_droppable(self):
        """
        DESCRIPTION: Verify that 'Sections' in the List of Promotions Sections in CMS are drag and droppable
        EXPECTED: Section items are drag and droppable
        """
        pass

    def test_006_navigate_to_application_and_go_to_promotions_page_from_carousel_menu(self):
        """
        DESCRIPTION: Navigate to Application and go to 'Promotions' page from 'Carousel-menu'
        EXPECTED: User is redirected to 'Promotions' page
        """
        pass

    def test_007_verify_that_sections_order_in_cms_reflect_the_order_sections_are_shown_on_promotion_page_on_app(self):
        """
        DESCRIPTION: Verify that Sections order in CMS reflect the order Sections are shown on 'Promotion' Page on App
        EXPECTED: Sections order in CMS reflect the order Sections are shown on 'Promotion' Page
        """
        pass
