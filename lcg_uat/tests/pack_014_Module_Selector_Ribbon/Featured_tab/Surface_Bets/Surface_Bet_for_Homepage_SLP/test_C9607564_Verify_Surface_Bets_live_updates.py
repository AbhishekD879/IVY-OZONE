import pytest

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl  # cannot perform liveserv updated on hl/prod
@pytest.mark.medium
@pytest.mark.surface_bets
@pytest.mark.mobile_only
@pytest.mark.liveserv_updates
@pytest.mark.featured
@pytest.mark.cms
@vtest
class Test_C9607564_Verify_Surface_Bets_live_updates(BaseFeaturedTest):
    """
    TR_ID: C9607564
    VOL_ID: C9776078
    NAME: Verify Surface Bets live updates
    DESCRIPTION: Test case verifies price live updates of the Surface Bet
    PRECONDITIONS: 1. There is a are Surface Bet added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True
    increased_price = '99/2'
    decreased_price = '13/98'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add Surface Bet to the SLP/Homepage in the CMS
        DESCRIPTION: Open this SLP page in the application
        """
        category_id = self.ob_config.football_config.category_id

        cms_surface_bet_football = self.cms_config.get_sport_module(sport_id=category_id,
                                                                    module_type='SURFACE_BET')[0]
        if cms_surface_bet_football['disabled']:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('Surface bets are disabled for Football')
            else:
                self.cms_config.change_sport_module_state(sport_module=cms_surface_bet_football)

        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids, self.__class__.team1 = event.selection_ids, event.team1
        self.__class__.eventID = event.event_id
        surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_ids[self.team1],
                                                      categoryIDs=category_id)

        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        result = self.wait_for_surface_bets(name=self.surface_bet_title, delimiter='42/16,', timeout=1, poll_interval=1,
                                            raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.wait_for_surface_bets(name=self.surface_bet_title, delimiter='42/16,', timeout=15, poll_interval=1)

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        surface_bet.scroll_to()
        self.__class__.surface_bet = surface_bet

    def test_001_in_ti_increase_the_price_for_the_selection_of_some_surface_bet(self):
        """
        DESCRIPTION: In TI increase the price for the selection of some Surface Bet
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.increased_price)

    def test_002_in_the_application_verify_the_price_within_the_price_button_gets_changed_in_live_without_page_refresh(self):
        """
        DESCRIPTION: In the application verify the price within the Price button gets changed in live, without page refresh
        EXPECTED: Corresponding Price button on the Surface Bet card displays new price
        EXPECTED: Price button becomes red for a second
        """
        self.assertTrue(self.surface_bet.bet_button.is_price_changed(expected_price=self.increased_price, timeout=30),
                        msg=f'Price for {self.surface_bet_title} was not changed to "{self.increased_price}"')

    def test_003_in_ti_decrease_the_price_for_the_selection_of_some_surface_bet(self):
        """
        DESCRIPTION: In TI decrease the price for the selection of some Surface Bet
        """
        self.ob_config.change_price(selection_id=self.selection_ids[self.team1], price=self.decreased_price)

    def test_004_in_the_application_verify_the_price_within_the_price_button_gets_changed_in_live_without_page_refresh(self):
        """
        DESCRIPTION: in the application verify the price within the Price button gets changed in live, without page refresh
        EXPECTED: Corresponding Price button on the Surface Bet card displays new price
        EXPECTED: Price button becomes blue for a second
        """
        self.assertTrue(self.surface_bet.bet_button.is_price_changed(expected_price=self.decreased_price, timeout=40),
                        msg=f'Price for {self.surface_bet_title} was not changed to "{self.decreased_price}"')
