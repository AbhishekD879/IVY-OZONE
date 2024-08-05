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
class Test_C28446_Verify_number_of_available_markets_Markets_link(Common):
    """
    TR_ID: C28446
    NAME: Verify '<number of available markets> Markets' link
    DESCRIPTION: This test case verifies '<number of available markets> Markets' ('+<number of available markets> Markets' for desktop) link on the Event section.
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

    def test_002_navigate_to_sport_landing_page(self):
        """
        DESCRIPTION: Navigate to <Sport> landing page
        EXPECTED: *  <Sport> Landing Page is opened
        EXPECTED: *  'Matches' tab is opened by default
        """
        pass

    def test_003_verify_number_of_available_markets_markets_plusnumber_of_available_markets_markets_for_desktop_link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '<number of available markets> Markets' ('+<number of available markets> Markets' for desktop) link for event with several markets
        EXPECTED: For mobile/tablet view:
        EXPECTED: '<number of available markets> Markets' is shown below odds buttons
        EXPECTED: For desktop view:
        EXPECTED: '+<number of available markets> Markets' is shown next to odds buttons
        """
        pass

    def test_004_verify_number_of_extra_markets_in_brackets(self):
        """
        DESCRIPTION: Verify number of extra markets in brackets
        EXPECTED: Number of markets corresponds to:
        EXPECTED: 'Number of all markets - **1**'
        """
        pass

    def test_005_tap_on_number_of_available_markets_markets_plusnumber_of_available_markets_markets_for_desktop_link(self):
        """
        DESCRIPTION: Tap on '<number of available markets> Markets' ('+<number of available markets> Markets' for desktop) link
        EXPECTED: Event Details page opened
        """
        pass

    def test_006_verify_number_of_available_markets_markets_plusnumber_of_available_markets_markets_for_desktop_link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Verify '<number of available markets> Markets' ('+<number of available markets> Markets' for desktop) link for event with ONLY one market
        EXPECTED: Link is not shown on the Event section
        """
        pass
