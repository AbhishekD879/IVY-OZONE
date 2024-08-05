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
class Test_C29319_No_active_Promotions(Common):
    """
    TR_ID: C29319
    NAME: No active Promotions
    DESCRIPTION: Purpose of this test case is to verify Promotion page without promotions.
    PRECONDITIONS: Proceed to CMS: https://CMS_ENDPOINT/keystone
    PRECONDITIONS: (check CMS_ENDPOINT via devlog function)
    PRECONDITIONS: Make sure there are no active promotions
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be delay up to 5-10 mins before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application.
        EXPECTED: Home page is opened
        """
        pass

    def test_002_tap_promotions_item_on_sport_menu_robbon(self):
        """
        DESCRIPTION: Tap Promotions item on Sport Menu Robbon
        EXPECTED: "Promotions" page is opened
        """
        pass

    def test_003_verify_page_content(self):
        """
        DESCRIPTION: Verify page content
        EXPECTED: There are no active promotions.
        EXPECTED: Text 'No active Promotions at the moment' is displayed.
        """
        pass
