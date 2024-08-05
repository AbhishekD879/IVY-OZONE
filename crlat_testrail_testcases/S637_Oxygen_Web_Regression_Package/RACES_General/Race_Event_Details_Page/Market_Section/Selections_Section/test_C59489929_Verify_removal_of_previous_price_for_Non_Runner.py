import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.
@vtest
class Test_C59489929_Verify_removal_of_previous_price_for_Non_Runner(Common):
    """
    TR_ID: C59489929
    NAME: Verify removal of previous price for Non-Runner
    DESCRIPTION: This test case is to verify not to display previous odds of Non-Runner
    PRECONDITIONS: Non-runner horse should have previous odds
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_click_on_the_event_which_has_non_runner_information_with_previous_odds(self):
        """
        DESCRIPTION: Click on the event which has Non-Runner information with previous odds
        EXPECTED: If non runner horse has previous odds it should not display
        EXPECTED: ![](index.php?/attachments/get/115417211)
        """
        pass
