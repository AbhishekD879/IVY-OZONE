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
class Test_C1045450_Verify_undisplayed_events_for_Result_tab___To_be_archived(Common):
    """
    TR_ID: C1045450
    NAME: Verify undisplayed events for 'Result' tab  -  To be archived
    DESCRIPTION: This test case verifies undisplayed events that should be shown in the 'Results' tab
    DESCRIPTION: NOTE, only "Win or Each Way" market should be shown in 'Result' tab
    PRECONDITIONS: To retrieve data from the Site Server use the following:
    PRECONDITIONS: 1)  Events are set resulted in Backoffice TI
    PRECONDITIONS: 2) To verify Results for events use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/HistoricDrilldown/X.XX/ResultedEvent/XXXXXX?translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: *XXXXXX - an event id (Note, several event ids can also be pasted using comma as a separator. e.g.1574736,1574926**)*
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: See attributes:
    PRECONDITIONS: startTime - to verify event start date
    PRECONDITIONS: typeFlagCodes - to identify group the event belongs to
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_on_the_homepage_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On the homepage tap 'Greyhounds' icon from the Sports Menu Ribbon
        EXPECTED: 'Greyhounds' landing page is opened
        EXPECTED: 'Today tab' tab is displayed
        """
        pass

    def test_003_tap_results_tab(self):
        """
        DESCRIPTION: Tap 'Results' tab
        EXPECTED: 'Results' tab is opened
        EXPECTED: **'By Latest Results' **sorting type is selected by default
        """
        pass

    def test_004_in_ti_undisplay_market_of_one_of_the_existing_resulted_events(self):
        """
        DESCRIPTION: In TI: Undisplay market of one of the existing resulted events
        EXPECTED: Event is shown undisplayed
        """
        pass

    def test_005_navigate_to_the_app_and_refresh_result_tab(self):
        """
        DESCRIPTION: Navigate to the app and refresh 'Result' tab
        EXPECTED: Undisplayed event is shown
        """
        pass

    def test_006_repeat_step_4_5_for_event_and_selection(self):
        """
        DESCRIPTION: Repeat step 4-5 for event and selection
        EXPECTED: Undisplayed event is shown
        """
        pass
