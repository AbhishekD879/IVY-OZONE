import pytest

from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.betslip
@pytest.mark.quick_bet
@pytest.mark.bet_placement
@pytest.mark.bet_receipt
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.login
@vtest
class Test_C11366890_Verify_bet_placement_on_To_Finish_market(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C11366890
    NAME: Verify bet placement on 'To Finish' market
    DESCRIPTION: This test case verifies bet placement on 'To Finish' market
    PRECONDITIONS: 1) Horse Racing events with To Finish '2ND / 3RD / 4TH' markets (templateMarketName='To Finish Second', templateMarketName="To Finish Third", templateMarketName="To Finish Fourth") are available
    PRECONDITIONS: 2) To observe LiveServe changes make sure:
    PRECONDITIONS: - LiveServ updates is checked on 'Class' and 'Type' levels in TI
    PRECONDITIONS: - 'Bet In Play List' flag is checked on 'Event' level in TI
    PRECONDITIONS: - 'Bet in Running' is checked on 'Market' level in TI
    PRECONDITIONS: 3) To get information for an event uses the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    markets = [
        ('to_finish_second',),
        ('to_finish_third',),
        ('to_finish_fourth',)
    ]
    price = '1/2'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        """
        event_params = self.ob_config.add_UK_racing_event(markets=self.markets, number_of_runners=3, sp=False,
                                                          lp_prices={0: self.price,
                                                                     1: self.price,
                                                                     2: self.price})
        self.__class__.eventID = event_params.event_id
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False

    def test_001_login(self):
        """
        DESCRIPTION: Login
        EXPECTED: User is logged in
        """
        self.site.login()

    def test_002_navigate_to_edp_and_open_to_finish_market_tab(self):
        """
        DESCRIPTION: Navigate to EDP and open 'To Finish' market tab
        EXPECTED: 'To Finish' market tab is opened
        """
        self.__class__.tab_name = vec.racing.TO_FINISH_MARKET_NAME
        self.__class__.balance = self.site.header.user_balance

        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        market_tabs = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.items_as_ordered_dict
        self.assertTrue(market_tabs, msg='No market tabs found')
        self.assertIn(self.tab_name, market_tabs.keys(),
                      msg=f'"{self.tab_name}" tab was not found in the tabs list "{market_tabs.keys()}"')

        self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(self.tab_name)

    def test_003_for_mobile_click_on_a_bet_button_of_one_of_the_selections(self, fractional=True):
        """
        DESCRIPTION: For mobile:
        DESCRIPTION: Click on a bet button of one of the selections
        EXPECTED: Quick bet overlay is opened
        EXPECTED: Odds are shown in fractional format
        """
        if self.is_mobile:
            event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(event_markets_list, msg='No event market tabs found')
            self.assertIn(self.tab_name, event_markets_list.keys(),
                          msg=f'"{self.tab_name}" market was not found in the '
                              f'list of tabs "{event_markets_list.keys()}"')

            self.__class__.event_market = event_markets_list[self.tab_name]

            outcomes = self.event_market.items_as_ordered_dict
            self.assertTrue(outcomes, msg='No outcomes found')

            self.__class__.outcome = list(outcomes.values())[0]
            self.outcome.bet_button.click()

            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
            pattern = self.fractional_pattern if fractional else self.decimal_pattern
            self.assertRegexpMatches(self.site.quick_bet_panel.selection.content.odds_value, pattern,
                                     msg=f'Odds "{self.site.quick_bet_panel.selection.content.odds_value}" '
                                         f'does not match pattern "{pattern}"')

    def test_004_for_mobile_enter_stake_and_place_bet(self):
        """
        DESCRIPTION: For mobile:
        DESCRIPTION: Enter stake and place bet
        EXPECTED: Bet is placed. Bet receipt is displayed
        EXPECTED: Balance is decreased by stake amount
        """
        if self.is_mobile:
            self.site.quick_bet_panel.selection.content.amount_form.input.value = self.bet_amount
            self.site.quick_bet_panel.place_bet.click()

            bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed()
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')

            self.verify_user_balance(expected_user_balance=self.balance - self.bet_amount)

    def test_005_click_on_a_bet_button_of_one_of_the_selections(self):
        """
        DESCRIPTION: Click on a bet button of one of the selections
        EXPECTED: For mobile:
        EXPECTED: Quick bet overlay is opened
        EXPECTED: For desktop:
        EXPECTED: Selection is added to the Betslip
        """
        if self.is_mobile:
            self.site.quick_bet_panel.close()
            self.outcome.bet_button.click()
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not shown')
        else:
            event_markets_list = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
            self.assertTrue(event_markets_list, msg='No event market tabs found')
            self.assertIn(self.tab_name, event_markets_list.keys(),
                          msg=f'"{self.tab_name}" market was not found in the '
                              f'list of tabs "{event_markets_list.keys()}"')

            self.__class__.event_market = event_markets_list[self.tab_name]

            outcomes = self.event_market.items_as_ordered_dict
            self.assertTrue(outcomes, msg='No outcomes found')

            self.__class__.outcome = list(outcomes.values())[0]
            self.outcome.bet_button.click()

    def test_006_for_mobile_click_on_add_to_betslip_button(self):
        """
        DESCRIPTION: For mobile:
        DESCRIPTION: Click on 'Add to Betslip' button
        EXPECTED: Quick bet overlay is closed
        EXPECTED: Betslip counter is 1
        """
        if self.is_mobile:
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')

            self.verify_betslip_counter_change(expected_value=1)

    def test_007_open_betslip_enter_stake_and_press_bet_now(self, fractional=True):
        """
        DESCRIPTION: Open betslip, enter stake and press 'Bet Now'
        EXPECTED: Bet receipt is displayed
        EXPECTED: Odds are shown in fractional format
        EXPECTED: Balance is decreased by stake amount
        """
        self.__class__.balance = self.site.header.user_balance
        self.site.open_betslip()

        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No BetReceipt sections found')

        single_section = sections.get(vec.betslip.BETSLIP_SINGLES_NAME)
        self.assertTrue(single_section, msg='No Betslip sections found')

        stakes = single_section.items_as_ordered_dict
        self.assertTrue(stakes, msg='No stakes found')
        single = list(stakes.values())[0]
        pattern = self.fractional_pattern if fractional else self.decimal_pattern
        self.assertRegexpMatches(single.odds, pattern,
                                 msg=f'Odds "{single.odds}" does not match pattern "{pattern}"')

        self.verify_user_balance(expected_user_balance=self.balance - self.bet_amount)

        self.site.bet_receipt.close_button.click()

    def test_008_change_price_format_to_decimal_in_my_account_settings_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Change price format to Decimal in My Account > Settings and repeat steps 2-7
        """
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')

        self.test_002_navigate_to_edp_and_open_to_finish_market_tab()
        self.test_003_for_mobile_click_on_a_bet_button_of_one_of_the_selections(fractional=False)
        self.test_004_for_mobile_enter_stake_and_place_bet()
        self.test_005_click_on_a_bet_button_of_one_of_the_selections()
        self.test_006_for_mobile_click_on_add_to_betslip_button()
        self.test_007_open_betslip_enter_stake_and_press_bet_now(fractional=False)
