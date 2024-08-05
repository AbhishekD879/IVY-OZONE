import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


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
class Test_C9607553_Verify_undisplayed_Surface_Bets_displaying(BaseFeaturedTest):
    """
    TR_ID: C9607553
    NAME: Verify "undisplayed" Surface Bets displaying
    DESCRIPTION: Test case verifies that undisplayed Surface Bet isn't shown
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the SLP/Homepage in the CMS
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

    def test_001_in_the_ti_mark_the_selection_from_the_surface_bet_as_not_displayed(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as not displayed
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True)

    def test_002_in_the_application_refresh_the_category_pagehomepage(self):
        """
        DESCRIPTION: In the application refresh the category page/homepage
        EXPECTED: Surface Bet with the undisplayed selection isn't shown
        """
        self.assertFalse(self.surface_bet.bet_button.is_enabled(expected_result=False, timeout=30),
                         msg=f'Bet button is not disabled for "{self.surface_bet_title}"')

    def test_003_in_the_ti_mark_the_selection_from_the_surface_bet_as_displayed(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as displayed
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=True)

    def test_004_in_the_application_refresh_the_category_pagehomepage(self):
        """
        DESCRIPTION: In the application refresh the category page/homepage
        EXPECTED: Surface Bet is shown
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        self.surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(self.surface_bets, msg='No Surface Bets found')
        self.surface_bet = self.surface_bets.get(self.surface_bet_title)
        self.surface_bet.scroll_to()
        self.assertTrue(self.surface_bet.bet_button.is_enabled(timeout=30),
                        msg=f'Bet button is not enabled for "{self.surface_bet_title}"')

    def test_005_pass_1_4_steps_with_undisplaying_on_market_and_event_levels(self):
        """
        DESCRIPTION: Pass 1-4 steps with undisplaying on market and event levels
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)
        self.surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.surface_bet = self.surface_bets.get(self.surface_bet_title)
        self.assertFalse(self.surface_bet.bet_button.is_enabled(expected_result=False, timeout=30),
                         msg=f'Bet button is not disabled for "{self.surface_bet_title}"')

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.test_004_in_the_application_refresh_the_category_pagehomepage()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True)
        self.test_002_in_the_application_refresh_the_category_pagehomepage()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        self.test_004_in_the_application_refresh_the_category_pagehomepage()
