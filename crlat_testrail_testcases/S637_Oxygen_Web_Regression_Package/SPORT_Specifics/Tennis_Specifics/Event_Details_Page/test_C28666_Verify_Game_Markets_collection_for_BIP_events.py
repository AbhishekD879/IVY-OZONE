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
class Test_C28666_Verify_Game_Markets_collection_for_BIP_events(Common):
    """
    TR_ID: C28666
    NAME: Verify 'Game Markets' collection for BIP events
    DESCRIPTION: This test case verifies 'Game Markets' collection for BIP events
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-5349 (Tennis Game Markets - Hide when all outcomes are suspended)
    PRECONDITIONS: Make sure that there is 'Game Markets' collection on Event Detail Page and there are the markets avalaible
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Note: need to create a market with market template |Current Game Winner|
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details Page
        EXPECTED: Event Details Page is opened
        EXPECTED: 'Main Markets' collection is opened by default
        """
        pass

    def test_003_go_to_game_markets_collection(self):
        """
        DESCRIPTION: Go to 'Game Markets' collection
        EXPECTED: The list of markets that belongs to 'Game Markets' collection is shown
        EXPECTED: Make sure that there are no markets with all suspened outcomes
        """
        pass

    def test_004_chose_market_within_game_markets_collection(self):
        """
        DESCRIPTION: Chose market within 'Game Markets' collection
        EXPECTED: 
        """
        pass

    def test_005_trigger_the_following_situation_for_this_marketmarketstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for this market:
        DESCRIPTION: **marketStatusCode="S"**
        EXPECTED: Selected market becomes suspended
        EXPECTED: Verified market is shown only 3 seconds and then disappears from 'Game Markets' collection
        """
        pass

    def test_006_chose_other_marker_within_game_markets_collection(self):
        """
        DESCRIPTION: Chose other marker within 'Game Markets' collection
        EXPECTED: 
        """
        pass

    def test_007_trigger_the_following_situation_for_all_outcomes_of_this_marketoutcomestatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for all outcomes of this market:
        DESCRIPTION: **outcomeStatusCode="S"**
        EXPECTED: All its outcomes become suspended
        EXPECTED: Verified market is shown only 3 seconds and then disappears from 'Game Markets' collection
        """
        pass

    def test_008_go_to_all_markets_tab(self):
        """
        DESCRIPTION: Go to 'All Markets' tab
        EXPECTED: 
        """
        pass

    def test_009_find_a_market_that_belongs_to_game_markets_collection(self):
        """
        DESCRIPTION: Find a market that belongs to 'Game Markets' collection
        EXPECTED: 
        """
        pass

    def test_010_trigger_the_following_situation_for_this_marketmarketstatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for this market:
        DESCRIPTION: **marketStatusCode="S"**
        EXPECTED: Selected market becomes suspended
        EXPECTED: Verified market is shown only 3 seconds and then disappears from 'All Markets' collection
        """
        pass

    def test_011_find_the_other_market_that_belongs_to_game_markets_collection(self):
        """
        DESCRIPTION: Find the other market that belongs to 'Game Markets' collection
        EXPECTED: 
        """
        pass

    def test_012_trigger_the_following_situation_for_all_outcomes_of_this_marketoutcomestatuscodes(self):
        """
        DESCRIPTION: Trigger the following situation for all outcomes of this market:
        DESCRIPTION: **outcomeStatusCode="S"**
        EXPECTED: All its outcomes become suspended
        EXPECTED: Verified market is shown only 3 seconds and then disappears from 'All Markets' collection
        """
        pass
