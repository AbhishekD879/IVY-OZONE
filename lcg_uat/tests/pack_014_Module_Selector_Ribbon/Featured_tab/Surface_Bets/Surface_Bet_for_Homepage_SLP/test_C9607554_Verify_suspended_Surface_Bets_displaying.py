import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl  # cannot perform liveserv updated on hl/prod
# @pytest.mark.prod
@pytest.mark.medium
@pytest.mark.surface_bets
@pytest.mark.mobile_only
@pytest.mark.liveserv_updates
@pytest.mark.featured
@pytest.mark.cms
@vtest
class Test_C9607554_Verify_suspended_Surface_Bets_displaying(BaseFeaturedTest):
    """
    TR_ID: C9607554
    VOL_ID: C9771302
    NAME: Verify "suspended" Surface Bets displaying
    DESCRIPTION: Test case verifies that suspended Surface Bet is marked as disabled
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the category/homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True
    surface_bet_title = ''

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Surface Bet to the SLP/Homepage in the CMS
        DESCRIPTION: Open this SLP/Homepage page in the application
        """
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=self.ob_config.backend.ti.football.category_id,
                                                           module_type='SURFACE_BET')[0]
        if cms_surface_bet['disabled']:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('Surface bets are disabled for Football')
            else:
                self.cms_config.change_sport_module_state(sport_module=cms_surface_bet)

        event = self.ob_config.add_autotest_premier_league_football_event()
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.eventID, self.__class__.marketID = event.event_id, self.ob_config.market_ids[event.event_id][market_short_name]
        self.__class__.selection_ids, self.__class__.team1 = event.selection_ids, event.team1
        self.__class__.selection_id = self.selection_ids[self.team1]

        surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_id,
                                                      categoryIDs=self.ob_config.football_config.category_id)

        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        result = self.wait_for_surface_bets(name=self.surface_bet_title, timeout=1, poll_interval=1, raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.wait_for_surface_bets(name=self.surface_bet_title, timeout=15, poll_interval=1)

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        self.__class__.surface_bet = surface_bet

    def test_001_in_the_ti_mark_the_selection_from_the_surface_bet_as_suspended(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as suspended
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True)

    def test_002_in_the_application_verify_the_price_button_is_marked_as_suspended_without_page_refreshing(self):
        """
        DESCRIPTION: In the application verify the Price button is marked as suspended without page refreshing
        EXPECTED: Price button becomes suspended (disabled)
        """
        self.assertFalse(self.surface_bet.bet_button.is_enabled(expected_result=False, timeout=30),
                         msg=f'Bet button is not disabled for "{self.surface_bet_title}"')

    def test_003_in_the_ti_mark_the_selection_from_the_surface_bet_as_not_suspended(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as not suspended
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=True)

    def test_004_in_the_application_verify_the_price_button_is_marked_as_enabled_without_page_refreshing(self):
        """
        DESCRIPTION: in the application verify the Price button is marked as enabled without page refreshing
        EXPECTED: Price button becomes not suspended (enabled)
        """
        self.surface_bet.scroll_to()
        self.assertTrue(self.surface_bet.bet_button.is_enabled(timeout=30),
                        msg=f'Bet button is not enabled for "{self.surface_bet_title}"')

    def test_005_pass_1_4_steps_with_suspending_on_market_and_event_levels(self):
        """
        DESCRIPTION: Pass 1-4 steps with suspending on market and event levels
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)
        self.test_002_in_the_application_verify_the_price_button_is_marked_as_suspended_without_page_refreshing()

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.test_004_in_the_application_verify_the_price_button_is_marked_as_enabled_without_page_refreshing()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True)
        self.test_002_in_the_application_verify_the_price_button_is_marked_as_suspended_without_page_refreshing()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.test_004_in_the_application_verify_the_price_button_is_marked_as_enabled_without_page_refreshing()
