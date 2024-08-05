import re
from datetime import datetime
import pytest
import tests
import json
import voltron.environments.constants as vec
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from voltron.utils.helpers import do_request
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.byb_widget
@pytest.mark.desktop
@pytest.mark.adhoc_suite
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66100486_Verify_the_GA_Tracking_for_the_Place_Bet(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C66100486
    NAME: Verify the GA Tracking for the Place Bet
    DESCRIPTION: This test case is to verify the GA Tracking for the Place Bet
    PRECONDITIONS: 1. BYB Widget sub section should be created under BYB main section and active for the Football Home page
    PRECONDITIONS: 2. Navigation to go CMS -> BYB -> BYB Widget
    """
    keep_browser_open = True
    bet_amount = 0.1
    headers = {'Content-Type': 'application/json'}
    enable_bs_performance_log = True

    def get_outcome_details(self):
        wait_for_haul(5)
        url = f'{tests.settings.BETTINGMS}v1/buildBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        post_data = placebet_request.get('postData')
        self.assertTrue(post_data, msg='Post Data is not found in placeBet request')
        legs = post_data.get('leg')
        self.assertTrue(legs, msg='No Legs found in placeBet request')
        for leg in legs:
            sports_leg = leg.get('sportsLeg')
            self.assertTrue(sports_leg, msg='No sportsLeg found in placeBet request')
            price = sports_leg.get('price')
            self.assertTrue(price, msg='No price found in placeBet request')
            price_type_ref = price.get('priceTypeRef')
            self.assertTrue(price_type_ref, msg='No priceTypeRef found in placeBet request')
        data = json.dumps(post_data)
        req = do_request(url=url, data=data, headers=self.headers)
        outcome_details = req['outcomeDetails']
        return outcome_details

    def verify_ga_tracking_of_bet_receipt(self, category_id, selection_id, event_id, type_id, bet_id, odds, market_name,
                                          event_name, eventcategory, tab_name,belongs_inplay=1, url=None):

        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value=eventcategory)
        self.assertTrue(re.match(r'[0-9]+', event_id),
                        msg='Event id "%s" has incorrect format.\nExpected format: "xxxxxxx"' % event_id)
        if self.device_type == 'desktop':
            expected_response = {
                'ecommerce': {
                    'purchase': {
                        'actionField': {
                            'id': bet_id + ':1',
                            'revenue': self.bet_amount
                        },
                        'products': [
                            {
                                'brand': 'BuildABet in-play and cash out Spain',
                                'category': str(category_id),
                                'dimension60': str(event_id),
                                'dimension61': str(selection_id),
                                'dimension62': 0,
                                'dimension63': 0,
                                'dimension64': tab_name,
                                'dimension65': 'byb widget',
                                'dimension66': 1,
                                'dimension67': odds,
                                'dimension86': 0,
                                'dimension166': 'normal',
                                'dimension180': f'sport/football-1cc-1pc-1bp-{event_name}',
                                'dimension87': 0,
                                'dimension88': None,
                                'id': bet_id,
                                'name':event_name ,
                                'price': self.bet_amount,
                                'variant': int(type_id),
                                'quantity': 1,
                                'metric1': 0
                            }
                        ]
                    }
                },
                'event': 'trackEvent',
                'eventAction': 'place bet',
                'eventCategory': eventcategory,
                'eventLabel': 'success',
                'location': url
            }
        else:
            expected_response = {
                'event': 'trackEvent',
                'eventAction': 'place bet',
                'eventCategory': eventcategory,
                'eventLabel': 'success',
                'ecommerce': {
                    'purchase': {
                        'actionField': {
                            'id': bet_id,
                            'revenue': self.bet_amount
                        },
                        'products': [
                            {
                                'brand': market_name,
                                'category': str(category_id),
                                'dimension60': str(event_id),
                                'dimension61': str(selection_id),
                                'dimension62': 0,
                                'dimension63': 0,
                                'dimension64': tab_name,
                                'dimension65': 'byb widget',
                                'dimension66': 1,
                                'dimension67': odds,
                                'dimension86': 0,
                                'dimension166': 'normal',
                                'dimension180': f'sport/football-1cc-1pc-1bp-{event_name}',
                                'dimension87': 0,
                                'dimension88': None,
                                'metric1': 0,
                                'id': bet_id,
                                'name': 'single',
                                'price': self.bet_amount,
                                'variant': type_id
                            }
                        ]
                    }
                }
            }
        self.assertEqual(actual_response, expected_response)

    def test_000_preconditions(self):
        """
        Description: checking Byb_module is enabled in Football SLP
        Expected:
        """
        # verifying BYB Widget enabled or not in Football SLP page
        BYb_widget_football = self.cms_config.get_sport_module(module_type='BYB_WIDGET')
        id_ = BYb_widget_football[0].get('id')
        if BYb_widget_football[0]['disabled']:
            raise CMSException('"BYB Widget" module is disabled on Football SLP')
        # getting byb widget data
        self.__class__.byb = self.cms_config.get_byb_widget()
        self.__class__.byb_widget_container_title = self.byb.get('title')
        byb_widget_datas = self.byb.get('data')
        self.__class__.byb_widget_card_locations = []
        byb_widget_cards_ids = []
        for byb_widget_data in byb_widget_datas:
            byb_widget_cards_ids.append(byb_widget_data['id'])
            self.byb_widget_card_locations.append(byb_widget_data.get('locations'))
        if len(self.byb_widget_card_locations) == 0:
            self.cms_config.create_new_market_cards(title='Test1', event_id='244941566', market_id='836300153',
                                                    location='Football Homepage')
        elif 'Football Homepage' in [item for sublist in self.byb_widget_card_locations for item in sublist]:
            self._logger.info('BYB Widget is enabled in Football SLP')
        else:
            self.cms_config.update_market_cards(market_card_id=byb_widget_cards_ids[0], location='Football Homepage')

    def test_001_launch_the_application_and_login_with_valid_credentials(self):
        """
        DESCRIPTION: Launch the application and login with valid credentials
        EXPECTED: Able to launch the application and login successfully
        """
        self.site.login()

    def test_002_navigate_to_the_football_home_page(self):
        """
        DESCRIPTION: Navigate to the Football Home page
        EXPECTED: User can able to navigate to the Football Home page successfully
        """

        self.navigate_to_page(name='sport/football')
        football_page = self.site.wait_content_state(vec.siteserve.FOOTBALL_TAB)
        self.assertTrue(football_page, msg='User not on Football page')
        self.__class__.expected_sport_tab = self.site.football.tabs_menu.current
        sport_tab_from_cms = \
            self.get_sport_tab_name(
                self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                self.ob_config.football_config.category_id)
        self.assertEqual(self.expected_sport_tab, sport_tab_from_cms,
                         msg=f'Default tab is not "{sport_tab_from_cms}", it is "{self.expected_sport_tab}"')

    def test_003_verify_the_display_of_byb_widget_on_the_byb_homepage(self):
        """
        DESCRIPTION: Verify the display of BYB Widget on the BYB Homepage
        EXPECTED: User can able to see the BYB Widget
        """
        # verifying BYB Widget container present or not
        byb_widget_containers = self.site.home.byb_widget.items_as_ordered_dict
        self.assertTrue(byb_widget_containers, msg='BYB Widget container is not present in Football SLP')
        for byb_widget_container_name, byb_widget_container in byb_widget_containers.items():
            self.assertEqual(byb_widget_container_name.upper(), self.byb_widget_container_title.upper(),
                             msg=f'Actual BYB Widget container Title from CMS: {self.byb_widget_container_title.upper()} and '
                                 f'Expected BYB Widget Container Title from FE:{byb_widget_container_name.upper()} both are not same')
            # Verifying BYB Widget accordions
            byb_widgets = byb_widget_container.items_as_ordered_dict_inc_dup
            self.assertTrue(byb_widgets, msg='BYB Widget is not present in Football SLP')
            for byb_widget_name, byb_widget in byb_widgets.items():
                self.__class__.byb_widget_name_v = byb_widget.name
                # verifying BYB widget cards
                byb_sections = byb_widget.items_as_ordered_dict
                self.assertTrue(byb_sections, msg='BYB Widget cards is not present in Football SLP')
                for self.__class__.byb_section_name, byb_section in byb_sections.items():
                    result = byb_section.has_card_odds()
                    self.assertTrue(result, msg="BYB Widget Cards odds are not displaying ")
                    byb_section.card_odds.click()
                    break
                break
            break

    def test_004_click_on_any_selection_and_add_to_betslip(self):
        """
        DESCRIPTION: Click on any selection and add to betslip
        EXPECTED: User can click on any selection and can add to betslip successfully
        """
        # verifying the selection in betslip
        if self.device_type == 'desktop':
            self.site.open_betslip()
            betslip = self.get_betslip_content()
            self.assertTrue(betslip, msg='Betslip is not displayed')
            singles_section = self.get_betslip_sections().Singles
            for selection_name, selection in singles_section.items():
                self.assertEqual(self.byb_section_name, selection_name, msg="both names are not same")
        else:
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            quick_bet = self.site.quick_bet_panel.selection.content
            self.assertTrue(quick_bet, msg='Quick Bet content is not loading')

    def test_005_enter_the_stake_and_place_a_bet(self):
        """
        DESCRIPTION: Enter the stake and place a bet
        EXPECTED: User can enter the stake and place a bet successfully
        """
        if self.device_type=='mobile':
            quick_bet = self.site.quick_bet_panel.selection.content
            quick_bet.amount_form.input.click()
            quick_bet.amount_form.input.value = self.bet_amount
            self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(),
                            msg='The button "Place bet" is not active')
            self.site.quick_bet_panel.place_bet.click()
            wait_for_haul(3)
            self.__class__.bet_receipt_id = self.site.quick_bet_panel.bet_receipt.bet_id

        else:
            self.place_single_bet()
            self.check_bet_receipt_is_displayed()
            self.__class__.bet_receipt_id = self.site.bet_receipt.bet_id
        # Here we are taking category id,selection id etc...from build bet call
        outcome_details = self.get_outcome_details()
        for outcome in outcome_details:
            if self.byb_section_name.replace(" ", "") == outcome['name'].replace(" ", ""):
                self.__class__.byb_widget_event_id = outcome['eventId']
                self.__class__.byb_widget_type_id = outcome['typeId']
                self.__class__.byb_widget_category_id = outcome['categoryId']
                self.__class__.byb_widget_selection_id = outcome['id']
                self.__class__.byb_widget_market_desc = outcome['marketDesc']
                self.__class__.byb_widget_event_dec = outcome['eventDesc']
                self.__class__.byb_widget_pricenum = outcome['priceNum']
                self.__class__.byb_widget_priceDen = outcome['priceDen']
                break

    def test_006_verify_ga_tracking(self):
        """
        DESCRIPTION: Verify GA Tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: betslip,
        EXPECTED: component.LabelEvent: success,
        EXPECTED: component.ActionEvent: place bet,
        EXPECTED: ecommerce : object,
        EXPECTED: .purchase:object,
        EXPECTED: .id: {{transactionId},
        EXPECTED: .revenue: revenue ex:0.5,
        EXPECTED: .products: array,
        EXPECTED: .0: object,
        EXPECTED: .name :  HVBD Nutifood U21 v Sanna Khanh Hoa U21,
        EXPECTED: .id:    O/191499836/0000003,
        EXPECTED: .price : 0.5,
        EXPECTED: .dimension60: 238271291,
        EXPECTED: .dimension61: 1815133198,
        EXPECTED: .dimension62: 1,
        EXPECTED: .dimension63: 0,
        EXPECTED: .dimension64:'byb widget',
        EXPECTED: .dimension65: 'next events' ,
        EXPECTED: .dimension66 :1,
        EXPECTED: .dimension67: 81,
        EXPECTED: .dimension86 :0,
        EXPECTED: .metric1 : 0,
        EXPECTED: .category: 16,
        EXPECTED: .variant:1935,
        EXPECTED: .brand : build your own bet,
        EXPECTED: .quantity:1,
        EXPECTED: .dimension87: 0,
        EXPECTED: .dimension88: null,
        EXPECTED: .dimension180:  {location of bet(card) - postion of card - page of the card - on position of card on page - card name
        EXPECTED: ex: homepage - 2cc - 3pc - 1bp- england vs scotland } /* bet_deatils*/
        EXPECTED: }]
        EXPECTED: });
        """
        odds = round(float(int(self.byb_widget_pricenum) / int(self.byb_widget_priceDen)) + 1, 2)
        url = self.device.get_current_url().replace(f'https://{tests.HOSTNAME}', '').split('?')[0]
        self.verify_ga_tracking_of_bet_receipt(category_id=self.byb_widget_category_id,
                                               selection_id=self.byb_widget_selection_id,
                                               event_id=self.byb_widget_event_id,
                                               type_id=self.byb_widget_type_id,
                                               bet_id=self.bet_receipt_id,
                                               odds=odds,
                                               tab_name=self.expected_sport_tab,
                                               market_name=self.byb_widget_market_desc,
                                               event_name=self.byb_widget_event_dec,
                                               url=url if self.device_type == 'desktop' else None,
                                               eventcategory='quickbet' if self.device_type == 'mobile' else 'betslip'
                                               )

    def test_007_verify_ga_tracking_in_console_for_the_dimension64_and_dimension180(self):
        """
        DESCRIPTION: Verify GA tracking in console for the dimension64 and dimension180
        EXPECTED: .dimension64:'byb widget',
        EXPECTED: .dimension180:  {location of bet(card) - postion of card - page of the card - on position of card on page - card name
        EXPECTED: ex: homepage - 2cc - 3pc - 1bp- england vs scotland } /* bet_deatils*/
        """
        # covered in above step
