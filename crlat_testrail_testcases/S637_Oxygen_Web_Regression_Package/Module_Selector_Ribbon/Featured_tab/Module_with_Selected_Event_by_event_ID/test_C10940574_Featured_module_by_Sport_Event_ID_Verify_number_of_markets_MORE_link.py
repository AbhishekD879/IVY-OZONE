import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C10940574_Featured_module_by_Sport_Event_ID_Verify_number_of_markets_MORE_link(Common):
    """
    TR_ID: C10940574
    NAME: Featured module by <Sport> Event ID: Verify '<number of markets> MORE >' link
    DESCRIPTION: This test case verifies '<number of markets> MORE >' link on the Event section.
    PRECONDITIONS: 1.  Active Featured modules by EventID(not Outright Event with primary market) is created in CMS and displayed on Featured tab in app. Make sure you have events with one market and with more than one market in those modules.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3.  In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: On the Featured tab calculation of markets is implemented in another way as on Landing pages. The following filter is used:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForEvent/XXX,...,XXX?count=event:market&simpleFilter=event.siteChannels:contains:M
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XXX,...,XXX - list of Event ID's
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    """
    keep_browser_open = True

    def test_001_navigate_to_module_that_has_event_with_multiple_markets(self):
        """
        DESCRIPTION: Navigate to module that has Event with multiple markets
        EXPECTED: 
        """
        pass

    def test_002_verify_number_of_available_markets_more__link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '<number of available markets> MORE >' link for event with several markets
        EXPECTED: **CORAL:**
        EXPECTED: Link is shown under Price/Odds buttons of event in format:
        EXPECTED: **"<number of available markets> MORE >"**
        EXPECTED: **LADBROKES:**
        EXPECTED: Link is shown over Price/Odds buttons of event in format:
        EXPECTED: **"<number of available markets> MORE >"**
        """
        pass

    def test_003_verify_number_of_extra_markets_in_brackets(self):
        """
        DESCRIPTION: Verify number of extra markets in brackets
        EXPECTED: For **pre-match** events number of markets correspond to:
        EXPECTED: 'Number of all markets - **1**'
        EXPECTED: For **BIP **events number of markets correspond to:
        EXPECTED: 'Number of markets with **'isMarketBetInRun="true"' **attribute - **1**'
        """
        pass

    def test_004_tap_number_of_markets_more__link(self):
        """
        DESCRIPTION: Tap '<number of markets> MORE >' link
        EXPECTED: '<number of markets> MORE >' link leads to the Event Details page
        """
        pass

    def test_005_navigate_to_module_that_has_event_with_single_market_and_verify_number_of_markets_more__link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Navigate to module that has Event with single market and Verify '<number of markets> MORE >' link for event with ONLY one market
        EXPECTED: '<number of markets> MORE >' link is not shown on the Event section
        """
        pass
