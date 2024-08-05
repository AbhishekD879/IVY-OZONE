import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.user_account
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C146509_Format_of_Price_Odds_on_Cash_Out_tab(BaseCashOutTest, BaseRacing):
    """
    TR_ID: C146509
    NAME: Format of Price/Odds on 'Cash Out' tab
    DESCRIPTION: This test case verifies Price/Odds in decimal and fractional format
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has placed Singles and Multiple bets on events where Cash Out offer is available
    """
    keep_browser_open = True
    events = None
    single_bet_event_names, multiples_bet_event_names = None, None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        DESCRIPTION: Login
        DESCRIPTION: Place a bet
        """
        # Sport events
        self.__class__.events = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        selection_ids = [event.selection_ids[event.team1] for event in self.events]
        event = self.events[0]
        self.__class__.single_bet_event_names = [f'{event.event_name} {event.local_start_time}']

        # Racing events
        racing_event1 = self.ob_config.add_UK_racing_event(number_of_runners=1, cashout=True)
        racing_event2 = self.ob_config.add_UK_racing_event(number_of_runners=1, cashout=True)
        start_time1_local = self.convert_time_to_local(date_time_str=racing_event1.event_date_time)
        start_time2_local = self.convert_time_to_local(date_time_str=racing_event2.event_date_time)

        racing_selection_ids = (list(racing_event1.selection_ids.values())[0],
                                list(racing_event2.selection_ids.values())[0])
        racing_event1_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time1_local}'
        racing_event2_name = f'{self.horseracing_autotest_uk_name_pattern} {start_time2_local}'
        self.__class__.racing_single_bet_event_names = [racing_event1_name]
        self.__class__.racing_multiples_bet_event_names = [racing_event1_name, racing_event2_name]

        username = tests.settings.betplacement_user
        self.site.login(username=username)

        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(selection_ids=racing_selection_ids)
        self.place_bet_on_all_available_stakes()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.navigate_to_page(name='/')

    def test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Cash Out' tab on 'My Bets' page / 'Bet Slip' widget
        EXPECTED: 'Cash Out' tab opened
        """
        self.site.open_my_bets_cashout()

    def test_002_verify_price_odds_in_fractional_format_of_single_selection(self):
        """
        DESCRIPTION: Verify Price/Odds in fractional format of Single selection
        EXPECTED: In fractional format Price/Odds corresponds to: *'priceNum'/'priceDen'* attributes (i.e.9/1)
        """
        self.__class__.cashout = self.site.cashout.tab_content.accordions_list
        single_bet_name, single_bet = self.cashout.get_bet(bet_type='SINGLE', event_names=self.single_bet_event_names)
        single_betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(single_betlegs, msg=f'No betlegs found for {self.single_bet_event_names}')
        [self.assertRegexpMatches(betleg.odds_value, self.fractional_pattern)
         for betleg_name, betleg in single_betlegs.items()]

    def test_003_verify_price_odds_in_fractional_format_of_multiples_selection(self):
        """
        DESCRIPTION: Verify Price/Odds in fractional format of Multiples selection
        EXPECTED: In fractional format Price/Odds corresponds to: *'priceNum'/'priceDen'* attributes (i.e.9/1)
        """
        self.__class__.multiples_bet_event_names = [event.event_name for event in self.events]
        multiples_bet_name, multiples_bet = self.cashout.get_bet(event_names=self.multiples_bet_event_names)
        multiples_betlegs = multiples_bet.items_as_ordered_dict
        self.assertTrue(multiples_betlegs, msg=f'No betlegs found for {multiples_bet_name}')

        [self.assertRegexpMatches(betleg.odds_value, self.fractional_pattern)
         for betleg_name, betleg in multiples_betlegs.items()]

    def test_004_go_to_settings_switch_odds_format_to_decimal_and_go_back_to_cashout_page(self):
        """
        DESCRIPTION: Go to Settings, switch Odds format to Decimal and go back to Cashout page
        EXPECTED: Odds are shown in Decimal format
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.test_001_navigate_to_cash_out_tab_on_my_bets_page_bet_slip_widget()

    def test_005_verify_price_odds_in_decimal_format_of_single_selection(self):
        """
        DESCRIPTION: Verify Price/Odds in decimal format of Single selection
        EXPECTED: In decimal format Price/Odds corresponds to: *'priceDec'* attribute (i.e.10)
        """
        self.__class__.cashout = self.site.cashout.tab_content.accordions_list

        single_bet_name, single_bet = self.cashout.get_bet(bet_type='SINGLE', event_names=self.single_bet_event_names)
        single_betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(single_betlegs, msg=f'No betlegs found for {self.single_bet_event_names}')
        [self.assertRegexpMatches(betleg.odds_value, self.decimal_pattern)
         for betleg_name, betleg in single_betlegs.items()]

    def test_006_verify_price_odds_in_decimal_format_of_multiple_selection(self):
        """
        DESCRIPTION: Verify Price/Odds in decimal format of Single selection
        EXPECTED: In decimal format Price/Odds corresponds to: *'priceDec'* attribute (i.e.10)
        """
        multiples_bet_name, multiples_bet = self.cashout.get_bet(event_names=self.multiples_bet_event_names)
        multiples_betlegs = multiples_bet.items_as_ordered_dict
        self.assertTrue(multiples_betlegs, msg=f'No betlegs found for {multiples_bet_name}')

        [self.assertRegexpMatches(betleg.odds_value, self.decimal_pattern)
         for betleg_name, betleg in multiples_betlegs.items()]

    def test_007_verify_sp_price_displaying_for_single_racing_selections(self):
        """
        DESCRIPTION: Verify SP price displaying for Single Racing selections
        EXPECTED: **SP** is shown next to 'Odds:' label
        """
        self.__class__.cashout = self.site.cashout.tab_content.accordions_list

        single_bet_name, single_bet = self.cashout.get_bet(bet_type='SINGLE',
                                                           event_names=self.racing_single_bet_event_names)
        single_betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(single_betlegs, msg=f'No betlegs found for {single_bet_name}')
        [self.assertEqual(betleg.odds_value, 'SP', msg=f'Price is not SP it is {betleg.odds_value}')
         for betleg_name, betleg in single_betlegs.items()]

    def test_008_verify_sp_price_displaying_for_racing_selections_in_multiple_bet(self):
        """
        DESCRIPTION: Verify SP price displaying for Racing selections in Multiple bet
        EXPECTED: **SP** is shown next to 'Odds:' label
        """
        multiples_bet_name, multiples_bet = self.cashout.get_bet(event_names=self.racing_multiples_bet_event_names)
        multiples_betlegs = multiples_bet.items_as_ordered_dict
        self.assertTrue(multiples_betlegs, msg=f'No betlegs found for {multiples_bet_name}')

        [self.assertEqual(betleg.odds_value, 'SP', msg=f'Price is not SP it is {betleg.odds_value}')
         for betleg_name, betleg in multiples_betlegs.items()]
