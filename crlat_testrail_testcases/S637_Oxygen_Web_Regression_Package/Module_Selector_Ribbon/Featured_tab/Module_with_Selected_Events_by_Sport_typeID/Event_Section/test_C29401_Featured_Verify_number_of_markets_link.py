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
class Test_C29401_Featured_Verify_number_of_markets_link(Common):
    """
    TR_ID: C29401
    NAME: Featured: Verify '+<number of markets>' link
    DESCRIPTION: This test case verifies '+<number of markets>' link on the Event section.
    DESCRIPTION: **Jira ticket:** BMA-1624
    PRECONDITIONS: 1.  Active Featured module by TypeID is created in CMS and displayed on Featured tab in app. Make sure you have events with one market and with more than one market in this module.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3.  In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: '+<number of markets>' link is shown only for events that are retrieved by typeID, for boosted selections link is not displayed.
    PRECONDITIONS: On the Featured tab calculation of markets is implemented in another way as on Landing pages. The following filter is used:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForEvent/XXX,...,XXX?count=event:market&simpleFilter=event.siteChannels:contains:M
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XXX,...,XXX - list of Event ID's
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    """
    keep_browser_open = True

    def test_001_go_to_event_section(self):
        """
        DESCRIPTION: Go to Event section
        EXPECTED: 
        """
        pass

    def test_002_verify_plusnumber_of_markets_link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '+<number of markets>' link for event with several markets
        EXPECTED: Link is shown next to the Price/Odds buttons of event in format:
        EXPECTED: **"+<number of available markets>"**
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

    def test_004_tap_plusnumber_of_markets_link(self):
        """
        DESCRIPTION: Tap '+<number of markets>' link
        EXPECTED: '+<number of markets>' link leads to the Event Details page
        """
        pass

    def test_005_verify_plusnumber_of_markets_link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Verify '+<number of markets>' link for event with ONLY one market
        EXPECTED: '+<number of markets>' link is not shown on the Event section
        """
        pass
