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
class Test_C59559_Verify_Enhanced_Multiples_events_displaying_on_Specials_tab(Common):
    """
    TR_ID: C59559
    NAME: Verify 'Enhanced Multiples' events displaying on Specials tab
    DESCRIPTION: This test case verifies how Events from Enhanced Multiples type (typeId =2562) will be displayed on Specials tab
    PRECONDITIONS: 1. Make sure special events are available
    PRECONDITIONS: 2. Make sure events are from typeId = 2652
    PRECONDITIONS: 3. In order to configure special events go to the Open Bet TI, find the event, open market and tick 'Special' flag
    PRECONDITIONS: 4. In order to get a list of special events use link: {domain}/openbet-ssviewer/Drilldown/2.19/EventToOutcomeForClass/{classIds}?simpleFilter=event.categoryId:intersects:16&simpleFilter=event.siteChannels:contains:M&simpleFilter=event.suspendAtTime:greaterThan:ZZZZ-YY-XXT10:34:30.000Z&existsFilter=event:simpleFilter:market.drilldownTagNames:intersects:MKTFLAG_SP&prune=event&prune=market
    PRECONDITIONS: where, ZZZZ-YY-XX - is a current date
    PRECONDITIONS: Note, event is set as special when typeFlagCodes = MKTFLAG_SP
    PRECONDITIONS: Where domain is:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk - for TST2 environment
    PRECONDITIONS: https://ss-aka-ori-stg2.coral.co.uk - for STG2 environment
    PRECONDITIONS: https://ss-aka-ori.coral.co.uk - for HL and PROD environments
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Oxygen app is opened
        """
        pass

    def test_002_go_to_football___specials_tab(self):
        """
        DESCRIPTION: Go to 'Football' -> 'Specials' tab
        EXPECTED: 'Specials' tab is opened
        """
        pass

    def test_003_open_enhanced_multiples_section(self):
        """
        DESCRIPTION: Open 'Enhanced Multiples' section
        EXPECTED: Events from Enhanced Multiples type are shown
        EXPECTED: Enhanced Multiples section has a fixture header with event date displayed
        """
        pass

    def test_004_verify_events_displaying(self):
        """
        DESCRIPTION: Verify events displaying
        EXPECTED: Events from EM type are shown as a list of selections (no market name or event name)
        EXPECTED: All outcomes from EM market are shown
        EXPECTED: Each outcome is shown in a separate section
        """
        pass

    def test_005_verify_outcome_section(self):
        """
        DESCRIPTION: Verify outcome section
        EXPECTED: Outcome name with corresponding price odds button is shown
        EXPECTED: Time of special event is shown under the outcome name
        EXPECTED: Time corresponds to the SS response
        """
        pass

    def test_006_verify_outcome_name(self):
        """
        DESCRIPTION: Verify outcome name
        EXPECTED: Outcome name corresponds to the Site Server response
        EXPECTED: **Each outcome is shown separately **(of events with more than one market and more than one outcome, of  events one market and more than one outcome, of  events with one market and one outcome)
        """
        pass

    def test_007_check_priceodds_button_near_the_selection_name(self):
        """
        DESCRIPTION: Check price/odds button near the selection name
        EXPECTED: Corresponding price/odds button is shown
        EXPECTED: In case price is absent -> nothing is shown instead of price/odds, just outcome name is shown
        """
        pass

    def test_008_repeat_steps__3___7_for_different_types_of_em_events_mtch_tnmt_etc_events(self):
        """
        DESCRIPTION: Repeat steps # 3 - 7 for different types of EM events (MTCH, TNMT etc. events)
        EXPECTED: 
        """
        pass
