import pytest
import tests
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.p2
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C44870186_Verify_Navigation_arrows_In_Play_widget_and_Surface_Bets_on_Football_Sports_Landing_Page(BaseBetSlipTest):
    """
    TR_ID: C44870186
    NAME: "Verify Navigation arrows, In-Play widget and Surface Bets on Football Sports Landing Page.
    DESCRIPTION: "Verify Navigation arrows, In-Play widget and Surface Bets on Football Sports Landing Page.
    """
    keep_browser_open = True
    bet_amount = 0.05

    def test_000_precondition(self):
        """
        PRECONDITIONS: BETA app is loaded and User is on Home page
        PRECONDITIONS: Surface bets are configured on Football Sports Landing Page
        DESCRIPTION: Add Surface Bets to the Homepage in the CMS
        """
        category_id = self.ob_config.football_config.category_id
        cms_surface_bet = self.cms_config.get_sport_module(sport_id=category_id, module_type='SURFACE_BET')[0]
        self.assertTrue(cms_surface_bet, msg='Surface bets are not available ')
        if cms_surface_bet['disabled'] and tests.settings.backend_env != "prod":
            self.cms_config.change_sport_module_state(sport_module=self.cms_surface_bet)
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_001_from_home_page_tap_on_footballfrom_header_menu_or_from_all_sports_menu(self):
        """
        DESCRIPTION: From home page tap on Football
        DESCRIPTION: (From header Menu or from All sports menu)
        EXPECTED: User lands on Football sports landing page
        """
        if self.device_type in ['mobile', 'tablet']:
            if self.brand == 'ladbrokes':
                self.site.home.menu_carousel.click_item(vec.inplay.IN_PLAY_FOOTBALL, timeout=5)
            else:
                self.site.home.menu_carousel.click_item(vec.inplay.IN_PLAY_FOOTBALL)
        else:
            self.site.header.sport_menu.items_as_ordered_dict['FOOTBALL'].click()
        self.site.wait_content_state('FOOTBALL')

    def test_002_mobile__tablet_only__verify_surface_bets_on_football_landing_page(self):
        """
        DESCRIPTION: Mobile & Tablet only : Verify Surface bets on Football Landing Page
        EXPECTED: User should see Surface bets.
        EXPECTED: User should be able to scroll across the surface bet if more than one are available.
        EXPECTED: User should be able to add and place bets from SurfaceBets.
        """
        if self.device_type in ['mobile', 'tablet']:
            surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
            self.assertTrue(surface_bets, msg='No Surface Bets found')
            event_name, event = list(surface_bets.items())[-1]
            self.assertTrue(event.is_displayed(), msg=f'surface bet {event_name} is not displayed')
            event.bet_button.click()
            quick_bet = self.site.quick_bet_panel.selection
            quick_bet.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()
            self.assertTrue(self.site.quick_bet_panel.wait_for_bet_receipt_displayed(timeout=10),
                            msg='Bet Receipt is not shown')
            self.site.quick_bet_panel.header.close_button.click()

    def test_003_desktop_only__verify_in_play_widget_on_foot_ball_landing_page(self):
        """
        DESCRIPTION: Desktop only : Verify In-Play Widget on Foot ball Landing Page
        EXPECTED: On Football Landing Page, User should see In-Play widget.
        EXPECTED: User should be able to scroll across the events if more than one event available.
        EXPECTED: User should navigate to the respective event when tapped on any In-Play event
        """
        if self.device_type == 'desktop':
            self.device.refresh_page()
            sections = self.site.football.in_play_widget.items_as_ordered_dict.get('In-Play LIVE Football')
            widgets = sections.content.items_as_ordered_dict
            self.assertTrue(widgets, msg='Widget are not available')
            event_name, event = list(widgets.items())[-1]
            self.assertTrue(event.is_displayed(), msg=f'Widget {event_name} is not displayed')
            event.click()
            if self.brand == 'ladbrokes':
                page_title = self.site.football.header_line.page_title.title
            else:
                page_title = list(self.site.football.breadcrumbs.items_as_ordered_dict.keys())[-1]
            self.assertIn(event_name.upper(), page_title.upper(),
                          msg=f'widget{event_name} is not navigated to {page_title}')
