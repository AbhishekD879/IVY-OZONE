import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2  # # Need to update script for QA2 once QA2 envs are available
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C28488_Verify_selection_data_and_placing_a_bet(BaseBetSlipTest):
    """
    TR_ID: C28488
    NAME: Verify selection data and placing a bet
    DESCRIPTION: This test case verifies selection data and placing a bet.
    PRECONDITIONS: 1) http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) User is logged in
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create/find test event
        """
        event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
        self.__class__.eventID = event['event']['id']
        self.__class__.event_name = f"{normalize_name(event['event']['name'])}"
        self.__class__.market_name = next((market['market']['name'] for market in event['event']['children']
                                           if 'Match Betting' in market['market']['templateMarketName']), '')

        self.__class__.outcomes = next(((market['market']['children']) for market in event['event']['children']
                                        if 'Match Betting' in market['market']['templateMarketName'] and
                                        market['market'].get('children')), None)
        if self.outcomes is None:
            raise SiteServeException('There are no available outcomes')

        # outcomeMeaningMinorCode: A - away, H - home, D - draw
        self.__class__.team1 = next((outcome['outcome']['name'] for outcome in self.outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') and
                                     outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
        self.__class__.team2 = next((outcome['outcome']['name'] for outcome in self.outcomes if
                                     outcome['outcome'].get('outcomeMeaningMinorCode') and
                                     outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)
        if not self.team1:
            raise SiteServeException('No Home team found')
        if not self.team2:
            raise SiteServeException('No Aways team found')
        self._logger.info(f'*** Football event with event id "{self.eventID}"')
        self.__class__.section_name = self.expected_market_sections.match_result

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_tap_sporticon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>'  icon on the Sports Menu Ribbon
        EXPECTED: 'Sport' Landing Page is opened
        """
        # Covered in Step# 3

    def test_003_tap_event_name_or_more_link_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name or 'More' link on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')

    def test_004_go_to_verified_market_section(self):
        """
        DESCRIPTION: Go to verified Market section
        EXPECTED: It is possible to collapse/expand Market sections by tapping the section's header
        """
        markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets_list, msg='Markets list is not present')

        if self.device_type == 'desktop' or self.brand == 'ladbrokes':
            self.__class__.market = markets_list.get(self.section_name.title())
        else:
            self.__class__.market = markets_list.get(self.section_name.upper())
        self.assertTrue(self.market, msg='Can not find Match Result section')

        self.market.collapse()
        self.assertFalse(self.market.is_expanded(), msg='Cannot collapse the section "%s"' % self.section_name)
        self.market.expand()
        self.assertTrue(self.market.is_expanded(), msg='Cannot expand the section "%s"' % self.section_name)

    def test_005_go_to_verified_selection_section(self):
        """
        DESCRIPTION: Go to verified selection section
        EXPECTED: Selection section is displayed within Market section
        """
        self.__class__.outcomes_ui = self.market.outcomes.items_as_ordered_dict
        self.assertTrue(self.outcomes, msg='No outcomes are shown for Match Result market')

    def test_006_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: Selection name corresponds to '**name**' attribute on the outcome level for verified Market
        """
        if self.brand == 'bma':
            expected_selection_names = [self.team1, 'Draw', self.team2]
        else:
            expected_selection_names = [self.team1.upper(), 'DRAW', self.team2.upper()]
        actual_selection_names = list(self.outcomes_ui.keys())
        self.assertEqual(expected_selection_names, actual_selection_names,
                         msg=f'Selection name "{expected_selection_names}" is not the same as expected "{actual_selection_names}"')

    def test_007_verify_data_of_priceodds_buttons_in_fractional_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in fractional format
        EXPECTED: *   'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        for outcome_name, outcome in self.outcomes_ui.items():
            self.assertRegexpMatches(outcome.bet_button.name, self.fractional_pattern,
                                     msg=f'Stake odds value "{outcome.bet_button.name}" not match fractional pattern: "{self.fractional_pattern}"')

    def test_008_verify_data_of_priceodds_buttons_in_decimal_format(self):
        """
        DESCRIPTION: Verify data of Price/Odds buttons in decimal format
        EXPECTED: *   'Price/Odds' corresponds to the **priceDec **if **eventStatusCode="A"**
        EXPECTED: *   Disabled **'S'** button is displayed instead of prices if **eventStatusCode="S"**
        """
        self.navigate_to_page("Homepage")
        self.site.login()
        # Changing the odd format to decimal from setting form
        result = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(result, msg='Odds format is not changed to Decimal')

        self.test_003_tap_event_name_or_more_link_on_the_event_section()
        self.test_004_go_to_verified_market_section()
        self.test_005_go_to_verified_selection_section()
        for outcome_name, outcome in self.outcomes_ui.items():
            self.assertRegexpMatches(outcome.bet_button.name, self.decimal_pattern,
                                     msg=f'Stake odds value "{outcome.bet_button.name}" not match decimal pattern: "{self.decimal_pattern}"')

    def test_009_selectunselect_same_priceodds_button(self):
        """
        DESCRIPTION: Select/unselect same Price/Odds button
        EXPECTED: Button is highlighted/unhighlighted respectively
        """
        outcome_name, outcome = list(self.outcomes_ui.items())[0]
        self.assertFalse(outcome.bet_button.is_selected(expected_result=False),
                         msg=f'Bet button "{outcome_name}" is highlighted')
        outcome.bet_button.click()
        self.site.wait_splash_to_hide()
        self.site.add_first_selection_from_quick_bet_to_betslip()
        self.assertTrue(outcome.bet_button.is_selected(), msg=f'Bet button "{outcome_name}" is not highlighted')

    def test_010_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: Bet indicator displays 1.
        """
        # Covered in step# 10

    def test_011_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: The bet is be present
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No bets found')
        # self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        _, self.__class__.stake = list(singles_section.items())[0]

    def test_012_verify_selection(self):
        """
        DESCRIPTION: Verify selection
        EXPECTED: The following info is displayed on the Betslip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Event start time and event name (**'startTime'** and event **'name'** attributes)
        EXPECTED: 4.  Selection odds (**'PriceNum'/'PriceDen' **attributes in fraction format or **'price Dec'** in decimal format)
        """
        outcome_name = self.stake.outcome_name
        self.assertEqual(outcome_name, self.team1,
                         msg=f'Selection name "{outcome_name}" is not the same as expected "{self.team1}"')

        market_name = self.stake.market_name
        self.assertEqual(market_name, self.market_name,
                         msg=f'Market name "{market_name}" is not the same as expected "{self.market_name}"')

        event_name = self.stake.event_name
        self.assertEqual(event_name, self.event_name,
                         msg=f'Selection name "{event_name}" is not the same as expected "{self.event_name}"')

    def test_013_add_amount_to_bet_using_stake_field_or_quick_stake_buttons(self):
        """
        DESCRIPTION: Add amount to bet using Stake field or Quick Stake buttons
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   **Total Stake**
        EXPECTED: *   **Total Est. Returns**
        """
        self.assertTrue(self.stake.est_returns_label, msg='"Est. Returns" field is not displayed')
        self.assertTrue(self.stake.est_returns, msg='"Est. Returns" field is not displayed')
        label = vec.betslip.ESTIMATED_RESULTS if self.brand == 'bma' else vec.betslip.POTENTIAL_RESULTS
        self.assertEqual(self.stake.est_returns_label.text, label,
                         msg=f'Incorrect label of "Est. Returns" field\n'
                             f'Actual: {self.stake.est_returns_label.text}\nExpected: "{label}"')
        self.assertEqual(float(self.stake.est_returns), 0.00,
                         msg=f'Est. Returns amount is: "{self.stake.est_returns}" but should be "0.00")')

        old_est_returns = self.stake.est_returns
        self.stake.amount_form.input.click()
        self.stake.amount_form.input.value = self.bet_amount

        result = wait_for_result(lambda: self.stake.est_returns != old_est_returns,
                                 name='Estimated Returns value to change',
                                 timeout=2)
        self.assertTrue(result,
                        msg=f'"Est. Returns" field value "{self.stake.est_returns}" has not changed after stake was entered')

        total_stake = self.get_betslip_content().total_stake
        self.assertNotEqual(total_stake, '0.00',
                            msg=f'"Total Stake" field value "{total_stake}" has not changed after stake was entered')

    def test_014_tapbet_now_button(self):
        """
        DESCRIPTION: Tap **'Bet Now**' button
        EXPECTED: *   Bet is placed successfully
        EXPECTED: *   Confirmation message is shown
        """
        self.get_betslip_content().bet_now_button.click()
        self.assertTrue(self.site.is_bet_receipt_displayed(), msg='Bet Receipt is not displayed.')
