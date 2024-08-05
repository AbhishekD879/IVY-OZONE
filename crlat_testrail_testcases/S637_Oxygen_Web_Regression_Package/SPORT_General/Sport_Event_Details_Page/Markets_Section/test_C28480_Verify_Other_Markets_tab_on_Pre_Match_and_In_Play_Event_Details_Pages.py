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
class Test_C28480_Verify_Other_Markets_tab_on_Pre_Match_and_In_Play_Event_Details_Pages(Common):
    """
    TR_ID: C28480
    NAME: Verify 'Other Markets' tab on Pre-Match and In-Play Event Details Pages 
    DESCRIPTION: This test case verifies 'Other Markets' tab on Pre-Match and In-Play Event Details Pages.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/SportToCollection?translationLang=LL
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002_navigate_to_sports_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sports> Landing page
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_clicktap_on_event_name_or_more_link_in_the_event_card(self):
        """
        DESCRIPTION: Click/Tap on Event name or 'More' link in the event card
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_clicktap_on_other_markets_tab_and_verify_present_markets(self):
        """
        DESCRIPTION: Click/Tap on 'Other Markets' tab and verify present markets
        EXPECTED: Market's **collectionNames **doesn't contain any** **name of collection or **collectionNames **is absent at all
        """
        pass

    def test_005_verify_present_market_type_sections(self):
        """
        DESCRIPTION: Verify present market type sections
        EXPECTED: *   The first **two **market type sections are expanded by default
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand  market type sections by tapping the section's header
        """
        pass

    def test_006_verify_market_absence(self):
        """
        DESCRIPTION: Verify market absence
        EXPECTED: Market section is absent if it isn't available in the SiteServer
        """
        pass
