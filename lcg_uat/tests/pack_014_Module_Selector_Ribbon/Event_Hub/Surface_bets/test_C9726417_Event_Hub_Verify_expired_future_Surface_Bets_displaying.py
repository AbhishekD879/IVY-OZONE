import pytest
from time import sleep
from faker import Faker
from collections import OrderedDict
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # test case only applicable for QA2 as we need configure event hub sports module in CMS
@pytest.mark.high
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C9726417_Event_Hub_Verify_expired_future_Surface_Bets_displaying(Common):
    """
    TR_ID: C9726417
    NAME: Event Hub: Verify expired/future Surface Bets displaying
    DESCRIPTION: Test case verifies that expired/future Surface Bet isn't shown on Event Hub tab
    PRECONDITIONS: 1. There are a Surface Bet added to the Event Hub in the CMS
    PRECONDITIONS: 2. Open this Event Hub tab in the application
    PRECONDITIONS: CMS path for the Event Hub: Sport Pages > Event Hub > Edit event hub > Surface Bets Module
    """
    keep_browser_open = True
    tabs_bma = OrderedDict()
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def create_surface_bet(self):
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids, self.__class__.team1 = event.selection_ids, event.team1
        self.__class__.eventID = event.event_id
        self.__class__.price_button_text = self.ob_config.event.prices['odds_home']
        self.__class__.surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_ids[self.team1],
                                                                     content=self.content,
                                                                     priceNum=self.price_num,
                                                                     priceDen=self.price_den,
                                                                     eventIDs=self.eventID,
                                                                     edpOn=True,
                                                                     categoryIDs=[0, 16],
                                                                     event_hub_id=self.event_hub_index[0])
        self.__class__.surface_bet_id = self.surface_bet.get('id')
        self.__class__.surface_bet_title = self.surface_bet.get('title').upper()

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1. There is a  Surface Bet added to the Event Hub in the CMS
        DESCRIPTION: 2. Open this Event Hub tab in the application
        """
        self.site.wait_content_state('Home')
        self.site.login()
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        self.__class__.tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                                   tab['visible'] is True and
                                   tab['directiveName'] == 'EventHub' and
                                   (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                                       time_format="%Y-%m-%dT%H:%M:%S", hours=-1))]
        self.__class__.selected_tab = self.tabs_cms[0]
        self.__class__.event_hub_index = [tab['hubIndex'] for tab in module_ribbon_tabs if
                                          tab['title'].upper() == self.selected_tab]
        self.__class__.tabs_bma = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        surface_bet_modules_cms = None
        for tab_name, tab in self.tabs_bma.items():
            if tab_name == self.selected_tab:
                tab.click()
                break
        self.__class__.sports_module_event_hub = self.cms_config.get_sport_modules_for_event_hub(
            self.event_hub_index[0])
        for module in self.sports_module_event_hub:
            if module['moduleType'] == 'SURFACE_BET':
                surface_bet_modules_cms = module
                break
        if surface_bet_modules_cms is None:
            self.cms_config.add_sport_module_to_event_hub(module_type='SURFACE_BET')
        else:
            surface_bet_module_status = [module['disabled'] for module in self.sports_module_event_hub
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
        event_name, self.__class__.sb_event = list(surface_bets.items())[0]
        self.assertTrue(self.sb_event.is_displayed(), msg=f'surface bet "{event_name}" is not displayed')

    def test_001_in_the_cms_edit_the_surface_bet_set_display_fromto_to_the_past(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the past.
        """
        past_date_from = self.get_date_time_formatted_string(time_format=self.time_format, days=-2)[:-3] + 'Z'
        past_date_to = self.get_date_time_formatted_string(time_format=self.time_format, days=-1)[:-3] + 'Z'
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=past_date_from,
                                           displayTo=past_date_to)

    def test_002_in_the_application_refresh_the_eventh_hub_page_to_verify_this_surface_bet_isnt_displayed(self):
        """
        DESCRIPTION: In the application refresh the Eventh Hub page to verify this Surface bet isn't displayed
        EXPECTED: Surface Bet isn't displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sleep(2)
        result = wait_for_result(lambda: f'/{self.event_hub_index[0]}' in self.device.get_current_url(),
                                 name=f'Waiting for Event hub with index "{self.event_hub_index[0]}"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Did not navigate to Event hub with index "{self.event_hub_index[0]}"')
        surface_bet_presence = self.site.home.tab_content.has_surface_bets()
        if surface_bet_presence:
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            surface_bet = surface_bets.get(self.surface_bet_title)
            self.assertFalse(surface_bet,
                             msg=f'"{self.surface_bet_title}" is found in "{list(surface_bets.keys())}"')

    def test_003_in_the_cms_edit_the_surface_bet_set_display_fromto_to_the_future(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the future.
        """
        future_date_from = self.get_date_time_formatted_string(time_format=self.time_format, days=2)[:-3] + 'Z'
        future_date_to = self.get_date_time_formatted_string(time_format=self.time_format, days=3)[:-3] + 'Z'
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=future_date_from,
                                           displayTo=future_date_to)

    def test_004_in_the_application_refresh_the_event_hub_page_to_verify_this_surface_bet_isnt_displayed(self):
        """
        DESCRIPTION: In the application refresh the Event hub page to verify this Surface bet isn't displayed
        EXPECTED: Surface Bet isn't displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        sleep(2)
        surface_bet_presence = self.site.home.tab_content.has_surface_bets()
        if surface_bet_presence:
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            surface_bet = surface_bets.get(self.surface_bet_title)
            self.assertFalse(surface_bet,
                             msg=f'"{self.surface_bet_title}" is found in "{list(surface_bets.keys())}"')
