import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C59489922_Verify_the_generic_silk_displayed_for_Non_Runner(Common):
    """
    TR_ID: C59489922
    NAME: Verify the generic silk displayed for Non-Runner
    DESCRIPTION: Verify that Generic (default) silk is displayed for a "Non-Runner" as per the designs mentioned in Zeplin
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Event should have atleast one Non-Runner
    PRECONDITIONS: (In Open Bet make one selection as Non- Runner)
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

    def test_003_click_on_the_event_which_has_atleast_one_non_runner(self):
        """
        DESCRIPTION: Click on the event which has atleast one Non-Runner
        EXPECTED: User should be navigated to the Event details page
        """
        pass

    def test_004_scroll_down_to_the_non_runner_selections_from_any_marketindexphpattachmentsget111391784(self):
        """
        DESCRIPTION: Scroll down to the Non-Runner selections from any market
        DESCRIPTION: ![](index.php?/attachments/get/111391784)
        EXPECTED: 1: Non-Runner should be displayed below the horse name
        EXPECTED: 2: Generic (default) silk should be displayed for the Horse
        """
        pass
