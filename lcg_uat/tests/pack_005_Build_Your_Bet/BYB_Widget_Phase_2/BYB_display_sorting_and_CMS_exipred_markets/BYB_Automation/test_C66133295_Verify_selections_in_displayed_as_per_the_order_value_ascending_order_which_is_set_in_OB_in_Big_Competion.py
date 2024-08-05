import re
import tests
import pytest
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from datetime import datetime
from tzlocal import get_localzone
from crlat_cms_client.utils.date_time import get_date_time_as_string
import requests
import json
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.byb_widget
@pytest.mark.OZONE_15384
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.insprint_auto
@pytest.mark.desktop
@vtest
class Test_C66133295_Verify_selections_in_displayed_as_per_the_order_value_ascending_order_which_is_set_in_OB_in_Big_Competion(BaseBetSlipTest):
    """
    TR_ID: C66133295
    NAME: Verify selections in displayed as per the order value ascending order which is set in OB in Big Competion
    DESCRIPTION: This testcase is to verify selections in BYB widget to be displayed as per the order value which is set in OB in Big Competion
    PRECONDITIONS: 1) Create BYB market card in Big Competition Page for the event in OB 2) BYB Widget sub section should be created under BYB main section3) Navigate a BYB active card for the above created event in OB
    """
    keep_browser_open = True
    timezone = str(get_localzone())
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
                                              url_encode=False, minutes=2)[:-3] + 'Z'
        elif self.timezone.upper() == 'EUROPE/LONDON':
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, hours=-1, minutes=2)[:-3] + 'Z'
        else:
            date_to = get_date_time_as_string(date_time_obj=datetime.now(),
                                              time_format='%Y-%m-%dT%H:%M:%S.%f',
                                              url_encode=False, hours=-5.5, minutes=2)[:-3] + 'Z'
        return date_to

    def reading_disp_order_from_Big_competition(self, market_ids, bid_competion_id, outcomes=None):
        # Reading Modules from FSC calls
        env = tests.settings.cms_env
        if env == 'hlv0':
            env = 'beta'
        elif env == 'prd0':
            env = 'prod'
        url = f'https://bigcompetition.{env}.coral.co.uk/competition/tab/{bid_competion_id}' if self.brand == 'bma' else \
            f'https://bigcompetition.{env}.ladbrokes.com/competition/tab/{bid_competion_id}'
        byb_data = requests.get(url=url)
        # Check the response status code and print the response content
        if byb_data.status_code == 200:
            # Convert the response content (which is a JSON string) to a dictionary
            byb_data_response_dict = json.loads(byb_data.content)
            for module in byb_data_response_dict['competitionModules']:
                if module['type'] == 'BYB_WIDGET':
                    byb_widget_FE = module['data']
                    for byb_widget_data_FE in byb_widget_FE:
                        if byb_widget_data_FE['marketId'] in market_ids:
                            markets = byb_widget_data_FE['event']['markets']
                            for market in markets:
                                outcomes = market['outcomes']
                            break
                    break
            else:
                raise CMSException("BYB Title is not Match in FE")
        return outcomes

    def is_all_negative(self, lst):
        return all(x < 0 for x in lst)

    def is_ascending(self, lst):
        return lst == sorted(lst)

    def check_list(self, lst):
        if self.is_all_negative(lst):
            return self.is_ascending(lst)
        else:
            return False

    def test_000_preconditions(self):
        """
        Description: checking Byb_module is enabled in Big Competition Page
        Expected:
        """
        # getting byb widget data
        byb = self.cms_config.get_byb_widget()
        self.__class__.byb_widget_container_title = byb.get('title')
        byb_widget_datas = byb.get('data')
        byb_widget_card_locations = []
        byb_widget_cards_ids = []
        self.__class__.byb_widget_market_ids = []
        for byb_widget_data in byb_widget_datas:
            byb_widget_cards_ids.append(byb_widget_data['id'])
            self.byb_widget_market_ids.append(byb_widget_data['marketId'])
            byb_widget_card_locations.append(byb_widget_data.get('locations'))
        # Big Competition page
        big_competitions = self.cms_config.get_big_competition()
        if len(byb_widget_card_locations) == 0:
            for competition in big_competitions:
                if competition['name'].upper() == "WORLD CUP":
                    if not competition['enabled']:
                        raise CMSException("World Cup Big competiotion id not enabled")
                    big_competition_id = competition.get('id')
                    self.cms_config.create_new_market_cards(title='Auto_BYB', event_id='',
                                                            market_id='', date_from=self.date_from(),
                                                            date_to=self.date_to(), locations=big_competition_id)

        else:
            type_id = None
            for competition in big_competitions:
                for byb_widget in byb_widget_card_locations:
                    if competition.get('id') in byb_widget:
                        if competition['enabled']:
                            competition_tabs = competition['competitionTabs']
                            for sub_tabs in competition_tabs:
                                if sub_tabs['name'] == 'Highlights':
                                    self.__class__.competition_tab_id = sub_tabs['id']
                                    competition_modules = sub_tabs['competitionModules']
                                    for byb_widget_module in competition_modules:
                                        if byb_widget_module['name'] == 'BYB Widget':
                                            if not byb_widget_module['enabled']:
                                                self.cms_config.update_next_events_module_for_big_competition(module_name='BYB Widget',
                                                                                                                module_type='BYB_WIDGET',
                                                                                                                module_id=self.competition_tab_id,
                                                                                                                type_id=type_id,enabled='true')
                                        else:
                                            # if BYB Widget is not present in Highlights tab creating BYB Widget
                                            new_module = self.cms_config.create_module_for_big_competation(
                                                    competition_id=competition.get('id'),
                                                    tab_id=self.competition_tab_id, module_name='BYB Widget',
                                                    module_type='BYB_WIDGET')

                                            break  # Break added here to stop further iteration
                                    break  # Break added here to stop further iteration
                            break

    def test_001_launch_ladscoral_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch Lads/Coral and login with valid credentials
        EXPECTED: Login should be successful
        """
        self.site.login()

    def test_002_navigate_to_big_competition_page(self):
        """
        DESCRIPTION: Navigate to Big Competition Page
        EXPECTED: User should be navigated to big Competition Page
        """
        self.navigate_to_page(name=f'/big-competition/world-cup')
        self.site.wait_content_state_changed(timeout=10)

    def test_003_verify_the_display_of_byb_widget_in_big_competition(self):
        """
        DESCRIPTION: Verify the display of BYB Widget in Big Competition
        EXPECTED: User can able to see the BYB Widget
        """
        self.__class__.byb_outcome_ids_FE = []
        # verifying BYB Widget container present or not
        self.assertTrue(self.site.home.has_byb_widget,msg='BYB Widget container is not present in Home Page' )
        self.__class__.byb_widget_containers = self.site.home.byb_widget.items_as_ordered_dict
        self.assertTrue(self.byb_widget_containers, msg='BYB Widget sliders are not present')
        for byb_widget_container_name, byb_widget_container in self.byb_widget_containers.items():
            self.assertEqual(byb_widget_container_name.upper(), self.byb_widget_container_title.upper(),
                             msg=f'Expected BYB Widget container Title from CMS: {self.byb_widget_container_title.upper()} and '
                                 f'Actual BYB Widget Container Title from FE:{byb_widget_container_name.upper()} both are not same')
            # Verifying BYB Widget accordions
            byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup
            self.assertTrue(byb_widgets, msg='BYB Widget is not present in Home Page')
            for byb_widget_name, byb_widget in byb_widgets.items():
                # verifying BYB widget cards
                byb_sections = byb_widget.items_as_ordered_dict_inc_dup
                self.assertTrue(byb_sections, msg='BYB Widget cards is not present in Home Page')
                for byb_section_name, byb_section in byb_sections.items():
                    result = byb_section.has_card_odds()
                    self.assertTrue(result, msg="BYB Widget Cards odds are not displaying ")
                    self.byb_outcome_ids_FE.append(int(byb_section.card_odds.selection_id))

                count = byb_widget.byb_footer_page_counter
                numbers = re.findall(r'\d+', count)

                # Convert extracted numbers to integers
                numbers = [int(num) for num in numbers]

                # Find the highest number
                highest_number = max(numbers)
                for i in range(1, highest_number):
                    if highest_number >= i:
                        byb_widget.right_arrow.click()
                        byb_sections = byb_widget.items_as_ordered_dict_inc_dup
                        for byb_section_name, byb_section in byb_sections.items():
                            result = byb_section.has_card_odds()
                            self.assertTrue(result, msg="BYB Widget Cards odds are not displaying ")
                            self.byb_outcome_ids_FE.append(int(byb_section.card_odds.selection_id))
                break

            break

    def test_004_verify_the_selections_order_id_siplayed_as_per_display_order_in_the_ob(self):
        """
        DESCRIPTION: Verify the selections order id siplayed as per display order in the OB
        EXPECTED: Selections order should be as per display order in OB
        """
        # Verifying BYB Widget outcome ids are ascending order in FE
        result = self.is_ascending(self.byb_outcome_ids_FE)
        if result:
            self.assertTrue(result, msg=f'FE Selection ids are not in ascendng order')
        else:
            outcomes = self.reading_disp_order_from_Big_competition(market_ids=self.byb_widget_market_ids,
                                                                    bid_competion_id=self.competition_tab_id)
            display_order_in_FE = []
            for id in self.byb_outcome_ids_FE:
                for outcome in outcomes:
                    if id == outcome['id']:
                        display_order_in_FE.append(int(outcome['displayOrder']))
            self.assertTrue(self.is_ascending(display_order_in_FE),
                            msg='display orders of selection ids are not in sort order')

    def test_005_verify_the_selections_order_for_the_two_selections_for_which_same_disporder_is_set_in_ob(self):
        """
        DESCRIPTION: Verify the selections order for the two selections for which same disporder is set in OB
        EXPECTED: Selections ID ascending order is compared and smaller one is displaed first folloed the second one
        """
        # Covered in above step
        # place bet
        for byb_widget_container_name, byb_widget_container in self.byb_widget_containers.items():
            # Verifying BYB Widget accordions
            byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup
            for byb_widget_name, byb_widget in byb_widgets.items():
                # verifying BYB widget cards
                byb_sections = byb_widget.items_as_ordered_dict
                for byb_outcome_name, byb_section in byb_sections.items():
                    result = byb_section.has_card_odds()
                    self.assertTrue(result, msg="BYB Widget Cards odds are not displaying ")
                    byb_section.card_odds.click()
                    break
                break
            break
        # verifying the selection in betslip
        if self.device_type == 'desktop':
            self.site.open_betslip()
            betslip = self.get_betslip_content()
            self.assertTrue(betslip, msg='Betslip is not displayed')
            singles_section = self.get_betslip_sections().Singles
            for selection_name, selection in singles_section.items():
                self.assertEqual(byb_outcome_name, selection_name, msg="both names are not same")
        else:
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel.selection.content
            self.assertTrue(quick_bet, msg='Quick Bet content is not loading')

        # place bet
        if self.device_type == 'mobile':
            quick_bet = self.site.quick_bet_panel.selection.content
            quick_bet.amount_form.input.click()
            quick_bet.amount_form.input.value = self.bet_amount
            self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                            msg='The button "Place bet" is not active')
            self.site.quick_bet_panel.place_bet.click()
            wait_for_haul(3)            
        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
