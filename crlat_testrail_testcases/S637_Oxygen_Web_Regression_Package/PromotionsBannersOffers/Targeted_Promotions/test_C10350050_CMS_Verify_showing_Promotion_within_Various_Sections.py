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
class Test_C10350050_CMS_Verify_showing_Promotion_within_Various_Sections(Common):
    """
    TR_ID: C10350050
    NAME: [CMS] Verify showing Promotion within Various Sections
    DESCRIPTION: This test case verifies showing Promotion within Various Sections
    PRECONDITIONS: Navigate to Oxygen CMS (Coral/Ladbrokes)
    PRECONDITIONS: Go to 'Promotion' page from Navigation menu
    PRECONDITIONS: Add two Promotions with Promo IDs
    PRECONDITIONS: Add a new Section with Promo ID of one of previously added Promotions
    PRECONDITIONS: Back to Main navigation in CMS
    """
    keep_browser_open = True

    def test_001_navigate_to_section_sub_menu_and_tap_on_section_nameverify_that_user_is_navigated_to_edit_promotions_sections_page(self):
        """
        DESCRIPTION: Navigate to Section sub menu and tap on Section name
        DESCRIPTION: Verify that user is navigated to 'Edit Promotions Sections' page
        EXPECTED: User is navigated to 'Edit Promotions Sections' page
        """
        pass

    def test_002___update_section_name_and_add_one_more_promo_id_see_preconditions__tap_save_changes_button(self):
        """
        DESCRIPTION: - Update Section name and add one more Promo ID (see preconditions)
        DESCRIPTION: - Tap 'Save Changes' button
        EXPECTED: Updated Section 'Name' and 'Promotion ID' are saved
        """
        pass

    def test_003_navigate_to_application_and_go_to_promotions_page_from_carousel_menu(self):
        """
        DESCRIPTION: Navigate to Application and go to 'Promotions' page from 'Carousel-menu'
        EXPECTED: User is redirected to 'Promotions' page
        """
        pass

    def test_004_verify_that__section_name_and_promotion_id_are_updated_within_their_respective_section(self):
        """
        DESCRIPTION: Verify that  Section 'Name' and 'Promotion ID' are updated within their respective section
        EXPECTED: Section 'Name' and 'Promotion ID' are updated within their respective section
        """
        pass
