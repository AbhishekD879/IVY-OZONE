import pytest
import tests
from collections import OrderedDict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.smoke
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.betslip
@pytest.mark.football
@pytest.mark.critical
@pytest.mark.login
@vtest
class Test_C29010_Making_Sport_Single_Selection(BaseBetSlipTest):
    """
    TR_ID: C29010
    NAME: Making <Sport> Single Selection
    DESCRIPTION: This test case verifies Making Single Selections on the <Sport> pages.
    DESCRIPTION: AUTOTEST [C11802800]
    PRECONDITIONS: To retrieve information from Site Server use steps:
    PRECONDITIONS: 1)To get class IDs and type IDs for <Sport>  use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?translationLang=LL?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M
    PRECONDITIONS: *   XX - Category ID (Sport id)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 2) To get a list of events for types use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForType/XXXX?translationLang=LL?simpleFilter=market.dispSortName:equals:ZZ&simpleFilter=market.siteChannels:contains:M&existsFilter=event:simpleFilter:market.isActive
    PRECONDITIONS: *   Notice XXXX is the type ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   ZZ - dispSortName specific value for each Sport, shows the primary marker (e.g. Football - MR, Tennis - HH)
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: 3) To get a list of events' details use link
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXX?translationLang=LL
    PRECONDITIONS: *   Notice XXXX is the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: Use attributes:
    PRECONDITIONS: *   **'name'** to see the event name
    PRECONDITIONS: *   **'className'** to see the region/country name
    PRECONDITIONS: *   **'typeName'** to see the league name
    PRECONDITIONS: *   **'name'** on the market level - to see the market name
    PRECONDITIONS: *   **'name' **on the outcome level - to see selection name
    PRECONDITIONS: *   **'livePriceNum'/'livePriceDen'** in the outcome level - to see odds for selection in fraction format
    PRECONDITIONS: *   **'priceDec'** in the outcome level - to see odds for selection in decimal format
    """
    keep_browser_open = True
    number_of_events = 1
    currency = '£'
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: TST2/STG2: Create football event, PROD: Find active football event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            # event 1
            self.__class__.eventID = self.event['event']['id']
            self.__class__.created_event_name = normalize_name(self.event['event']['name'])
            self.__class__.market_name = next((market['market']['name'] for market in self.event['event']['children']
                                               if 'Match Betting' in market['market']['templateMarketName']), '')

            outcomes = next(((market['market']['children']) for market in self.event['event']['children']
                             if 'Match Betting' in market['market']['templateMarketName'] and
                             market['market'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')

            # outcomeMeaningMinorCode: A - away, H - home, D - draw
            self.__class__.team1 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'H'), None)
            self.__class__.team2 = next((outcome['outcome']['name'] for outcome in outcomes if
                                         outcome['outcome'].get('outcomeMeaningMinorCode') and
                                         outcome['outcome']['outcomeMeaningMinorCode'] == 'A'), None)
            if not self.team1:
                raise SiteServeException('No Home team found')
            if not self.team2:
                raise SiteServeException('No Away team found')
            self.__class__.league1 = self.get_accordion_name_for_event_from_ss(event=self.event)

            self.__class__.expected_betslip_counter_value += 1

        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, self.__class__.team2 = event_params.team1, event_params.team2
            self.__class__.eventID = event_params.event_id
            self.__class__.created_event_name = '%s v %s' % (event_params.team1, event_params.team2)
            self.__class__.expected_betslip_counter_value += 1
            self.__class__.league1 = tests.settings.football_autotest_league
            self.__class__.outcome_price = self.ob_config.event.prices['odds_home']
            self.__class__.market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')

    def test_001_login(self):
        """
        DESCRIPTION: Login as user that has enough funds to place a bet
        EXPECTED: Logged in as a appropriate user
        """
        self.site.login(async_close_dialogs=False, timeout_close_dialogs=5)

        self.site.close_all_dialogs()
        self.site.toggle_quick_bet()

    def test_002_tap_sport_icon_on_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>' icon on the Sports Menu Ribbon
        EXPECTED: *   <Sport> Landing Page is opened
        EXPECTED: *   'Today' tab is opened by default
        """
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')

    def test_003_add_single_selection_to_bet_slip(self):
        """
        DESCRIPTION: Add single selection to bet slip
        EXPECTED: Bet indicator displays 1.
        """
        if self.site.root_app.has_timeline_overlay_tutorial(timeout=2, expected_result=True):
            self.site.timeline_tutorial_overlay.close_icon.click()
        event = self.get_event_from_league(event_id=self.eventID,
                                           section_name=self.league1)
        output_prices = event.get_active_prices()
        self.assertTrue(output_prices,
                        msg=f'Could not find output prices for created event "{self.created_event_name}"')
        self.__class__.selection_name = self.team1
        selection_price = output_prices.get(self.team1)
        self.assertTrue(selection_price, msg=f'Bet button for "{self.team1}" was not found')
        selection_price.click()
        self.site.close_all_dialogs()
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.assertTrue(selection_price.is_selected(timeout=2),
                        msg=f'Bet button "{self.selection_name}" is not active after selection')

    def test_004_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: *   Added selection is present
        EXPECTED: *   Section is named 'Singles (1)' **From OX99** [Section is named Your Selections]
        EXPECTED: *   'Stake' box is focused by default
        EXPECTED: *   Numeric keyboard with quick stake buttons are shown above disabled 'BET NOW'/LOG IN & BET' button **From OX99** Numeric keyboard with quick stake buttons are shown above 'Total Satke' and 'Estimated Returns'
        """
        betslip_counter = self.site.header.bet_slip_counter.counter_value

        self.verify_betslip_counter_change(expected_value=self.expected_betslip_counter_value)

        self.site.open_betslip()
        self.site.close_all_dialogs(timeout=3)
        singles_section = self.get_betslip_sections().Singles

        betslip = self.get_betslip_content()
        section_name = betslip.your_selections_label
        self.assertEqual(section_name, vec.betslip.YOUR_SELECTIONS,
                         msg=f'Betslip section name "{section_name}" is not the same as expected "{vec.betslip.YOUR_SELECTIONS}"')
        selections_count = betslip.selections_count
        self.assertEqual(selections_count, betslip_counter,
                         msg=f'BetSlip counter in section name "{selections_count}" '
                             f'and counter "{selections_count}" doesn\'t match')

        self.__class__.stake = singles_section.get(self.team1)
        self.assertTrue(self.stake, msg=f'"{self.team1}" stake was not found in "{singles_section.keys()}"')

    def test_005_verify_selection_displaying(self):
        """
        DESCRIPTION: Verify selection displaying
        EXPECTED: - Selection is displayed as collapsible/expandable section within the betslip
        EXPECTED: - it is possible to expand/collapse selection information by clicking '+' sign
        EXPECTED: **From OX99** [Section is displayed as expandable section]
        """
        pass  # cannot verify directly, indirectly will be verified in the next steps

    def test_006_verify_selection_information_in_collapse_statefrom_ox99_not_actual(self):
        """
        DESCRIPTION: Verify selection information in collapse state
        DESCRIPTION: **From OX99** [Not actual]
        EXPECTED: The following info is displayed on the Bet Slip:
        EXPECTED: 1.  Selection name (**'name'** attribute on the outcome level)
        EXPECTED: 2.  Market type (**'name'** attribute on the market level)
        EXPECTED: 3.  Selection odds ('livePriceNum'/'livePriceDen' attributes in fraction format OR 'price Dec' in decimal format)
        """
        pass  # OX 99 part is verified in the next step

    def test_007_verify_selection_information_in_expanded_state(self):
        """
        DESCRIPTION: Verify selection information in expanded state
        EXPECTED: * The following additional info is shown:
        EXPECTED: **From OX99**
        EXPECTED: [- selection name
        EXPECTED: - price
        EXPECTED: - market name
        EXPECTED: - event name]
        EXPECTED: 'estimated returns' / 'potential returns' for that individual bet
        EXPECTED: stake box
        EXPECTED: 1.  Event name ( **'name'** attribute on event level)
        EXPECTED: - Format for Sports: 'Team_A v/vs Team_B'
        """
        event_name = self.stake.event_name
        self.assertEqual(event_name, self.created_event_name,
                         msg=f'Selection name "{event_name}" is not the same as expected "{self.created_event_name}"')
        outcome_name = self.stake.outcome_name
        self.assertEqual(outcome_name, self.selection_name,
                         msg=f'Selection name "{outcome_name}" is not the same as expected "{self.selection_name}"')
        market_name = self.stake.market_name
        self.assertEqual(market_name, self.market_name,
                         msg=f'Market name "{market_name}" is not the same as expected "{self.market_name}"')
        if tests.settings.backend_env == 'prod':  # this is to handle prices that might change
            outcomes = next((market['market']['children'] for market in self.event['event']['children']
                             if 'Match Betting' in market['market']['templateMarketName']), None)
            if outcomes is None:
                raise SiteServeException('There are no available outcomes')

            self.__class__.initial_prices = OrderedDict([(outcome['outcome']['name'],
                                                          f'{outcome["outcome"]["children"][0]["price"]["priceNum"]}/'
                                                          f'{outcome["outcome"]["children"][0]["price"]["priceDen"]}')
                                                         for outcome in outcomes])
            self.__class__.outcome_price = self.initial_prices[self.team1]
        odds = self.stake.odds
        self.assertEqual(odds, self.outcome_price,
                         msg=f'Outcome "{outcome_name}" price "{odds}" is not the same as expected "{self.outcome_price}"')
        self.assertTrue(self.stake.est_returns_label, msg='"Est. Returns" field is not displayed')
        self.assertTrue(self.stake.est_returns, msg='"Est. Returns" field is not displayed')
        label = vec.betslip.ESTIMATED_RESULTS if self.brand == 'bma' else vec.betslip.POTENTIAL_RESULTS
        self.assertEqual(self.stake.est_returns_label.text, label,
                         msg=f'Incorrect label of "Est. Returns" field\n'
                             f'Actual: {self.stake.est_returns_label.text}\nExpected: "{label}"')
        self.assertEqual(float(self.stake.est_returns), 0.00,
                         msg=f'Est. Returns amount is: "{self.stake.est_returns}" but should be "0.00")')

    def test_008_tap_stake_box(self):
        """
        DESCRIPTION: Tap 'Stake' box
        EXPECTED: *   Box becomes focused
        EXPECTED: *   Numeric keyboard with quick stake buttons are shown above disabled 'BET NOW'/LOG IN & BET' button **From OX99** Numeric keyboard with quick stake buttons are shown above 'Total Satke' and 'Estimated Returns'
        """
        self.stake.amount_form.input.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.stake.amount_form.is_active(), msg='Stake input field was not focused')
            self.assertTrue(
                self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard shown', timeout=3),
                msg='Betslip keyboard is not shown')

    def test_009_change_focus_on_bet_slip_slide_tap_somewhere_outside_stake_box(self):
        """
        DESCRIPTION: Change focus on Bet Slip slide (tap somewhere outside 'Stake' box)
        EXPECTED: *   'Stake' box is NOT focused and '<currency symbol> 0.00' is shown within box
        EXPECTED: *   Numeric keyboard is NOT shown
        """
        if self.device_type == 'mobile':
            keyboard = self.get_betslip_content().keyboard
            keyboard.enter_amount_using_keyboard(value='enter')
            self.assertFalse(self.stake.amount_form.is_active(expected_result=False),
                             msg='Stake input box is focused')
            result = self.get_betslip_content().keyboard.is_displayed(name='Betslip keyboard to hide',
                                                                      expected_result=False,
                                                                      timeout=3)
            self.assertFalse(result, msg='Betslip keyboard is not shown')

    def test_010_tap_stake_box_and_add_amount_to_bet_using_numeric_keyboard_or_quick_stake(self):
        """
        DESCRIPTION: Tap 'Stake' box and add amount to bet using numeric keyboard or quick stake
        EXPECTED: The total wager for the bet is entered. The following fields are changed due to selected stake:
        EXPECTED: *   Value in the **Stake** box
        EXPECTED: *   **Estimated Returns** (in format XX.XX)
        EXPECTED: *   **Total Stake** (in format XX.XX)
        EXPECTED: *   **Total Est. Returns** (in format XX.XX)
        """
        old_est_returns = self.stake.est_returns
        self.stake.amount_form.input.click()
        if self.device_type == 'mobile':
            self.assertTrue(self.stake.amount_form.is_active(), msg='Stake input field was not focused')
            keyboard = self.get_betslip_content().keyboard
            keyboard.enter_amount_using_keyboard(value=0.05)
        else:
            self.stake.amount_form.enter_amount('0.05')
        result = wait_for_result(lambda: self.stake.est_returns != old_est_returns,
                                 name='Estimated Returns value to change',
                                 timeout=2)
        self.assertTrue(result, msg=f'"Est. Returns" field value "{self.stake.est_returns}" has not changed after stake was entered')

        total_stake = self.get_betslip_content().total_stake
        self.assertNotEqual(total_stake, '0.00',
                            msg=f'"Total Stake" field value "{total_stake}" has not changed after stake was entered')

    def test_011_close_betslip_for_mobile_only(self):
        """
        DESCRIPTION: Close Betslip (**for Mobile only**)
        EXPECTED: Betslip overlay is closed
        """
        if self.device_type == 'mobile':
            self.get_betslip_content().close_button.click()
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=3), msg='Betslip was not closed')

    def test_012_go_to_betslip_again(self):
        """
        DESCRIPTION: Go to Betslip  again
        EXPECTED: *  Selection and entered stake are remembered
        EXPECTED: *  Numeric keyboard with quick stake buttons are shown above 'BET NOW'/LOG IN & BET' button **From OX99** Numeric keyboard with quick stake buttons are shown above 'Total Satke' and 'Estimated Returns'
        """
        self.site.open_betslip()
        self.site.close_all_dialogs()
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section.get(self.team1)
        self.assertTrue(stake, msg='"%s" stake was not found' % self.team1)
        self.test_011_close_betslip_for_mobile_only()
