import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28481_Verify_All_Markets_tab(Common):
    """
    TR_ID: C28481
    NAME: Verify 'All Markets' tab
    DESCRIPTION: This test case verifies 'All Markets' tab.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
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

    def test_002_tap_sporticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>'  icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_verify_presence_of_all_market_tab(self):
        """
        DESCRIPTION: Verify presence of 'All Market' tab
        EXPECTED: 'All Market' tab is always first on the Markets Ribbon
        """
        pass

    def test_005_tap_all_markets_tab(self):
        """
        DESCRIPTION: Tap 'All Markets' tab
        EXPECTED: All existing markets for verified event are shown
        """
        pass

    def test_006_verify_present_market_type_sections(self):
        """
        DESCRIPTION: Verify present market type sections
        EXPECTED: *   The first **two **market type sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand  market type sections by tapping the section's header
        """
        pass
