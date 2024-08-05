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
class Test_C60094820_Verify_the_silk_change_when_a_horse_is_declared_as_Non_Runner(Common):
    """
    TR_ID: C60094820
    NAME: Verify the silk change when a horse is declared as Non-Runner
    DESCRIPTION: Verify that when a horse is declared as Non-Runner, silk changes to generic silk.
    PRECONDITIONS: 1: Horse racing event should be available
    PRECONDITIONS: 2: Bespoke silks should be available for the event
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

    def test_003_click_on_any_horse_racing_event_which_has_bespoke_silks_available(self):
        """
        DESCRIPTION: Click on any horse racing event which has bespoke silks available.
        EXPECTED: 1: User should be navigated to the Event details page
        EXPECTED: 2: User should be able to see all the Horse details and silks
        """
        pass

    def test_004_configure_in_open_bet_for_one_of_the_selection_as_non_runner(self):
        """
        DESCRIPTION: Configure in Open Bet for one of the selection as Non-Runner
        EXPECTED: Open Bet configuration should be successful
        """
        pass

    def test_005_navigate_back_to_event_details_page_in_front_end_and_scroll_to_the_selection_which_was_configured_non_runner_in_open_bet(self):
        """
        DESCRIPTION: Navigate back to event details page in Front end and scroll to the selection which was configured Non-Runner in Open Bet
        EXPECTED: 1: "Non-Runner" should be displayed below the horse name
        EXPECTED: 2: Generic (default) silk should be displayed
        EXPECTED: 3: Bespoke silk should no longer be displayed
        """
        pass
