import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C237150_devlogCMS_control_of_Free_bets_page_if_there_are_no_free_bets_available(Common):
    """
    TR_ID: C237150
    NAME: devlogCMS control of Free bets page if there are no free bets available
    DESCRIPTION: This test case verifies CMS control of Free bets page if there are no free bets available
    PRECONDITIONS: 1. User should not have any free bets added to his account
    PRECONDITIONS: 2. To load CMS use the next link:
    PRECONDITIONS: CMS_ENDPOINT/keystone/static-blocks
    PRECONDITIONS: where CMS_ENDPOINT can be found using devlog
    PRECONDITIONS: NOTE: For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_on_account_menu_icon(self):
        """
        DESCRIPTION: Tap on Account menu icon
        EXPECTED: Account menu is opened
        """
        pass

    def test_003_tap_offers__free_bets_item(self):
        """
        DESCRIPTION: Tap 'OFFERS & FREE BETS' item
        EXPECTED: * 'OFFERS & FREE BETS' menu is opened
        """
        pass

    def test_004_tap_sports_free_bets_item(self):
        """
        DESCRIPTION: Tap 'SPORTS FREE BETS' item
        EXPECTED: * 'MY FREEBETS/BONUSES' page is opened
        EXPECTED: * Make sure that  text has been taken from 'No Freebets message' static block in CMS
        """
        pass

    def test_005_go_to_cms_and_make_some_changes_in_no_freebets_message_static_block_and_save_it(self):
        """
        DESCRIPTION: Go to CMS and make some changes in 'No freebets message' static block and save it
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_007_go_to_free_bets_page_and_verify_changes_made_on_step_5(self):
        """
        DESCRIPTION: Go to Free bets page and verify changes made on step #5
        EXPECTED: Changes made in CMS are displayed successfully
        """
        pass
