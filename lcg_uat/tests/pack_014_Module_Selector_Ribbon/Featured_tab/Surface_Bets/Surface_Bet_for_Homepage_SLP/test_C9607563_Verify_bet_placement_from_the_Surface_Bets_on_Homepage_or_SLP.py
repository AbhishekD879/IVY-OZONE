import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
# @pytest.mark.prod  # cannot modify cms / create modules on prod
@pytest.mark.medium
@pytest.mark.surface_bets
@pytest.mark.mobile_only
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.featured
@pytest.mark.cms
@pytest.mark.login
@vtest
class Test_C9607563_Verify_bet_placement_from_the_Surface_Bets_on_Homepage_or_SLP(BaseFeaturedTest, BaseBetSlipTest):
    """
    TR_ID: C9607563
    VOL_ID: C9770723
    NAME: Verify bet placement from the Surface Bets on Homepage/SLP
    DESCRIPTION: Test case verifies possibility to place bet from the Surface Bet on Homepage/SLP
    PRECONDITIONS: 1. There are a few Surface Bet added to the SLP/Homepage in the CMS
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
        DESCRIPTION: Log in
        """
        category_id = self.ob_config.football_config.category_id

        cms_surface_bet_football = self.cms_config.get_sport_module(sport_id=category_id,
                                                                    module_type='SURFACE_BET')[0]
        if cms_surface_bet_football['disabled']:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('Surface bets are disabled for Football')
            else:
                self.cms_config.change_sport_module_state(sport_module=cms_surface_bet_football)

        cms_surface_bet_homepage = self.cms_config.get_sport_module(sport_id=0,
                                                                    module_type='SURFACE_BET')[0]
        if cms_surface_bet_homepage['disabled']:
            if tests.settings.cms_env == 'prd0':
                raise CmsClientException('Surface bets are disabled for Football')
            else:
                self.cms_config.change_sport_module_state(sport_module=cms_surface_bet_homepage)

        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.eventID = event['event']['id']
            self._logger.info(f'*** Found Football event with id "{self.eventID}"')
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are not available outcomes')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(selection_ids.values())[0]

        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.selection_ids, self.__class__.team1 = event.selection_ids, event.team1
            self.__class__.selection_id = self.selection_ids[self.team1]
        surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_id,
                                                      categoryIDs=category_id,
                                                      highlightsTabOn=True)
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        self.site.login()

    def test_001_place_the_bet_using_price_button_of_the_surface_bet_from_the_betslip_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Place the bet using Price button of the Surface bet from the Betslip. Verify bet is placed successfully
        EXPECTED: Bet is placed successfully
        """
        self.site.wait_content_state('Home')
        self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))

        result = self.wait_for_surface_bets(name=self.surface_bet_title, delimiter='42/0,', timeout=1, poll_interval=1,
                                            raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.home.get_module_content(module_name=self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
            self.wait_for_surface_bets(name=self.surface_bet_title, delimiter='42/0,', timeout=40, poll_interval=1)

        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        surface_bet.scroll_to()
        surface_bet.bet_button.click()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(surface_bet.bet_button.is_selected(timeout=5),
                        msg='Bet button is not selected after click')
        self.site.open_betslip()
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_002_place_the_bet_using_price_button_of_the_surface_bet_from_the_quickbet_verify_bet_is_placed_successfully(self):
        """
        DESCRIPTION: Place the bet using Price button of the Surface bet from the QuickBet. Verify bet is placed successfully
        EXPECTED: Bet is placed successfully
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('Football')
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
        surface_bet.bet_button.click()

        self.assertTrue(self.site.wait_for_quick_bet_panel(timeout=10), msg='Quick Bet is not shown')
        self.assertTrue(surface_bet.bet_button.is_selected(), msg='Bet button is not selected after click')
        quick_bet_panel = self.site.quick_bet_panel
        quick_bet = quick_bet_panel.selection.content
        amount_form = quick_bet.amount_form
        self.assertTrue(amount_form.input.is_active(timeout=5), msg='Amount input field is not active')
        amount_form.input.value = self.bet_amount
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
