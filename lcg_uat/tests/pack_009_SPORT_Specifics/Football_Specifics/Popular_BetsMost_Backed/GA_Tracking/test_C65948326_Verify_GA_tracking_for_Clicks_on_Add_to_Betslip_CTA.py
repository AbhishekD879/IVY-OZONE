import json
import pytest
from crlat_cms_client.utils.exceptions import CMSException
import re
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest
from voltron.utils.helpers import do_request
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.popular_bets
@pytest.mark.popular_bets_GA_tracking
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65948326_Verify_GA_tracking_for_Clicks_on_Add_to_Betslip_CTA(BaseDataLayerTest, BaseBetSlipTest):
    """
    TR_ID: C65948326
    NAME: Verify GA tracking for Clicks on Add to Betslip CTA
    DESCRIPTION: This test case verifies GA tracking for clicks on Add to Betslip CTA
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    PRECONDITIONS: Should have Football events
    """
    keep_browser_open = True
    headers = {'Content-Type': 'application/json'}
    enable_bs_performance_log = True

    def verify_ga_tracking_of_bet_receipt(self, category_id, selection_id, event_id, type_id, bet_id, odds, market_name,
                                          event_name, url, belongs_inplay=0):

        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='betslip')
        self.assertTrue(re.match(r'[0-9]+', event_id),
                        msg='Event id "%s" has incorrect format.\nExpected format: "xxxxxxx"' % event_id)

        expected_response = {
            'ecommerce': {
                'purchase': {
                    'actionField': {
                        'id': bet_id + ':1',
                        'revenue': self.bet_amount
                    },
                    'products': [
                        {
                            'brand': market_name,
                            'category': str(category_id),
                            'dimension60': str(event_id),
                            'dimension61': str(selection_id),
                            'dimension62': belongs_inplay,
                            'dimension63': 0,
                            'dimension64': self.tab_name.upper(),
                            'dimension65': 'Popular bets',
                            'dimension66': 1,
                            'dimension67': odds,
                            'dimension86': 0,
                            'dimension166': 'normal',
                            'dimension180': 'normal',
                            'dimension87': 0,
                            'dimension88': None,
                            'metric1': 0,
                            'id': bet_id,
                            'name': event_name,
                            'price': self.bet_amount,
                            'variant': int(type_id),
                            'quantity': 1
                        }
                    ]
                }
            },
            'event': 'trackEvent',
            'eventAction': 'place bet',
            'eventCategory': 'betslip',
            'eventLabel': 'success',
            'location': url
        }
        self.assertEqual(actual_response, expected_response)

    def get_outcome_details(self, selection_id):
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
        res = {od.get('id'): od for od in outcome_details}
        return res.get(selection_id)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)
        tab = next((tab for tab in all_sub_tabs_for_football if
                    tab['enabled'] and tab['name'] == 'popularbets'), None)
        self.__class__.tab_name = tab['displayName'].upper()
        self.__class__.label_event_tab_name = next(
            (sub_tab['trendingTabName'] for sub_tab in tab['trendingTabs'] for inner_sub_tab in sub_tab['popularTabs']
             if inner_sub_tab['popularTabName'] == 'Popular_tab'), None)
        if not self.tab_name:
            raise CMSException('Popular Bet tab is not enabled in CMS!!')
        self.__class__.category_id = self.ob_config.football_config.category_id

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: User should launch the Application Successfully
        """
        self.site.launch_application()
        self.site.login()

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        self.site.open_sport('football')

    def test_003_click_on_popular_bets_section(self):
        """
        DESCRIPTION: Click on Popular Bets section
        EXPECTED: Able to navigate to the Popular Bets section successfully
        """
        all_tabs = self.site.football.tabs_menu.get_items(name=self.tab_name)
        insights_tab = all_tabs.get(self.tab_name)
        insights_tab.click()
        wait_for_result(lambda: self.site.football.tabs_menu.current.upper() == self.tab_name.upper())
        current_tab = self.site.football.tabs_menu.current.upper()
        self.assertEqual(current_tab, self.tab_name.upper(), f'Actual Highlighted Tab : "{current_tab}" is not same as'
                                                             f'Expected Highlighted Tab : "{self.tab_name}"')

    def test_004_click_on_add_to_betslip__observe_ga_tracking(self):
        """
        Test Case ID: C65948326
        DESCRIPTION: Click on Add to betslip  ,Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'popular bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'time filters',
        EXPECTED: component.LocationEvent: 'insights',
        EXPECTED: component.EventDetails: 'add to betslip cta',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });

        Test Case ID: C65948327
        EXPECTATION 2:
        EXPECTED: Note: Don't duplicate if tracking is exists please add Highlighted Values
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: [{
        EXPECTED: eventCategory: betslip,
        EXPECTED: eventLabel: success ,
        EXPECTED: eventAction: add to betslip,
        EXPECTED: ecommerce : object,
        EXPECTED: add:object,
        EXPECTED: products: array,
        EXPECTED: 0:object,
        EXPECTED: name :  HVBD Nutifood U21 v Sanna Khanh Hoa U21,
        EXPECTED: dimension60: 238271291,
        EXPECTED: dimension61: 1815133198,
        EXPECTED: dimension62: 0,
        EXPECTED: dimension63: 0,
        EXPECTED: dimension64: {popular bets} ,
        EXPECTED: dimension65: '{betmodule}'
        EXPECTED: category: 16,
        EXPECTED: variant:1935,
        EXPECTED: brand : Match Betting,
        EXPECTED: dimension87: 0,
        EXPECTED: dimension86: 0,
        EXPECTED: dimension88: null,
        EXPECTED: }]
        EXPECTED: });
        """
        football_tabs = self.cms_config.get_sport_tabs(sport_id=self.ob_config.football_config.category_id)
        popular_bets_tabs = next((tab for tab in football_tabs if
                                  tab['enabled'] and tab['name'] == 'popularbets'), None)
        popular_bet_tab_name = next(
            (popular_bets_sub_tab['trendingTabName'] for popular_bets_sub_tab in popular_bets_tabs['trendingTabs'] for
             inner_sub_tab in popular_bets_sub_tab['popularTabs']
             if inner_sub_tab['popularTabName'] == 'Popular_tab'), None)
        self.site.football.tab_content.grouping_buttons.click_button(button_name=popular_bet_tab_name.upper())
        self.site.football.tab_content.accordions_list.add_to_betslip_button.click()

        expected_resp = {'event': 'Event.Tracking',
                         'component.CategoryEvent': 'betting',
                         'component.LabelEvent': self.label_event_tab_name,
                         'component.ActionEvent': 'click',
                         'component.PositionEvent': 'time filters',
                         'component.LocationEvent': self.tab_name.lower(),
                         'component.EventDetails': 'add to betslip cta',
                         'component.URLClicked': 'not applicable'}

        actual_resp = self.get_data_layer_specific_object(object_key='component.EventDetails',
                                                          object_value='add to betslip cta')
        self.assertEqual(expected_resp, actual_resp)

        outcome_from_fe = self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup.get(4)
        selection_id = outcome_from_fe.bet_button.selection_id
        last_outcome_details = self.get_outcome_details(selection_id)

        name = last_outcome_details.get('eventDesc')
        event_id = last_outcome_details.get('eventId')
        variant = last_outcome_details.get('typeId')
        market_name = 'Specials' if 'Specials' in last_outcome_details.get('marketDesc') else last_outcome_details.get('marketDesc')

        self.verify_ga_tracking_record(event='trackEvent',
                                       event_category='betslip',
                                       event_label='success',
                                       event_action='add to betslip',
                                       event_id=event_id,
                                       selection_id=selection_id,
                                       variant=variant,
                                       category=self.category_id,
                                       name=name,
                                       inplay_status=0,
                                       customer_built=0,
                                       location=self.tab_name.upper(),
                                       module='Popular bets',
                                       brand=market_name,
                                       quantity=1,
                                       stream_active=False,
                                       stream_ID=None,
                                       dimension87=0,
                                       dimension86=0,
                                       dimension88=None
                                       )

    def test_005_click_on_remove_from_betslip__observe_ga_tracking(self):
        """
        Test Case ID : C65948325
        DESCRIPTION: Click on Remove from betslip  ,Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'popular bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'time filters',
        EXPECTED: component.LocationEvent: 'popular bets',
        EXPECTED: component.EventDetails: 'remove from betslip cta',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.football.tab_content.accordions_list.remove_from_betslip.click()

        expected_resp = {'event': 'Event.Tracking',
                         'component.CategoryEvent': 'betting',
                         'component.LabelEvent': self.label_event_tab_name,
                         'component.ActionEvent': 'click',
                         'component.PositionEvent': 'time filters',
                         'component.LocationEvent': self.tab_name.lower(),
                         'component.EventDetails': 'remove from betslip cta',
                         'component.URLClicked': 'not applicable'}

        actual_resp = self.get_data_layer_specific_object(object_key='component.EventDetails',
                                                          object_value='remove from betslip cta')
        self.assertEqual(actual_resp, expected_resp)

    def test_006_click_on_show_more__observe_ga_tracking(self):
        """
        Test Case ID : C65948324
        DESCRIPTION: Click on Show more  ,Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'Event.Tracking',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: 'betting',
        EXPECTED: component.LabelEvent: 'popular bets',
        EXPECTED: component.ActionEvent: 'click',
        EXPECTED: component.PositionEvent: 'time filters',
        EXPECTED: component.LocationEvent: 'popular bets',
        EXPECTED: component.EventDetails: 'show more',
        EXPECTED: component.URLClicked: 'not applicable'
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.football.tab_content.accordions_list.show_more_less.click()

        expected_resp = {'event': 'Event.Tracking',
                         'component.CategoryEvent': 'betting',
                         'component.LabelEvent': self.label_event_tab_name,
                         'component.ActionEvent': 'click',
                         'component.PositionEvent': 'time filters',
                         'component.LocationEvent': self.tab_name.lower(),
                         'component.EventDetails': 'show more',
                         'component.URLClicked': 'not applicable'}

        actual_resp = self.get_data_layer_specific_object(object_key='component.EventDetails',
                                                          object_value='show more')
        self.assertEqual(expected_resp, actual_resp)

    def test_007_click_on_add_to_betslip_and_place_bet_observe_ga_tracking(self):
        """
        Test Case ID : C65948328
        DESCRIPTION: Click on Add to betslip  ,Observe GA tracking
        EXPECTED: dataLayer.push({
        EXPECTED: 'event': 'trackEvent',
        EXPECTED: [{
        EXPECTED: component.CategoryEvent: betslip,
        EXPECTED: component.LabelEvent: success,
        EXPECTED: component.ActionEvent: place bet,
        EXPECTED: ecommerce : object,
        EXPECTED: purchase:object,
        EXPECTED: id: {{transactionId},
        EXPECTED: revenue: revenue ex:0.5,
        EXPECTED: products: array,
        EXPECTED: 0: object,
        EXPECTED: name :  HVBD Nutifood U21 v Sanna Khanh Hoa U21,
        EXPECTED: id:    O/191499836/0000003,
        EXPECTED: price : 0.5,
        EXPECTED: dimension60: 238271291,
        EXPECTED: dimension61: 1815133198,
        EXPECTED: dimension62: 0,
        EXPECTED: dimension63: 0,
        EXPECTED: dimension64:{popular bets} ,
        EXPECTED: dimension65: '{betmodule}' ,
        EXPECTED: dimension66 :1,
        EXPECTED: dimension67: 81,
        EXPECTED: dimension86 :0,
        EXPECTED: metric1 : 0,
        EXPECTED: category: 16,
        EXPECTED: variant:1935,
        EXPECTED: brand : Match Betting,
        EXPECTED: quantity:1,
        EXPECTED: dimension87: 0,
        EXPECTED: dimension88: null
        EXPECTED: }]
        EXPECTED: });
        """
        self.site.football.tab_content.accordions_list.add_to_betslip_button.click()
        outcome_from_fe = self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup.get(4)
        selection_id = outcome_from_fe.bet_button.selection_id
        last_outcome_details = self.get_outcome_details(selection_id)

        name = last_outcome_details.get('eventDesc')
        event_id = last_outcome_details.get('eventId')
        variant = last_outcome_details.get('typeId')
        odds = round(float(int(last_outcome_details['priceNum']) / int(last_outcome_details['priceDen'])) + 1, 2)
        url = self.device.get_current_url().replace(f'https://{tests.HOSTNAME}', '').split('?')[0]

        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[-1]
        stake.amount_form.input.value = self.bet_amount
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        bet_receipt_id = self.site.bet_receipt.bet_id
        market_name = self.site.bet_receipt.market_type[:-2]

        self.verify_ga_tracking_of_bet_receipt(category_id=self.category_id,
                                               selection_id=selection_id, type_id=variant,
                                               bet_id=bet_receipt_id, odds=odds,
                                               market_name=market_name, event_name=name, event_id=event_id, url=url)
