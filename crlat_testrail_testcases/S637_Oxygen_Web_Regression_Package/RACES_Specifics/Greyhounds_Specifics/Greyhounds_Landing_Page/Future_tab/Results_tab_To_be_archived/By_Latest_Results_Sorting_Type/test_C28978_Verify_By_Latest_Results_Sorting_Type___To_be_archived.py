import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28978_Verify_By_Latest_Results_Sorting_Type___To_be_archived(Common):
    """
    TR_ID: C28978
    NAME: Verify 'By Latest Results' Sorting Type  -  To be archived
    DESCRIPTION: This test case verifies 'Results' tab when 'By  Latest Results' sorting type is selected
    PRECONDITIONS: In order to get information related verified event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   *XXX - an event ID;*
    PRECONDITIONS: *   *X.XX - current supported version of OpenBet release*.
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_from_the_sports_menu_ribbon_select_greyhounds_icon(self):
        """
        DESCRIPTION: From the sports menu ribbon select 'Greyhounds' icon
        EXPECTED: 'Greyhound' landing page is opened
        """
        pass

    def test_003_tap_results_tab(self):
        """
        DESCRIPTION: Tap 'Results' tab
        EXPECTED: *   'Results' tab is opened
        EXPECTED: *   **'By  Latest Results'** sorting type is selected by default
        """
        pass

    def test_004_verify_results_section_header(self):
        """
        DESCRIPTION: Verify Result's section header
        EXPECTED: *   Header consists of Event off time and Event name (e.g. 4:15 Down Royal)
        EXPECTED: *   Event off time corresponds to the race local time (see **'name' **attribute from the SIte Server)
        EXPECTED: *   Event name corresponds to the Site Server response (**'name' **attribute)
        """
        pass

    def test_005_check_section_content(self):
        """
        DESCRIPTION: Check section content
        EXPECTED: List of the 5 most recent results is shown
        EXPECTED: All 5 results are expanded by default
        EXPECTED: Result section is expandable / collapsible
        """
        pass

    def test_006_check_event_section(self):
        """
        DESCRIPTION: Check event section
        EXPECTED: *   Each event is in separate block
        EXPECTED: *   Event section contains 4 columns: Place, Trap, Greyhounds, Price (SP) and Each Way Terms (if available)
        """
        pass
