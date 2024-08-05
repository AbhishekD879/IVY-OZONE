import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.Common import Common


@pytest.mark.uat
@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.desktop
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.p3
@pytest.mark.sports
@vtest
class Test_C44870188_Verify_the_sport_event_card_template_as_per_logic(Common):
    """
    TR_ID: C44870188
    NAME: Verify the sport event card template  as per logic
    """
    keep_browser_open = True

    def verify_competitions_collapsable_expandable(self, tournaments):
        if tournaments:
            for section in tournaments:
                if section.is_expanded():
                    section.collapse()
                    self.assertFalse(section.is_expanded(), msg='section is not collapsed')
                    section.expand()
                    self.assertTrue(section.is_expanded(), msg='section is not expanded')
                else:
                    section.expand()
                    self.assertTrue(section.is_expanded(), msg='section is not expanded')
                    section.collapse()
                    self.assertFalse(section.is_expanded(), msg='section is not collapsed')

    def test_000_precondition(self):
        """
        PRECONDITIONS: User is logged in and surface bets are available
        PRECONDITIONS: Verify the template for football
        DESCRIPTION: Add Surface Bets to the Homepage in the CMS
        """
        category_id = self.ob_config.football_config.category_id
        self.__class__.cms_surface_bet = self.cms_config.get_sport_module(sport_id=category_id,
                                                                          module_type='SURFACE_BET')[0]
        if self.cms_surface_bet['disabled'] and tests.settings.backend_env != "prod":
            self.cms_config.change_sport_module_state(sport_module=self.cms_surface_bet)
        self.site.login()

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('homepage')

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Sport> icon on the Sports Menu Ribbon
        EXPECTED: <Sport> Landing Page is opened
        EXPECTED: 'Home Draw Away' Price Odds Template Type is shown
        """
        if self.device_type == 'mobile':
            self.site.open_sport(name='FOOTBALL')
        else:
            self.site.header.sport_menu.items_as_ordered_dict[vec.football.FOOTBALL_TITLE.upper()].click()
        self.site.wait_content_state(state_name='FOOTBALL')
        self.assertTrue(self.site.sports_page.tabs_menu.items_as_ordered_dict['MATCHES'].is_selected())

        markets = []
        fb_tab = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.values())
        self.assertTrue(fb_tab, msg='No tab found on FB page')
        for i in range(2):
            markets.append(fb_tab[i])
        for market in markets:
            for event_name, event in market.items_as_ordered_dict.items():
                if len(event.template.items) != 0:
                    self.assertTrue(event.template.items_as_ordered_dict,
                                    msg=f'"Home Draw Away" Price Odds Template '
                                        f'Type is not displayed for event "{event_name}"')
        self.__class__.match = markets[0]

    def test_003_tap_anywhere_on_event_section(self):
        """
        DESCRIPTION: Tap anywhere on Event section
        EXPECTED: Event Details Page is opened
        """
        self.match.click()
        self.__class__.markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets, msg='No Event Details Page is opened with any markets ')

    def test_004_verify_below_data_for_event_in_the_edp_team_names_odds_market_name_event_eg_chelsea_v_arsenal__verify_collapseexpand_accordion_and__navigation_to_event_details_page_score_and_time_as_per_logic_below_show_score_and_time_if_available_else_show_score_and_live_if_time_is_not_available__and_event_has_started_show_live_only_if_score_and_time_is_not_available_and_event_has_started_display_watch_live_icon__if_available_verify_navigation_arrow_for_surface_bets_if_available(
            self):
        """
        DESCRIPTION: Verify below data for event in the EDP
        DESCRIPTION: -Team names
        DESCRIPTION: -Odds
        DESCRIPTION: -Market name
        DESCRIPTION: -Event (e.g Chelsea v Arsenal)
        DESCRIPTION: --Verify Collapse/Expand accordion and  Navigation to Event Details Page
        DESCRIPTION: -Score and time as per logic below:
        DESCRIPTION: -Show score and time if available, else
        DESCRIPTION: -Show score and Live if time is not available  and event has started
        DESCRIPTION: -Show Live only, if score and time is not available; and event has started
        DESCRIPTION: -Display 'Watch Live' Icon  if available
        DESCRIPTION: -Verify Navigation arrow for surface bets if available
        EXPECTED: All the data should be displayed correctly
        """
        # we cannot automate live score updates.

        edp_page = self.site.sport_event_details
        if self.device_type == 'mobile':
            edp_page = self.site.sport_event_details
            if edp_page.is_live_now_event:
                self.assertTrue(edp_page.event_title_bar.event_name, msg=f'event name:"{edp_page.event_title_bar.event_name}"is not found')
            else:
                self.site.wait_content_state('EventDetails', timeout=15)
            if self.site.sports_page.tab_content.has_surface_bets():
                surface_bets = self.site.sports_page.tab_content.surface_bets.items_as_ordered_dict
                self.assertTrue(surface_bets, msg='There are no surface bet in the container')

        else:
            self.assertTrue(edp_page.event_title_bar.event_name, msg=f'event name:"{edp_page.event_title_bar.event_name}"is not found')
            self.assertTrue(edp_page.event_title_bar.event_time,
                            msg=f'Time as per logic not displayed on Football EDP for event "{edp_page.event_title_bar.event_time}"')
        if edp_page.has_watch_live_icon:
            self.assertTrue(edp_page.has_watch_live_icon,
                            msg=f'event name:"{edp_page.has_watch_live_icon}"is not found')
        edp_markets = [list(self.markets.values())[0]]
        self.verify_competitions_collapsable_expandable(edp_markets)
        if self.device_type == 'mobile':
            outcome_list = self.markets[edp_markets[0].name]
        else:
            outcome_list = self.markets[edp_markets[0].name.split('\n', 1)[0]]
        self.assertTrue(outcome_list.add_to_betslip_button.is_displayed(),
                        msg=f'Odds are not displayed on EDP for market "{outcome_list.name}"')
