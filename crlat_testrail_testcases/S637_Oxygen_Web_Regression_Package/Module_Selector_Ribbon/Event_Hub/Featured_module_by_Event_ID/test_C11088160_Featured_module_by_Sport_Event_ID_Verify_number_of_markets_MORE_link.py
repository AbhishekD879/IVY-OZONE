import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C11088160_Featured_module_by_Sport_Event_ID_Verify_number_of_markets_MORE_link(Common):
    """
    TR_ID: C11088160
    NAME: Featured module by <Sport> Event ID: Verify '<number of markets> MORE >' link
    DESCRIPTION: This test case verifies '<number of markets> MORE >' link on the Event section.
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Module by <Sport> EventId(not Outright Event with the primary market) is created in EventHub. Make sure you have events with one market and with more than one market in those modules.
    PRECONDITIONS: 3. A user is on Homepage > EventHub tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: In order to check event data use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: On the Featured tab calculation of markets is implemented in another way as on Landing pages. The following filter is used:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForEvent/XXX,...,XXX?count=event:market&simpleFilter=event.siteChannels:contains:M
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: XXX,...,XXX - list of Event ID's
    """
    keep_browser_open = True

    def test_001_navigate_to_the_module_that_has_event_with_multiple_markets(self):
        """
        DESCRIPTION: Navigate to the module that has Event with multiple markets
        EXPECTED: 
        """
        pass

    def test_002_verify_ltnumber_of_available_marketsgt_more_gt_link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '&lt;number of available markets&gt; MORE &gt;' link for event with several markets
        EXPECTED: **CORAL:**
        EXPECTED: Link is shown under Price/Odds buttons of event in format:
        EXPECTED: **"&lt;number of available markets&gt; MORE &gt;"**
        EXPECTED: **LADBROKES:**
        EXPECTED: Link is shown over Price/Odds buttons of event in format:
        EXPECTED: **"&lt;number of available markets&gt; MORE &gt;"**
        """
        pass

    def test_003_verify_the_number_of_extra_markets_in_brackets(self):
        """
        DESCRIPTION: Verify the number of extra markets in brackets
        EXPECTED: For **pre-match** events number of markets correspond to:
        EXPECTED: 'Number of all markets - **1**'
        EXPECTED: For **BIP** events number of markets correspond to:
        EXPECTED: 'Number of markets with **'isMarketBetInRun="true"' **attribute - 1**'
        """
        pass

    def test_004_tap_ltnumber_of_marketsgt_more_gt_link(self):
        """
        DESCRIPTION: Tap '&lt;number of markets&gt; MORE &gt;' link
        EXPECTED: '&lt;number of markets&gt; MORE &gt;' link leads to the Event Details page
        """
        pass

    def test_005_navigate_to_the_module_that_has_event_with_a_single_market_and_verify_ltnumber_of_marketsgt_more_gt_link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Navigate to the module that has Event with a single market and Verify '&lt;number of markets&gt; MORE &gt;' link for event with ONLY one market
        EXPECTED: '&lt;number of markets&gt; MORE &gt;' link is not shown on the Event section
        """
        pass
