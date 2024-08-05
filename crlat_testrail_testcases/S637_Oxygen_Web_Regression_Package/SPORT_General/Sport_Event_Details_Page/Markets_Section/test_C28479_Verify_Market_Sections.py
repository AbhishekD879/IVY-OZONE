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
class Test_C28479_Verify_Market_Sections(Common):
    """
    TR_ID: C28479
    NAME: Verify Market Sections
    DESCRIPTION: This test case verifies Market sections on Pre-Match and In-Play Event Details Pages.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
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

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> Landing Page
        EXPECTED: <Sport> Landing Page is opened
        """
        pass

    def test_003_clicktap_on_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Click/Tap on Event name or 'More' link on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_verify_present_market_sections(self):
        """
        DESCRIPTION: Verify present Market sections
        EXPECTED: *   The first **two** Market sections are expanded by default **For Mobile/Tablet**
        EXPECTED: *   The first **four** Market sections are expanded by default **For Desktop**
        EXPECTED: *   The remaining sections are collapsed by default
        EXPECTED: *   It is possible to collapse/expand  Market sections by tapping the section's header
        """
        pass

    def test_005_verify_market_names(self):
        """
        DESCRIPTION: Verify Market names
        EXPECTED: Market name corresponds to the '**name**' attribute on Market level
        """
        pass

    def test_006_verify_cash_out_label(self):
        """
        DESCRIPTION: Verify 'CASH OUT' label
        EXPECTED: **'CASH OUT' **label is shown next to the Market Name if available (on Market level)
        """
        pass

    def test_007_verify_order_of_market_sections_for_verified_event(self):
        """
        DESCRIPTION: Verify order of Market sections for verified event
        EXPECTED: Market sections are ordered by:
        EXPECTED: *   Market '**displayOrder**' in ascending order
        EXPECTED: *   Alphanumerically (in case of same 'displayOrder' value)
        """
        pass

    def test_008_please_repeat_steps_4_5_for_all_available_collections_on_event_details_page(self):
        """
        DESCRIPTION: Please repeat steps №4-5 for all available Collections on Event Details Page
        EXPECTED: 
        """
        pass
