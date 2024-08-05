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
class Test_C59489921_Verify_that_Non_Runners_is_displayed_below_the_horse_names(Common):
    """
    TR_ID: C59489921
    NAME: Verify that "Non-Runners" is displayed below the horse names.
    DESCRIPTION: Verify that "Non-Runners" is displayed below the horse names.
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

    def test_004_scroll_down_to_the_non_runner_selections_from_any_marketindexphpattachmentsget111391783(self):
        """
        DESCRIPTION: Scroll down to the Non-Runner selections from any market
        DESCRIPTION: ![](index.php?/attachments/get/111391783)
        EXPECTED: User should be able to see "Non-Runner" below the Horse name
        """
        pass
