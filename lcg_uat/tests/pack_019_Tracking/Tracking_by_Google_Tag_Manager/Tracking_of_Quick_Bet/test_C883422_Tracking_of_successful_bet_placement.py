import re
import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_019_Tracking.Tracking_by_Google_Tag_Manager.BaseDataLayerTest import BaseDataLayerTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.quick_bet
@pytest.mark.google_analytics
@pytest.mark.low
@pytest.mark.other
@pytest.mark.login
@vtest
class Test_C883422_Tracking_of_successful_bet_placement(BaseBetSlipTest, BaseDataLayerTest):
    """
    TR_ID: C883422
    VOL_ID: C9698160
    NAME: Tracking of successful bet placement
    DESCRIPTION: This test verifies successful bet placement
    PRECONDITIONS: * Test case should be run on Mobile Only
    PRECONDITIONS: * Browser console should be opened
    PRECONDITIONS: * To view response open Dev tools -> Network -> WS -> choose the last request
    PRECONDITIONS: * Quick Bet functionality should be enabled in CMS and user`s settings
    PRECONDITIONS: * User is logged in and has positive balance
    """
    keep_browser_open = True
    inplay_event_team1 = None
    inplay_event_selection_ids = None
    inplay_event_id = None

    def verify_tracking(self, category_id, selection_id, type_id, bet_id, belongs_inplay=0):
        actual_response = self.get_data_layer_specific_object(object_key='eventCategory', object_value='quickbet')
        event_id = actual_response[u'ecommerce'][u'purchase'][u'products'][0]['dimension60']
        self.assertTrue(re.match(r'[0-9]+', event_id),
                        msg='Event id "%s" has incorrect format.\nExpected format: "xxxxxxx"' % event_id)

        expected_response = {
            'ecommerce': {
                'purchase': {
                    'actionField': {
                        'id': bet_id,
                        'revenue': self.bet_amount
                    },
                    'products': [
                        {
                            'brand': vec.siteserve.EXPECTED_MARKETS_NAMES.match_result,
                            'category': str(category_id),
                            'dimension60': str(event_id),
                            'dimension61': str(selection_id),
                            'dimension62': belongs_inplay,
                            'dimension63': 0,
                            'dimension64': self.get_default_tab_name_on_sports_edp(event_id=self.event_id),
                            'dimension65': 'edp',
                            'dimension66': 1,
                            'dimension67': 1.5,
                            'dimension86': 0,
                            'dimension87': 0,
                            'dimension88': None,
                            'metric1': 0,
                            'id': bet_id,
                            'name': 'single',
                            'price': self.bet_amount,
                            'variant': str(type_id)
                        }
                    ]
                }
            },
            'event': 'trackEvent',
            'eventAction': 'place bet',
            'eventCategory': 'quickbet',
            'eventLabel': 'success'
        }
        self.compare_json_response(actual_response, expected_response)

        self.site.quick_bet_panel.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide(timeout=15)

    def click_bet_button(self, team):
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        section = markets_list.get(self.expected_market_sections.match_result)
        self.assertTrue(section, msg='MATCH RESULT section is not found')
        output_prices_list = section.outcomes.items_as_ordered_dict
        self.assertTrue(output_prices_list, msg='Match result output prices were not found on Event Details page')
        output_prices_list[team].bet_button.click()
        self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True), msg='Quick Bet is not present')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team1, self.__class__.team2, self.__class__.selection_ids, self.__class__.event_id = \
            event_params.team1, event_params.team2, event_params.selection_ids, event_params.event_id
        self.__class__.event_name = f'{event_params.team1} v {event_params.team2}'

        start_time = self.get_date_time_formatted_string(seconds=20)
        event_params2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True, start_time=start_time)
        self.__class__.inplay_event_team1, self.__class__.inplay_event_selection_ids, self.__class__.inplay_event_id = \
            event_params2.team1, event_params2.selection_ids, event_params2.event_id
        self.__class__.event_name2 = f'{event_params2.team1} v {event_params2.team2}'

    def test_001_login(self):
        """
        DESCRIPTION: Login as a user that has sufficient funds to place a bet
        EXPECTED: User successfully signed in
        """
        self.site.login(username=tests.settings.freebet_user)
        self.__class__.user_balance = self.site.header.user_balance

    def test_002_navigate_to_football_event_page(self):
        """
        DESCRIPTION: Navigate to Event Details page
        EXPECTED: Appropriate Event Details page opened
        """
        self.navigate_to_edp(self.event_id)
        self.__class__.user_balance = self.site.header.user_balance

    def test_003_click_on_football_event_bet_button(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        EXPECTED: Quick Bet is displayed
        EXPECTED: Added selection and all data are displayed in Quick Bet
        """
        if self.brand != 'ladbrokes':
            self.click_bet_button(self.team1)
        else:
            self.click_bet_button(self.team1.upper())

    def test_004_enter_value_in_stake_field(self):
        """
        DESCRIPTION: Enter value in 'Stake' field
        EXPECTED: * 'Stake' field is populated with entered value
        """
        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount

    def test_005_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'PLACE BET' button
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        self.site.quick_bet_panel.place_bet.click()
        bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.bet_receipt_id = self.site.quick_bet_panel.bet_receipt.bet_id

    def test_006_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        DESCRIPTION: Verify **'betID'** parameter
        DESCRIPTION: Verify **'betCategory'** parameter
        DESCRIPTION: Verify **'betInPlay'** parameter
        DESCRIPTION: Verify **'bonusBet'** parameter
        EXPECTED: * **'betID'** parameter is present and has correct format
        EXPECTED: * **'betCategory'** parameter corresponds to OB category name for particular <Sport> / <Race>
        EXPECTED: * **'betInPlay'** = 'No' if user tried to place a bet on selection from Pre Match event
        EXPECTED: * **'bonusBet'** = 'False' if user tried to place a bet without free bet
        """
        self.verify_tracking(category_id=self.ob_config.backend.ti.football.category_id,
                             selection_id=self.selection_ids[self.team1], bet_id=self.bet_receipt_id,
                             type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id)

    def test_007_navigate_to_inplay_event_page(self):
        """
        DESCRIPTION: Navigate to In-Play Event Details page
        """
        self.navigate_to_edp(self.inplay_event_id)

    def test_008_click_on_football_event_bet_button(self):
        """
        DESCRIPTION: Add inplay selection to Quick Bet
        EXPECTED: Quick Bet is displayed
        """
        if self.brand != 'ladbrokes':
            self.click_bet_button(self.inplay_event_team1)
        else:
            self.click_bet_button(self.inplay_event_team1.upper())
        self.test_004_enter_value_in_stake_field()
        self.test_005_tap_place_bet_button()

    def test_009_type_in_console_datalayer_tap_enter_and_check_the_response(self):
        """
        DESCRIPTION: Type in console **'dataLayer'**, tap 'Enter' and check the response
        DESCRIPTION: Verify **'betID'** parameter
        DESCRIPTION: Verify **'betCategory'** parameter
        DESCRIPTION: Verify **'betInPlay'** parameter
        DESCRIPTION: Verify **'bonusBet'** parameter

        EXPECTED: * **'betID'** parameter is present and has correct format
        EXPECTED: * **'betCategory'** parameter corresponds to OB category name for particular <Sport> / <Race>
        EXPECTED: * **'betInPlay'** = 'No' if user tried to place a bet on selection from Pre Match event
        EXPECTED: * **'bonusBet'** = 'False' if user tried to place a bet without free bet
        """
        self.verify_tracking(category_id=self.ob_config.backend.ti.football.category_id,
                             selection_id=self.inplay_event_selection_ids[self.inplay_event_team1],
                             bet_id=self.bet_receipt_id,
                             type_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
                             belongs_inplay=1)
