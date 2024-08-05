import pytest
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.utils.waiters import wait_for_result
from crlat_cms_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # In prod/beta, we Can not configure event hub sports module in CMS
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726413_Event_Hub_Verify_disabled_Surface_Bets_displaying(Common):
    """
    TR_ID: C9726413
    NAME: Event Hub: Verify disabled Surface Bets displaying
    DESCRIPTION: Test cases verifies that disabled Surface Bets are not shown
    PRECONDITIONS: 1. There are a few valid Surface Bets added to the Event Hub in the CMS
    PRECONDITIONS: 2. Open this Event hub page in the application
    """
    keep_browser_open = True
    fake = Faker()
    content = fake.paragraph()
    price_num = fake.random_int(min=1, max=10)
    price_den = fake.random_int(min=20, max=50)

    def create_surface_bets(self):
        event = self.ob_config.add_autotest_premier_league_football_event()
        selection_ids, team1, team2 = event.selection_ids, event.team1, event.team2
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_ids[team1],
                                                      content=self.content,
                                                      priceNum=self.price_num,
                                                      priceDen=self.price_den,
                                                      eventIDs=self.eventID,
                                                      edpOn=True,
                                                      categoryIDs=[0, 16],
                                                      event_hub_id=self.event_hub_index[0])
        self.cms_config.add_surface_bet(selection_id=selection_ids[team2],
                                        content=self.content,
                                        priceNum=self.price_num,
                                        priceDen=self.price_den,
                                        eventIDs=self.eventID,
                                        edpOn=True,
                                        categoryIDs=[0, 16],
                                        event_hub_id=self.event_hub_index[0])
        self.__class__.surface_bet_title = surface_bet.get('title').upper()
        self.__class__.surface_bet_id = surface_bet.get('id')

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
        selected_tab = tabs_cms[0] if tabs_cms[0] != '5-A-SIDE' else tabs_cms[1]
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
        self.create_surface_bets()
        result = wait_for_result(lambda: f'/{self.event_hub_index[0]}' in self.device.get_current_url(),
                                 name=f'Waiting for Event hub with index "{self.event_hub_index[0]}"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Did not navigate to Event hub with index "{self.event_hub_index[0]}"')
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        event_name, sb_event = list(surface_bets.items())[0]
        self.assertTrue(sb_event.is_displayed(), msg=f'surface bet "{event_name}" is not displayed')

    def test_001_in_cms_disable_one_of_the_surface_bets_and_save_changes(self):
        """
        DESCRIPTION: In CMS disable one of the Surface Bets and save changes.
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id, disabled=True)

    def test_002_in_application_refresh_the_pageverify_disabled_surface_bet_isnt_shown_within_the_carousel(self):
        """
        DESCRIPTION: In application refresh the page.
        DESCRIPTION: Verify disabled Surface Bet isn't shown within the carousel.
        EXPECTED: Disabled Surface bet isn't shown
        """
        # changes for surface bets is taking sometime to reflect
        sleep(10)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(
            self.surface_bet_title)
        self.assertFalse(surface_bets,
                         msg=f'Disabled surface bet "{self.surface_bet_title}" is appearing on UI')

    def test_003_in_cms_enable_previously_disabled_surface_bets(self):
        """
        DESCRIPTION: In CMS enable previously disabled Surface Bets.
        """
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id, disabled=False)

    def test_004_in_application_refresh_the_pageverify_reenabled_surface_bet_is_shown_within_the_carousel(self):
        """
        DESCRIPTION: In application refresh the page.
        DESCRIPTION: Verify reenabled Surface Bet is shown within the carousel.
        EXPECTED: Surface bet is now shown
        """
        # changes for surface bets is taking sometime to reflect
        sleep(10)
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict.get(
            self.surface_bet_title)
        self.assertTrue(surface_bets,
                        msg=f'Enabled surface bet "{self.surface_bet_title}" is not appearing on UI')
