from time import sleep

import pytest
from selenium.common.exceptions import StaleElementReferenceException
import tests
from tests.base_test import vtest
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
@pytest.mark.featured
@pytest.mark.cms
@vtest
class Test_C9607556_Verify_expired_future_Surface_Bets_displaying(BaseFeaturedTest):
    """
    TR_ID: C9607556
    VOL_ID: C9776272
    NAME: Verify expired/future Surface Bets displaying
    DESCRIPTION: Test case verifies that expired/future Surface Bet isn't shown
    PRECONDITIONS: 1. There are a Surface Bet added to the SLP/Homepage in the CMS
    PRECONDITIONS: 2. Open this SLP/Homepage page in the application
    PRECONDITIONS: CMS path for the Homepage: Sport Pages > Homepage > Surface Bets Module
    PRECONDITIONS: CMS path for the sport category: Sport Pages > Sport Categories > Category > Surface Bets Module
    """
    keep_browser_open = True
    surface_bet_id = None
    surface_bet_title = ''
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

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

        category_id = self.ob_config.football_config.category_id
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
            event = self.ob_config.add_football_event_to_uefa_champions_league()
            self.__class__.selection_ids, self.__class__.team1 = event.selection_ids, event.team1
            self.__class__.selection_id = self.selection_ids[self.team1]
        surface_bet = self.cms_config.add_surface_bet(selection_id=self.selection_id,
                                                      categoryIDs=category_id)
        self.__class__.surface_bet_id = surface_bet.get('id')
        self.__class__.surface_bet_title = surface_bet.get('title').upper()

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')

        result = self.wait_for_surface_bets(name=self.surface_bet_title, timeout=1, poll_interval=1,
                                            raise_exceptions=False)
        if result is None:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.wait_for_surface_bets(name=self.surface_bet_title, timeout=15, poll_interval=1)

        surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')

    def test_001_in_the_cms_edit_the_surface_bet_set_display_from_to_to_the_past(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the past.
        """
        past_date_from = self.get_date_time_formatted_string(time_format=self.time_format, days=-2)[:-3] + 'Z'
        past_date_to = self.get_date_time_formatted_string(time_format=self.time_format, days=-1)[:-3] + 'Z'
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=past_date_from,
                                           displayTo=past_date_to)

        sleep(15)  # there's delay between putting values on CMS and appearance on UI

    def test_002_in_the_application_refresh_the_slp_homepage_verify_this_surface_bet_isnt_displayed(self):
        """
        DESCRIPTION: In the application refresh the SLP/Homepage verify this Surface bet isn't displayed
        EXPECTED: Surface Bet isn't displayed
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state('football')

        if self.site.football.tab_content.has_surface_bets():
            try:
                surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
            except StaleElementReferenceException:
                surface_bets = self.site.football.tab_content.surface_bets.items_as_ordered_dict
            self.assertTrue(surface_bets, msg='No Surface Bets found')
            surface_bet = surface_bets.get(self.surface_bet_title)
            self.assertFalse(surface_bet, msg=f'"{self.surface_bet_title}" found in "{list(surface_bets.keys())}"')

    def test_003_in_the_cms_edit_the_surface_bet_set_display_fromto_to_the_future(self):
        """
        DESCRIPTION: In the CMS edit the Surface Bet: set Display From/To to the future.
        """
        future_date_from = self.get_date_time_formatted_string(time_format=self.time_format, days=2)[:-3] + 'Z'
        future_date_to = self.get_date_time_formatted_string(time_format=self.time_format, days=3)[:-3] + 'Z'
        self.cms_config.update_surface_bet(surface_bet_id=self.surface_bet_id,
                                           displayFrom=future_date_from,
                                           displayTo=future_date_to)

    def test_004_in_the_application_refresh_the_slp_homepage_verify_this_surface_bet_isnt_displayed(self):
        """
        DESCRIPTION: In the application refresh the SLP/Homepage verify this Surface bet isn't displayed
        EXPECTED: Surface Bet isn't displayed
        """
        self.test_002_in_the_application_refresh_the_slp_homepage_verify_this_surface_bet_isnt_displayed()
