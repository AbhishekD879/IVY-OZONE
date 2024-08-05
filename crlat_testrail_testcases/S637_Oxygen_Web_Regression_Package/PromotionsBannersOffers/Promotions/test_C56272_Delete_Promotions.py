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
class Test_C56272_Delete_Promotions(Common):
    """
    TR_ID: C56272
    NAME: Delete Promotions
    DESCRIPTION: This test case verifies removing of promotions.
    PRECONDITIONS: To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/promotions
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
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

    def test_003_add_promotion_if_there_are_no_promotions(self):
        """
        DESCRIPTION: Add Promotion if there are no Promotions
        EXPECTED: "New Promotion NAME created" message appears
        """
        pass

    def test_004_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_005_tap_promotions_icon_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap 'Promotions' icon on Module Selector ribbon
        EXPECTED: 'Promotions' page is opened
        """
        pass

    def test_006_verify_presence_of_previous_added_promotions(self):
        """
        DESCRIPTION: Verify presence of previous added Promotions
        EXPECTED: * Previous added Promotion is shown on 'Promotions' page
        EXPECTED: * All data is displayed according to CMS
        """
        pass

    def test_007_back_to_cms___promotions_page(self):
        """
        DESCRIPTION: Back to CMS -> Promotions page
        EXPECTED: 
        """
        pass

    def test_008_click_on_remove_button_for_particular_promotion(self):
        """
        DESCRIPTION: Click on "Remove" button for particular Promotion
        EXPECTED: Remove completed popup with "Promotion is removed" message appears
        """
        pass

    def test_009_back_to_oxygen_app__promotions_page(self):
        """
        DESCRIPTION: Back to Oxygen app ->Promotions page
        EXPECTED: 
        """
        pass

    def test_010_verify_absence_of_previous_removed_promotion(self):
        """
        DESCRIPTION: Verify absence of previous removed Promotion
        EXPECTED: Previous removed Promotion is not displayed anymore
        """
        pass

    def test_011_repeat_steps_7_8_for_expiredinactive_promotions(self):
        """
        DESCRIPTION: Repeat steps #7-8 for expired/inactive promotions
        EXPECTED: Deleted promotions are no longer available on the front end and on the CMS
        """
        pass
