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
class Test_C10350053_CMS_Verify_showing_Promotion_in_More_from_Ladbrokes_Coral_Section(Common):
    """
    TR_ID: C10350053
    NAME: [CMS] Verify showing Promotion in More from Ladbrokes/Coral Section
    DESCRIPTION: This test case verifies showing Promotion in More from Ladbrokes/Coral Section
    PRECONDITIONS: Navigate to Oxygen CMS (Coral/Ladbrokes)
    PRECONDITIONS: Go to 'Promotion' page from Navigation menu
    PRECONDITIONS: Add new Promotion without Promo ID
    """
    keep_browser_open = True

    def test_001_navigate_to_application_and_go_to_promotions_page_from_carousel_menu(self):
        """
        DESCRIPTION: Navigate to Application and go to 'Promotions' page from 'Carousel-menu'
        EXPECTED: User is redirected to 'Promotions' page
        """
        pass

    def test_002_scroll_page_down_and_verify_that_promotion_without_promo_id_is_displayed_in_more_from_ladbrokescoral_section(self):
        """
        DESCRIPTION: Scroll page down and verify that Promotion without Promo ID is displayed in 'More from Ladbrokes/Coral' Section
        EXPECTED: Promotion which is not listed within Section is displayed in 'More from Ladbrokes/Coral' Section
        """
        pass
