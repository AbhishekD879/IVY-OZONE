
import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
from tests.Common import Common
from tests.base_test import vtest
from tzlocal import get_localzone
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
import requests
import json
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.byb_widget
@pytest.mark.OZONE_15083
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.insprint_auto
@pytest.mark.desktop
@vtest
class Test_C66133015_Verify_selections_in_BYB_widget_when_pagination_is_enabled_and_disabled(Common):
    """
    TR_ID: C66133015
    NAME: Verify selections in BYB widget when pagination is enabled and disabled
    DESCRIPTION: This testcase is to verify selections in BYB widget when pagination is enabled and disabled
    PRECONDITIONS: 1.Create BYB market for the event in OB
    PRECONDITIONS: 2. BYB Widget sub section should be created under BYB main section
    PRECONDITIONS: 3. Navigation to go CMS -> BYB -> BYB Widget
    PRECONDITIONS: 4.Create a BYB active card for the above created event in OB
    """
    keep_browser_open = True
    timezone = str(get_localzone())
    byb_widget_cards_ids = []

    def date_from(self):
        # Time Zone validation
        if self.timezone.upper() == "UTC":
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, minutes=-1)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, hours=-1, minutes=-1)[:-3] + 'Z'
        else:
            date_from = get_date_time_as_string(date_time_obj=datetime.now(),
                                                time_format='%Y-%m-%dT%H:%M:%S.%f',
                                                url_encode=False, hours=-5.5, minutes=-1)[:-3] + 'Z'
        return date_from

    def date_to(self):
        # Time Zone validation

        if self.timezone.upper() == "UTC":
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, minutes=5)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, hours=-1, minutes=5)[:-3] + 'Z'
        else:
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, hours=-5.5, minutes=5)[:-3] + 'Z'
        return date_to

    def reading_disp_order_from_FSC(self, market_ids, outcomes=None):
        # Reading Modules from FSC calls
        env = tests.settings.cms_env
        if env == 'hlv0':
            env = 'hl'
        elif env == 'prd0':
            env = 'prod'
        url = f'https://cms-{env}.coral.co.uk/cms/api/bma/fsc/16' if self.brand == 'bma' else \
                f'https://cms-{env}.ladbrokes.com/cms/api/ladbrokes/fsc/16'

        byb_data = requests.get(url=url)
        # Check the response status code and print the response content
        if byb_data.status_code == 200:
            # Convert the response content (which is a JSON string) to a dictionary
            byb_data_response_dict = json.loads(byb_data.content)
            for module in byb_data_response_dict['modules']:
                if module['@type'] == 'BybWidgetModule':
                    byb_widget_FE = module['data']
                    for byb_widget_data_FE in byb_widget_FE:
                        if byb_widget_data_FE['marketId'] in [int(value) for value in market_ids]:
                            markets = byb_widget_data_FE['markets']
                            for market in markets:
                                outcomes = market['outcomes']
                            break
                    break
            else:
                raise CMSException("BYB Title is not Match in FE")
        return outcomes

    def test_000_preconditions(self):
        """
        Description: checking Byb_module is enabled in Football SLP
        Expected:
        """
        # verifying BYB Widget enabled or not in Football SLP page
        BYb_widget_football = self.cms_config.get_sport_module(module_type='BYB_WIDGET', sport_id=16)
        if BYb_widget_football[0]['disabled']:
            raise CMSException('"BYB Widget" module is disabled on Football SLP')
        self.__class__.byb = self.cms_config.get_byb_widget()
        byb_widget_datas = self.byb.get('data')
        self.__class__.byb_widget_container_title = self.byb.get('title')
        if self.byb['showAll'] is False:
            self.cms_config.update_byb_widget(showAll=True)
        byb_widget_card_locations = []
        for byb_widget_data in byb_widget_datas:
            self.byb_widget_cards_ids.append(byb_widget_data['marketId'])
            byb_widget_card_locations.append(byb_widget_data.get('locations'))

        market_ids = self.byb_widget_cards_ids.copy()

        byb_widget_market_cards_ob = self.ss_req.ss_events_to_outcome_for_markets(market_ids=market_ids)
        for card_ob in byb_widget_market_cards_ob:
            if card_ob['event']['isActive'] and card_ob['event']['eventStatusCode'] == 'A':
                self._logger.info("BYB Widget Event is active")
            else:
                raise CMSException("BYB Widget is not Active and Suspended")
        expected_locations = ['Football Homepage']
        if len(byb_widget_card_locations) == 0:
            self.cms_config.create_new_market_cards(title='Auto_BYB', event_id='5024809',
                                                    market_id='58736433', date_from=self.date_from(),
                                                    date_to=self.date_to(), locations=expected_locations)
        for expected_location in expected_locations:
            if expected_location in [item for sublist in byb_widget_card_locations for item in sublist]:
                self._logger.info('BYB Widget is enabled in Football SLP')
            else:
                self.cms_config.update_market_cards(market_card_id=self.byb_widget_cards_ids[0], locations=expected_location)

        self.__class__.byb_widget_cards_ids = [self.byb_widget_cards_ids]

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the application and login with valid credentials
        EXPECTED: Able to launch the application and login successfully
        """
        self.site.login()

    def test_002_navigate_to_the_football_landing_page(self):
        """
        DESCRIPTION: Navigate to the Football Landing page
        EXPECTED: User can able to navigate to the Football Landing page successfully
        """
        self.navigate_to_page(name='sport/football')
        football_page = self.site.wait_content_state('football')
        self.assertTrue(football_page, msg='User not on Football page')
        expected_sport_tab = self.site.football.tabs_menu.current
        sport_tab_from_cms = \
            self.get_sport_tab_name(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, self.ob_config.football_config.category_id)
        self.assertEqual(expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{expected_sport_tab}"')

    def test_003_verify_the_display_of_byb_widget(self, expected_result=True):
        """
        DESCRIPTION: Verify the display of BYB Widget
        EXPECTED: User can able to see the BYB Widget
        """
        # verifying BYB Widget container present or not
        outcomes = self.reading_disp_order_from_FSC(market_ids=self.byb_widget_cards_ids[0])
        global byb_widget_container
        self.assertTrue(self.site.home.has_byb_widget,msg='BYB Widget container is not present in Home Page' )
        self.__class__.byb_widget_containers = self.site.home.byb_widget.items_as_ordered_dict
        self.assertTrue(self.byb_widget_containers, msg='BYB Widget sliders are not present')
        for byb_widget_container_name, byb_widget_container in self.byb_widget_containers.items():
            self.assertEqual(byb_widget_container_name.upper(), self.byb_widget_container_title.upper(),
                             msg=f'Expected BYB Widget container Title from CMS: {self.byb_widget_container_title.upper()} and '
                                 f'Actually BYB Widget Container Title from FE:{byb_widget_container_name.upper()} both are not same')
        # Verifying BYB Widget accordions
        byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup
        self.assertTrue(byb_widgets, msg='BYB Widget is not present in Football SLP')
        for byb_widget_name, byb_widget in byb_widgets.items():
            self.__class__.byb_widget_name_v = byb_widget.name
            byb_footer_menu = byb_widget.has_byb_widget_footer
            self.assertTrue(byb_footer_menu,
                            msg=f'BYB Widget Footer Menu is not showing in :{self.byb_widget_name_v}')
            byb_footer_left_arrow = byb_widget.has_left_arrow(expected_result=expected_result)
            byb_footer_right_arrow = byb_widget.has_right_arrow(expected_result=expected_result)
            if expected_result:
                # FSc Call for BYB Market Cards
                if len(outcomes) > 5:
                    self.assertTrue(byb_footer_left_arrow,
                                     msg=f'BYB Widget Footer left arrow still showing in FE:{self.byb_widget_name_v}')
                    self.assertTrue(byb_footer_right_arrow,
                                     msg=f'BYB Widget Footer left arrow still showing in FE:{self.byb_widget_name_v}')
                else:
                    self.assertFalse(byb_footer_left_arrow,
                                    msg=f'BYB Widget Footer left arrow is not showing in :{self.byb_widget_name_v}')
                    self.assertFalse(byb_footer_right_arrow,
                                    msg=f'BYB Widget Footer left arrow is not showing in :{self.byb_widget_name_v}')
            else:
                self.assertFalse(byb_footer_left_arrow,
                                 msg=f'BYB Widget Footer left arrow still showing in FE:{self.byb_widget_name_v}')
                self.assertFalse(byb_footer_right_arrow,
                                 msg=f'BYB Widget Footer left arrow still showing in FE:{self.byb_widget_name_v}')

    def test_004_verify_selections_in_byb_widget_when_pagination_is_enabled(self):
        """
        DESCRIPTION: Verify selections in BYB widget when pagination is enabled
        EXPECTED: Chevrons to navigate to next selections should be updated without refresh
        """
        # Covered in above statement when pagination is enabled

    def test_005_verify_selections_in_byb_widget_when_pagination_is_disabled(self):
        """
        DESCRIPTION: Verify selections in BYB widget when pagination is disabled
        EXPECTED: Chevrons should NOT be displayed without refresh
        """
        self.cms_config.update_byb_widget(showAll=False)
        wait_for_haul(10)
        self.test_003_verify_the_display_of_byb_widget(expected_result=False)
        self.cms_config.update_byb_widget(showAll=True)
