import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.promotions_banners_offers
@vtest
class Test_C15229028_CMS_Verify_Promotion_display_order_within_Various_Sections(Common):
    """
    TR_ID: C15229028
    NAME: [CMS] Verify Promotion display order within Various Sections
    DESCRIPTION: This test case verifies  Promotion is displayed according to display order set in CMS within Various Sections
    PRECONDITIONS: Make sure GroupBySection checkbox is enabled in CMS>System Config>Promotions
    PRECONDITIONS: Set Promotions is CMS:
    PRECONDITIONS: * Navigate to Oxygen CMS (Coral/Ladbrokes)
    PRECONDITIONS: * Go to 'Promotion' page from Navigation menu
    PRECONDITIONS: * Add 3 or more Promotions with Promo IDs
    PRECONDITIONS: * Add a new Section with Promo IDs of  previously added Promotions
    """
    keep_browser_open = True

    def test_001_navigate_to_coralladbrokes_application_and_go_to_promotions_page_from_carousel_menu(self):
        """
        DESCRIPTION: Navigate to Coral/Ladbrokes Application and go to 'Promotions' page from 'Carousel-menu'
        EXPECTED: User is redirected to 'Promotions' page
        """
        pass

    def test_002_verify_that_section_with_promotions_created_in_preconditions_is_displayed(self):
        """
        DESCRIPTION: Verify that Section with promotions created in preconditions is displayed
        EXPECTED: Section with promotions created in preconditions is displayed
        """
        pass

    def test_003_verify_the_order_of_promotions(self):
        """
        DESCRIPTION: Verify the order of Promotions
        EXPECTED: Promotions order is the same as set in CMS ( e.g. first id set is the first promotion to display)
        """
        pass

    def test_004__open_cms__promotions_section_created_previously_section__edit_promotions_order_by_changing_order_of_ids_save_changes(self):
        """
        DESCRIPTION: * Open CMS > Promotions> Section> Created previously section > Edit promotions order by changing order of ids
        DESCRIPTION: * Save Changes
        EXPECTED: Changes are saved
        """
        pass

    def test_005__return_back_to__coralladbrokes_application_promotions_page_verify_the_order_of_promotions_within_the_section(self):
        """
        DESCRIPTION: * Return back to  Coral/Ladbrokes Application 'Promotions' page
        DESCRIPTION: * Verify the order of Promotions within the section
        EXPECTED: Promotions order is the same as set in CMS
        """
        pass
