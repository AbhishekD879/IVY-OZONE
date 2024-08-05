import pytest
from crlat_siteserve_client.utils.helpers import do_request

from tests.base_test import vtest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.siteserve_client import exists_filter
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing



@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_selection_details
@pytest.mark.insprint_auto
@pytest.mark.desktop
@vtest
# covered test case C66113521
class Test_C66113519_Verify_Extra_Place_Signposting_at_selection_level_in_My_Bets_When_a_bet_is_placed_on_a_selection_which_offers_Extra_Place(BaseRacing,BaseBetSlipTest):
    """
    TR_ID: C66113519
    NAME: Verify Extra Place Signposting at selection level in My Bets When a bet is placed on a selection which offers Extra Place
    DESCRIPTION: This testcase verifies Extra Place Signposting at selection level in My Bets When a bet is placed on a selection which offers Extra Place
    PRECONDITIONS: Horse racing Bets on selections which offers Extra place should be avilable in open,cash out,Settled tabs
    """
    keep_browser_open = True
    markets_params = [('Win or Each Way', {})]

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/Get events
        """
        # url = 'https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.81/EventToOutcomeForEvent/{event_id}?referenceEachWayTerms=true&responseFormat=json'
        # resp = do_request(method='GET', url=url)
        # event = self.ss_req.ss_event_to_market_for_event(event_id='245322011')

        if tests.settings.backend_env == 'prod':
            additional_filter = []
            expected_template_market = 'Win or Each Way'
            additional_filter.append(
                exists_filter(LEVELS.EVENT, simple_filter(LEVELS.MARKET,
                                                          ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                          OPERATORS.INTERSECTS, 'MKTFLAG_EPR')))
            additional_filter.append(simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y'))
            additional_filter.append(simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                   OPERATORS.EQUALS, 'Y'))
            additional_filter.append(exists_filter(LEVELS.EVENT, simple_filter(
                LEVELS.MARKET, ATTRIBUTES.PRICE_TYPE_CODES, OPERATORS.INTERSECTS, 'LP')))
            additional_filter.append(simple_filter(LEVELS.OUTCOME, ATTRIBUTES.RUNNER_NUMBER, OPERATORS.IS_NOT_EMPTY))
            all_events = self.get_active_events_for_category(category_id=21, additional_filters=additional_filter,
                                                                all_available_events=True,gp=True)
            event_id = all_events[0]['event']['id']
            if self.brand == 'ladbrokes':
                url = f'https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.81/EventToOutcomeForEvent/{event_id}?referenceEachWayTerms=true&responseFormat=json'
            else:
                url = f'https://ss-aka-ori.coral.co.uk/openbet-ssviewer/Drilldown/2.81/EventToOutcomeForEvent/{event_id}?referenceEachWayTerms=true&responseFormat=json'
            events = do_request(method='GET', url=url)

            match_result_market = events['SSResponse']['children'][0]['event']['children'][0]['market']
            self.__class__.eachWayPlaces = match_result_market['eachWayPlaces']
            name = events['SSResponse']['children'][0]['event']['name']
            self.__class__.event_name = name.replace("|", "").split(' ', 1)[1]
            # ******** Getting Selection IDs ********
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes if 'outcome' in i}
            self.__class__.selection = list(all_selection_ids.keys())[0].replace("|", "")
            self.__class__.selection_id = list(all_selection_ids.values())[0]
            # ********** Getting refrenceEachWayTerms*******
            self.__class__.referenceEachWayTerms = next((i['referenceEachWayTerms']['places'] for i in outcomes if 'referenceEachWayTerms' in i), None)

        else:
            event1 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets_params)
            event2 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets_params)
            # getting type id
            self.__class__.type_id = event1[7]['event']['typeId']
            # getting type name
            self.__class__.expected_type_name = event1[7]['event']['typeName']
            # getting event name for type id
            self.__class__.event_names_for_type_id = list()
            self.event_names_for_type_id.append(event1[7]['event']['name'])
            self.event_names_for_type_id.append(event2[7]['event']['name'])
            # getting events for type id
            self.__class__.events_for_type_id = {event1[7]['event']['name']: event1[7],
                                                 event2[7]['event']['name']: event2[7]}
            limit = len(self.events_for_type_id) if len(self.events_for_type_id) < 2 else 2

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application_with_valid_credentials_with_precondition1(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition1
        EXPECTED: User is logged in
        """
        # Covered in above step

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.open_my_bets_open_bets()

    def test_004_verify_horse_racing_bets_which_offers_extra_place_in_open_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers Extra place in open tab
        EXPECTED: Extra place signposting should be displayed as per figma provided
        EXPECTED: ![](index.php?/attachments/get/6e47a14d-6a34-4a00-9205-72ffca9b8efa)
        """
        event_groups_section = self.site.open_bets.tab_content.accordions_list
        bet_name, bet = event_groups_section.get_bet(bet_type='SINGLE', number_of_bets=1)
        bet_legs = bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg=f'No one bet leg was found for bet: "{bet_name}"')
        bet_leg_name, bet_leg = list(bet_legs.items())[0]
        bet_leg_name = bet_leg_name.split(' - ')[0]
        self.assertEqual(bet_leg_name, self.selection,
                         msg=f'Single bet "{self.selection}" is not present in Open tab')
        self.assertTrue(bet_leg.has_extra_place_icon(), msg='Failed to display "Extra Place" icon in MY Bets >> Open tab >> Sports Tab ')
        actual_text = bet_leg.extra_place_icon_text.lower()
        expected_text = f'{self.eachWayPlaces} places instead of {self.referenceEachWayTerms}'

        self.assertEqual(actual_text,expected_text,
                        msg=f'Actual EP signposting is :{actual_text} is not same as Expected EP Signposting text in Open Tab >> sport Tab: {expected_text} ')

    def test_005_click_on_cash_out(self):
        """
        DESCRIPTION: Click on cash out
        EXPECTED: Cash out tab is opened
        """
        self.site.open_my_bets_cashout()
        event_groups_section = self.site.cashout.tab_content.accordions_list
        cashout_bet_name, cashout_bet = event_groups_section.get_bet(bet_type='SINGLE', number_of_bets=1)
        cashout_bet_legs = cashout_bet.items_as_ordered_dict
        self.assertTrue(cashout_bet_legs, msg=f'No one bet leg was found for bet: "{cashout_bet_name}"')
        cashout_bet_leg_name, self.__class__.cashout_bet_leg = list(cashout_bet_legs.items())[0]
        bet_leg_name = cashout_bet_leg_name.split(' - ')[0]
        self.assertEqual(bet_leg_name, self.selection,
                         msg=f'Single bet "{self.selection}" is not present in CashOut tab')

    def test_006_verify_horse_racing_bets_which_offers_extra_place_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers Extra place in Cash out tab
        EXPECTED: Extra place signposting should be displayed as per figma provided
        """
        self.assertTrue(self.cashout_bet_leg.has_extra_place_icon(), msg='Failed to display "Extra Place" icon in MY Bets >> Cashout Tab')
        actual_text = self.cashout_bet_leg.extra_place_icon_text.lower()
        expected_text = f'{self.eachWayPlaces} places instead of {self.referenceEachWayTerms}'

        self.assertEqual(actual_text, expected_text,
                         msg=f'Actual EP signposting is :{actual_text} is not same as Expected EP Signposting text in Cashout Tab: {expected_text} ')

        # Cashout  Horse Racing selection with EXTRA PLACE Signposting

        cashout_bet_name, cashout_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name,
            number_of_bets=1)
        cashout_bet.buttons_panel.full_cashout_button.click()
        cashout_amount = float(cashout_bet.buttons_panel.full_cashout_button.amount.value)
        confirmation_text = cashout_bet.buttons_panel.cashout_button.name
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + f' £{cashout_amount:.2f}'
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Expected confirmation text: "{expected_confirmation}" '
                             f'is not equal to actual: "{confirmation_text}"')
        self.assertTrue(cashout_bet.buttons_panel.has_full_cashout_button(timeout=8),
                        msg=f'CASHOUT button was not found on bet: "{cashout_bet_name}" section')
        cashout_bet.buttons_panel.full_cashout_button.click()
        cashout_bet.buttons_panel.cashout_button.click()

    def test_007_click_on_settled_tab(self):
        """
        DESCRIPTION: Click on settled tab
        EXPECTED: Settled tab is opened
        """
        self.site.open_my_bets_settled_bets()
        event_groups_section = self.site.settled_bets.tab_content.accordions_list
        settled_bet_name, settled_bet = event_groups_section.get_bet(bet_type='SINGLE', number_of_bets=1)
        settled_bet_legs = settled_bet.items_as_ordered_dict
        self.assertTrue(settled_bet_legs, msg=f'No one bet leg was found for bet: "{settled_bet_name}"')
        settled_bet_leg_name, settled_bet_leg = list(settled_bet_legs.items())[0]
        bet_leg_name = settled_bet_leg_name.split(' - ')[0]
        self.assertEqual(bet_leg_name, self.selection,
                         msg=f'Single bet "{self.selection}" is not present in Settled Tab')
        self.assertTrue(settled_bet_leg.has_extra_place_icon(),
                        msg='Failed to display "Extra Place" icon in MY Bets >> Settled Tab >> Sport Tab ')
        actual_text = settled_bet_leg.extra_place_icon_text.lower()
        expected_text = f'{self.eachWayPlaces} places instead of {self.referenceEachWayTerms}'

        self.assertEqual(actual_text, expected_text,
                         msg=f'Actual EP signposting is :{actual_text} is not same as Expected EP Signposting text in Settled Tab: {expected_text} ')

    def test_008_verify_horse_racing_bets_which_offers_extra_place_in_settled_tab(self):
        """
        DESCRIPTION: Verify Horse racing Bets which offers Extra place in Settled tab
        EXPECTED: Extra place signposting should be displayed as per figma provided
        EXPECTED: ![](index.php?/attachments/get/edc4d286-fd84-4006-9a6f-eff5e2a7b12f)
        """
        # Covered in above step
