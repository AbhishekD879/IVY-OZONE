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
class Test_C56313_Verify_Promotion_page_on_the_front_end_when_Promotions_are_not_set_in_the_CMS(Common):
    """
    TR_ID: C56313
    NAME: Verify Promotion page on the front end when Promotions are not set in the CMS
    DESCRIPTION: Test case verifies promotion page on the front end when Promotions are not set in the CMS
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_promotions_section(self):
        """
        DESCRIPTION: Go to 'Promotions' section
        EXPECTED: 'Promotions' section is opened
        """
        pass

    def test_003_remove_all_existing_promotions(self):
        """
        DESCRIPTION: Remove all existing Promotions
        EXPECTED: Promotions are removed successfully
        """
        pass

    def test_004_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_005_navigate_to_promotions_page_from_sports_menu_ribbon_or_left_navigation_menu(self):
        """
        DESCRIPTION: Navigate to 'Promotions' page from 'Sports Menu Ribbon' or 'Left Navigation' menu
        EXPECTED: 'Promotions' page is opened
        """
        pass

    def test_006_verify_promotions_page(self):
        """
        DESCRIPTION: Verify Promotions Page
        EXPECTED: Message about absence of Promotions is displayed on the page
        """
        pass
