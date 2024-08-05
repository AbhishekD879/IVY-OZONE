import pytest
from faker import Faker
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from crlat_cms_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # In prod/beta we Can not configure event hub sports module in CMS
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C9726415_Event_Hub_Verify_undisplayed_Surface_Bets_displaying(Common):
    """
    TR_ID: C9726415
    NAME: Event Hub: Verify "undisplayed" Surface Bets displaying
    DESCRIPTION: Test case verifies that undisplayed Surface Bet isn't shown on Event Hub
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event hub in the CMS
    PRECONDITIONS: 2. Open this Event Hub tab in the application
    PRECONDITIONS: CMS path for the Event Hub: Sport Pages > Event hub > Edit Event hub > Surface Bets Module
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def create_surface_bet(self):
        event = self.ob_config.add_autotest_premier_league_football_event()
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        self.__class__.eventID, self.__class__.marketID = event.event_id, self.ob_config.market_ids[event.event_id][
            market_short_name]
        self.__class__.selection_ids, self.__class__.team1 = event.selection_ids, event.team1
        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_ids[self.team1],
                                                                     content=self.content,
                                                                     priceNum=self.price_num,
                                                                     priceDen=self.price_den,
                                                                     eventIDs=self.eventID,
                                                                     edpOn=True,
                                                                     categoryIDs=[0, 16],
                                                                     event_hub_id=self.event_hub_index[0])
        self.__class__.surface_bet_title = self.surface_bet.get('title').upper()

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. There is a  Surface Bet added to the Event Hub in the CMS
        DESCRIPTION: 2. Open this Event Hub tab in the application
        """
        self.site.wait_content_state('Home', timeout=20)
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                    tab['visible'] is True and
                    tab['directiveName'] == 'EventHub' and
                    (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                        time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]
        selected_tab = tabs_cms[0]
        self.__class__.event_hub_index = [tab['hubIndex'] for tab in module_ribbon_tabs if
                                          tab['title'].upper() == selected_tab]
        tabs_bma = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        surface_bet_modules_cms = None
        for tab_name, tab in tabs_bma.items():
            if tab_name == selected_tab:
                tab.click()
                break
        sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(
            self.event_hub_index[0])
        for module in sports_module_event_hub:
            if module['moduleType'] == 'SURFACE_BET':
                surface_bet_modules_cms = module
                break
        if surface_bet_modules_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET')
        else:
            surface_bet_module_status = [module['disabled'] for module in sports_module_event_hub
                                         if module['moduleType'] == 'SURFACE_BET']
            if surface_bet_module_status is True:
                self.cms_config.change_sport_module_state(sport_module=surface_bet_modules_cms)
        self.create_surface_bet()
        result = wait_for_result(lambda: f'/{self.event_hub_index[0]}' in self.device.get_current_url(),
                                 name=f'Waiting for Event hub with index "{self.event_hub_index[0]}"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Did not navigate to Event hub with index "{self.event_hub_index[0]}"')
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        event_name, sb_event = list(surface_bets.items())[0]
        self.assertTrue(sb_event.is_displayed(), msg=f'surface bet "{event_name}" is not displayed')

    def test_001_in_the_ti_mark_the_selection_from_the_surface_bet_as_not_displayed(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as not displayed
        EXPECTED:
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True)

    def test_002_in_the_application_verify_surface_bet_gets_undisplayed_from_the_event_hub_page_by_live_update(self):
        """
        DESCRIPTION: In the application verify Surface Bet gets undisplayed from the Event Hub page by live update
        EXPECTED: Surface Bet with the undisplayed selection isn't shown
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sleep(3)
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(
            self.surface_bet['title'].upper())
        self.assertFalse(surface_bets.bet_button.is_enabled(expected_result=False, timeout=30),
                         msg=f'Bet button is not disabled for "{self.surface_bet_title}"')

    def test_003_in_the_ti_mark_the_selection_from_the_surface_bet_as_displayed(self):
        """
        DESCRIPTION: In the TI mark the selection from the Surface Bet as displayed
        EXPECTED:
        """
        self.ob_config.change_selection_state(selection_id=self.selection_ids[self.team1], displayed=True, active=True)

    def test_004_in_the_application_verify_surface_bet_gets_displayed_on_the_event_hub_page_by_live_update(self):
        """
        DESCRIPTION: In the application verify Surface Bet gets displayed on the Event Hub page by live update
        EXPECTED: Surface Bet is shown
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sleep(5)
        surface_bet = self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(
            self.surface_bet['title'].upper())
        surface_bet.scroll_to()
        self.assertTrue(surface_bet.bet_button.is_enabled(timeout=40),
                        msg=f'Bet button is not enabled for "{self.surface_bet_title}"')

    def test_005_pass_1_4_steps_with_undisplaying_on_market_and_event_levels(self):
        """
        DESCRIPTION: Pass 1-4 steps with undisplaying on market and event levels
        EXPECTED:
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True)
        surface_bet = self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(
            self.surface_bet['title'].upper())
        sleep(5)
        self.assertFalse(surface_bet.bet_button.is_enabled(expected_result=False, timeout=30),
                         msg=f'Bet button is not disabled for "{self.surface_bet_title}"')

        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)
        self.test_004_in_the_application_verify_surface_bet_gets_displayed_on_the_event_hub_page_by_live_update()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True)
        self.test_002_in_the_application_verify_surface_bet_gets_undisplayed_from_the_event_hub_page_by_live_update()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True)
        self.test_003_in_the_ti_mark_the_selection_from_the_surface_bet_as_displayed()

        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)
        sleep(2)
        self.test_004_in_the_application_verify_surface_bet_gets_displayed_on_the_event_hub_page_by_live_update()
