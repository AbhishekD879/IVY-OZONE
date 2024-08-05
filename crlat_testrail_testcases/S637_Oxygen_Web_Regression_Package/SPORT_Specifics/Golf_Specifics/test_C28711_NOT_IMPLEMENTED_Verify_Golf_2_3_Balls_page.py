import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28711_NOT_IMPLEMENTED_Verify_Golf_2_3_Balls_page(Common):
    """
    TR_ID: C28711
    NAME: NOT IMPLEMENTED: Verify Golf '2/3 Balls' page
    DESCRIPTION: This test case verifies content of Golf '2/3 Balls' page
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-12454: Display content for 2 & 3 Balls Golf events (Desktop)
    DESCRIPTION: BMA-10373: Display content for 2 & 3 Balls Golf events (Mobile)
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_golf_page(self):
        """
        DESCRIPTION: Go to 'Golf' page
        EXPECTED: *   Golf Landing Page is opened
        EXPECTED: *   '2/3 Balls' tab is opened by default
        """
        pass

    def test_003_verify_sub_tabs_in_the_23_balls_page(self):
        """
        DESCRIPTION: Verify sub tabs in the '2/3 Balls' page
        EXPECTED: *   PGA (1st tab) and European (2nd tab) are displayed
        EXPECTED: *   Tab that contains next starting event is opened by default
        """
        pass

    def test_004_clicktap_on_pga_tab(self):
        """
        DESCRIPTION: Click/Tap on PGA tab
        EXPECTED: *   PGA tab is opened
        EXPECTED: *   Enhanced Multiples section is displayed at the top of the page
        """
        pass

    def test_005_verify_markets_in_the_pga_page(self):
        """
        DESCRIPTION: Verify markets in the PGA page
        EXPECTED: *   Name of available markets is displayed in the PGA page
        EXPECTED: *   Markets that contain the most current event are expanded by default
        EXPECTED: *   All other markets are collapsed by default
        EXPECTED: *   All markets chronologically based on event start time
        EXPECTED: *   All markets sections are expandable/collapsable
        """
        pass

    def test_006_verify_tournaments_in_the_pga_page(self):
        """
        DESCRIPTION: Verify tournaments in the PGA page
        EXPECTED: *   Name of available tournaments is displayed in the PGA page
        EXPECTED: *   Tournaments that contain the most current event are expanded by default
        EXPECTED: *   All other tournaments are collapsed by default
        EXPECTED: *   All tournaments sections are expandable/collapsable
        """
        pass

    def test_007_verify_events_in_the_pga_page(self):
        """
        DESCRIPTION: Verify events in the PGA page
        EXPECTED: Events are displayed within Tournament section
        """
        pass

    def test_008_clicltap_on_european_tab(self):
        """
        DESCRIPTION: Clicl/Tap on European tab
        EXPECTED: *   European tab is opened
        EXPECTED: *   Enhanced Multiples section is displayed at the top of the page
        """
        pass

    def test_009_repeat_steps_5_7_but_for_european_tab(self):
        """
        DESCRIPTION: Repeat steps 5-7 but for European tab
        EXPECTED: 
        """
        pass
