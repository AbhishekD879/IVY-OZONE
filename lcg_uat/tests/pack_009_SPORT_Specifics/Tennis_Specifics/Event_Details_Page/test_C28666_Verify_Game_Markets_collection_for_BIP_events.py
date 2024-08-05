import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.sports
@pytest.mark.tennis
@pytest.mark.markets
@pytest.mark.event_details
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.issue('https://jira.egalacoral.com/browse/VOL-6105')  # Coral only
@vtest
class Test_C28666_Verify_Game_Markets_collection_for_BIP_events(BaseSportTest):
    """
    TR_ID: C28666
    NAME: Verify 'Game Markets' collection for BIP events
    DESCRIPTION: This test case verifies 'Game Markets' collection for BIP events
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-5349 (Tennis Game Markets - Hide when all outcomes are suspended)
    PRECONDITIONS: Make sure that there is 'Game Markets' collection on Event Detail Page and there are the markets available
    PRECONDITIONS: To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: *   Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: *   XXXXXXX - event id
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Note: need to create a market with market template |Current Game Winner|
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Tennis Live Event
        """
        event_params = self.ob_config.add_tennis_event_to_autotest_trophy(
            markets=[('current_game_1st_point', {'cashout': True}),
                     ('set_1_game_1_deuce', {'cashout': True})],
            is_live=True)
        self.__class__.eventID = event_params.event_id

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to Event Details Page
        EXPECTED: Event Details Page is opened
        EXPECTED: 'Main Markets' (for Coral) / 'All Markets' (for Ladbrokes) collection is opened by default
        """
        self.navigate_to_edp(event_id=self.eventID)
        markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(markets_tabs_list, msg=f'No markets tabs found')
        default_tab = markets_tabs_list.current
        expected_tab = self.get_default_tab_name_on_sports_edp(event_id=self.eventID)
        self.assertEqual(default_tab, expected_tab,
                         msg=f'\nDefault tab: "{default_tab}" '
                             f'is not as expected: "{expected_tab}"')

    def test_003_go_to_game_markets_collection(self):
        """
        DESCRIPTION: Go to 'Game Markets' (for Coral) / 'Game' (for Ladbrokes) collection
        EXPECTED: The list of markets that belongs to 'Game Markets' (for Coral) / 'Game' (for Ladbrokes) collection is shown
        EXPECTED: Make sure that there are no markets with all suspended outcomes
        """
        self.__class__.game_markets_tab = vec.siteserve.EXPECTED_MARKET_TABS.game
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=self.game_markets_tab)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, self.game_markets_tab,
                         msg=f'\nCurrent tab: "{current_tab}" '
                             f'is not as expected: "{self.game_markets_tab}')

    def test_004_choose_market_within_game_markets_collection(self):
        """
        DESCRIPTION: Choose market within 'Game Markets' (for Coral) / 'Game' (for Ladbrokes) collection
        """
        self.__class__.first_market_id = self.ob_config.market_ids[self.eventID]['current_game_1st_point']

    def test_005_suspend_this_market(self):
        """
        DESCRIPTION: Trigger the following situation for this market:
        DESCRIPTION: **marketStatusCode="S"**
        EXPECTED: Selected market becomes suspended
        EXPECTED: Verified market is shown only 3 seconds and then disappears from 'Game Markets' (for Coral) / 'Game' (for Ladbrokes) collection
        """
        self.ob_config.change_market_state(
            event_id=self.eventID, market_id=self.first_market_id, displayed=True, active=False)
        result = wait_for_result(lambda: vec.siteserve.EXPECTED_MARKET_TABS.current_game_1st_point not in self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.keys(),
                                 name=f'"{vec.siteserve.EXPECTED_MARKET_TABS.current_game_1st_point}" market to dissappear',
                                 timeout=15)
        self.assertTrue(result,
                        msg=f'"{vec.siteserve.EXPECTED_MARKET_TABS.current_game_1st_point}" should not be displayed')
        # activate market for 'all markets' tab verification
        self.ob_config.change_market_state(
            event_id=self.eventID, market_id=self.first_market_id, displayed=True, active=True)

    def test_006_choose_other_market_within_game_markets_collection(self):
        """
        DESCRIPTION: Choose other market within 'Game Markets' (for Coral) / 'Game' (for Ladbrokes) collection
        """
        self.__class__.second_market_id = self.ob_config.market_ids[self.eventID]['set_1_game_1_deuce']

    def test_007_suspend_this_market(self):
        """
        DESCRIPTION: Trigger the following situation for all outcomes of this market:
        DESCRIPTION: **outcomeStatusCode="S"**
        EXPECTED: All its outcomes become suspended
        EXPECTED: Verified market is shown only 3 seconds and then disappears from 'Game Markets' (for Coral) / 'Game' (for Ladbrokes) collection
        """
        self.ob_config.change_market_state(
            event_id=self.eventID, market_id=self.second_market_id, displayed=True, active=False)
        result = wait_for_result(lambda: vec.siteserve.EXPECTED_MARKET_TABS.set_1_game_1_deuce not in self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict.keys(),
                                 name=f'"{vec.siteserve.EXPECTED_MARKET_TABS.current_game_1st_point}" market to dissappear',
                                 timeout=15)
        self.assertTrue(result,
                        msg=f'"{vec.siteserve.EXPECTED_MARKET_TABS.set_1_game_1_deuce}" should not be displayed')
        # activate market for 'all markets' tab verification
        self.ob_config.change_market_state(
            event_id=self.eventID, market_id=self.second_market_id, displayed=True, active=True)

    def test_008_go_to_all_markets_tab(self):
        """
        DESCRIPTION: Go to 'All Markets' tab
        """
        # make activated markets to appear
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.sport_event_details.markets_tabs_list.open_tab(tab_name=vec.siteserve.EXPECTED_MARKET_TABS.all_markets)
        current_tab = self.site.sport_event_details.markets_tabs_list.current
        self.assertEqual(current_tab, vec.siteserve.EXPECTED_MARKET_TABS.all_markets,
                         msg=f'\nCurrent tab: "{current_tab}" '
                             f'is not as expected: "{vec.siteserve.EXPECTED_MARKET_TABS.all_markets}')

    def test_009_find_a_market_that_belongs_to_game_markets_collection(self):
        """
        DESCRIPTION: Find a market that belongs to 'Game Markets' (for Coral) / 'Game' (for Ladbrokes) collection
        """
        # we use market from step 6

    def test_010_suspend_this_market(self):
        """
        DESCRIPTION: Trigger the following situation for this market:
        DESCRIPTION: **marketStatusCode="S"**
        EXPECTED: Selected market becomes suspended
        EXPECTED: Verified market is shown only 3 seconds and then disappears from 'All Markets' collection
        """
        self.test_005_suspend_this_market()

    def test_011_find_the_other_market_that_belongs_to_game_markets_collection(self):
        """
        DESCRIPTION: Find the other market that belongs to 'Game Markets' (for Coral) / 'Game' (for Ladbrokes) collection
        """
        # we use market from step 8

    def test_012_suspend_this_market(self):
        """
        DESCRIPTION: Trigger the following situation for all outcomes of this market:
        DESCRIPTION: **outcomeStatusCode="S"**
        EXPECTED: All its outcomes become suspended
        EXPECTED: Verified market is shown only 3 seconds and then disappears from 'All Markets' collection
        """
        self.test_007_suspend_this_market()
