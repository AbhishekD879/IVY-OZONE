import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - we are NOT ALLOWED to Place a Tote bets on HL and PROD environments
# @pytest.mark.hl
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.bet_receipt
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.desktop
@pytest.mark.critical
@vtest
class Test_C1641510_Verify_UK_Tote_Exacta_Bet_Placement(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C1641510
    NAME: Verify UK Tote Exacta Bet Placement
    DESCRIPTION: This test case verifies bet placement on Exacta UK tote
    PRECONDITIONS: * The User's account balance is sufficient to cover the bet stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * UK Tote feature is enabled in CMS
    PRECONDITIONS: * Exacta pool type is available for HR Event
    PRECONDITIONS: * User should have a Horse Racing event detail page open ("Tote" tab)
    PRECONDITIONS: * To load Totepool ON/OFF CMS config use System-configuration (https://coral-cms- **endpoint** .symphony-solutions.eu)
    PRECONDITIONS: **endpoint** can be found using devlog
    """
    keep_browser_open = True
    outcomes = []
    selection_outcomes = []

    def test_001_select_exacta_sub_tab_under_tote_tab(self):
        """
        DESCRIPTION: Select "Exacta" sub-tab under "Tote" tab
        EXPECTED: Exacta tab is selected
        EXPECTED: Exacta racecard is opened
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        self.__class__.eventID = event.event_id
        self.__class__.event_typename = event.event_typename.strip()
        self.__class__.bet_amount = event.min_total_stake
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.site.login(async_close_dialogs=False)

        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='UK Tote tab is not opened')
        self.__class__.event_off_time = self.site.racing_event_details.tab_content.event_off_times_list.selected_item
        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        exacta_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
        self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
        self.__class__.outcomes = list(section.pool.items_as_ordered_dict.items())
        self.assertTrue(self.outcomes, msg='No outcomes found')

    def test_002_select_1st_and_2nd_check_boxes_for_any_runners(self):
        """
        DESCRIPTION: Select "1st" and "2nd" check boxes for any runners
        EXPECTED: Selections are added to the Exacta tote bet builder
        EXPECTED: "ADD TO BETSLIP" button becomes enabled in the bet builder
        EXPECTED: Corresponding bet type name is shown in the bet builder
        """
        for index, (outcome_name, outcome) in enumerate(self.outcomes[:2]):
            self.__class__.selection_outcomes.append('%s %s' % (index + 1, outcome_name))
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        self.__class__.bet_builder = section.bet_builder
        self.assertTrue(self.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

    def test_003_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Tap "ADD TO BETSLIP" button
        EXPECTED: Tote exacta bets are added to betslip
        EXPECTED: Bet builder disappears
        """
        self.bet_builder.summary.add_to_betslip_button.click()
        self.__class__.betslip_counter = self.site.header.bet_slip_counter.counter_value

    def test_004_open_betslip_and_verify_the_exacta_tote_bet(self):
        """
        DESCRIPTION: Open betslip and verify the exacta tote bet
        EXPECTED: There is a "remove" button to remove the exacta tote bet from the betslip
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        selections_count = self.get_betslip_content().selections_count

        self.assertEqual(
            selections_count,
            self.betslip_counter,
            msg='BetSlip counter in section name "%s" and counter "%s" doesn\'t match' %
                (selections_count, self.betslip_counter))
        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.remove_button.is_displayed(), msg='Remove button was not found')
        self.__class__.stake = stake

    def test_005_verify_bet_details_for_exacta_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for exacta tote bet
        EXPECTED: There are the following details on exacta tote bet:
        EXPECTED: "Singles (1)" label in the section header
        EXPECTED: "Exacta Totepool"
        EXPECTED: "Exacta" bet type name
        EXPECTED: Both selections with correct order according to the selected check boxes
        EXPECTED: Example:
        EXPECTED: + **Exacta Totepool**
        EXPECTED: Exacta
        EXPECTED: **1. Dr Julius No**
        EXPECTED: **2. Newberry New**
        """
        self.assertEqual(self.stake.outcome_name, f'{vec.uk_tote.UEXA} {vec.uk_tote.TOTEPOOL.title()}',
                         msg='Actual outcome name "%s", expected "%s"' %
                             (self.stake.outcome_name, f'{vec.uk_tote.UEXA} {vec.uk_tote.TOTEPOOL.title()}'))
        self.assertEqual(self.stake.market_name, vec.uk_tote.STRAIGHT_EXACTA_BET,
                         msg='Actual bet type "%s", expected "%s"' %
                             (self.stake.market_name, vec.uk_tote.STRAIGHT_EXACTA_BET))
        selection_outcomes = self.stake.tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No UK Tote selections found')
        self.assertEqual(list(selection_outcomes.keys()), self.selection_outcomes)

    def test_006_expand_the_bet_and_verify_the_start_date_and_time_of_the_race(self):
        """
        DESCRIPTION: Verify the start date and time of the race
        EXPECTED: * Time of the race is shown when the bet is expanded
        EXPECTED: * Format is the following:
        EXPECTED: HH:MM <event name>
        EXPECTED: <event start date>
        EXPECTED: Example:
        EXPECTED: 14:20 Lingfield
        EXPECTED: Today
        """
        expected_event_title = '%s %s' % (self.event_off_time, self.event_typename)
        self.assertEqual(self.stake.event_name, expected_event_title, msg='Actual event title "%s", expected "%s"' %
                                                                          (self.stake.event_name, expected_event_title))
        self.assertEqual(self.stake.event_date, 'Today', msg='Actual event date "%s", expected "Today"'
                                                             % self.stake.event_date)

    def test_007_tap_the_remove_button(self):
        """
        DESCRIPTION: Tap the "remove" button
        EXPECTED: Bet is removed from the betslip
        """
        self.stake.remove_button.click()

    def test_008_select_2_any_check_boxes_and_tap_add_to_betslip_button_in_the_exacta_tote_bet_builder(self):
        """
        DESCRIPTION: Select 2 "Any" check boxes and tap "ADD TO BETSLIP" button in the Exacta tote bet builder
        EXPECTED: Tote Exacta bets are added to betslip
        EXPECTED: Bet builder disappears
        EXPECTED: Betslip is increased by 1 number indicator
        """
        self.__class__.selection_outcomes = []
        for outcome_name, outcome in self.outcomes[:2]:
            self.__class__.selection_outcomes.append('%s %s' % (outcome.runner_number, outcome_name))
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[2]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')
        bet_builder.summary.add_to_betslip_button.click()

    def test_009_verify_bet_details_for_exacta_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for exacta tote bet
        EXPECTED: There are the following details on exacta tote bet:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Exacta Totepool"
        EXPECTED: * "Exacta" bet type name
        EXPECTED: * Two selections with race card numbers next to them
        EXPECTED: Example:
        EXPECTED: + **Exacta Totepool**
        EXPECTED: Exacta
        EXPECTED: **<race card number> Dr Julius No**
        EXPECTED: **<race card number> Newberry New**
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles

        selections_count = self.get_betslip_content().selections_count

        self.assertEqual(
            selections_count,
            self.betslip_counter,
            msg='BetSlip counter in section name "%s" and counter "%s" doesn\'t match' %
                (selections_count, self.betslip_counter))
        stake_name, stake = list(singles_section.items())[0]
        self.__class__.stake = stake

        self.assertEqual(self.stake.outcome_name, f'{vec.uk_tote.UEXA} {vec.uk_tote.TOTEPOOL.title()}',
                         msg='Actual outcome name "%s", expected "%s"' %
                             (self.stake.outcome_name, f'{vec.uk_tote.UEXA} {vec.uk_tote.TOTEPOOL.title()}'))
        self.assertEqual(self.stake.market_name, vec.uk_tote.REVERSE_EXACTA_BET,
                         msg=f'Actual bet type "{self.stake.market_name}", expected "{vec.uk_tote.REVERSE_EXACTA_BET}"')
        selection_outcomes = self.stake.tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No UK Tote selections found')
        self.assertEqual(list(selection_outcomes.keys()), self.selection_outcomes)

    def test_010_repeat_step_7(self):
        """
        DESCRIPTION: Repeat step 7
        EXPECTED: Bet is removed from the betslip
        """
        self.test_007_tap_the_remove_button()

    def test_011_select_a_couple_of_any_check_boxes_and_tap_add_to_betslip_button_in_the_exacta_tote_bet_builder(self):
        """
        DESCRIPTION: Select a couple of "Any" check boxes and tap "ADD TO BETSLIP" button in the Exacta tote bet builder
        EXPECTED: Selections are added to betslip
        """
        self.__class__.selection_outcomes = []
        for outcome_name, outcome in self.outcomes[:4]:
            self.__class__.selection_outcomes.append('%s %s' % (outcome.runner_number, outcome_name))
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[2]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        section_name, section = list(sections.items())[0]
        bet_builder = section.bet_builder
        self.assertTrue(bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')
        bet_builder.summary.add_to_betslip_button.click()

    def test_012_verify_bet_details_for_exacta_tote_bet(self):
        """
        DESCRIPTION: Verify bet details for exacta tote bet
        EXPECTED: There are the following details on exacta tote bet:
        EXPECTED: * "Singles (1)" label in the section header
        EXPECTED: * "Exacta Totepool"
        EXPECTED: * ""x lines Combination Exacta" bet type name
        EXPECTED: * Corresponding selections with race card numbers next to them
        EXPECTED: Example:
        EXPECTED: + **Exacta Totepool**
        EXPECTED: 6 lines Combination Exacta
        EXPECTED: **<race card number> King Calvin**
        EXPECTED: **<race card number> Newberry New**
        EXPECTED: **<race card number> Helfire**
        EXPECTED: WHERE
        EXPECTED: # of lines inCombination Exacta is calculated by the formula:
        EXPECTED: No. of selections x next lowest number (eg. 5 Selections picked 5 x 4 = 20)
        """
        self.site.open_betslip()
        singles_section = self.get_betslip_sections().Singles
        selections_count = self.get_betslip_content().selections_count

        self.assertEqual(
            selections_count,
            self.betslip_counter,
            msg='BetSlip counter in section name "%s" and counter "%s" doesn\'t match' %
                (selections_count, self.betslip_counter))
        stake_name, stake = list(singles_section.items())[0]
        self.__class__.stake = stake

        self.assertEqual(self.stake.outcome_name, f'{vec.uk_tote.UEXA} {vec.uk_tote.TOTEPOOL.title()}',
                         msg='Actual outcome name "%s", expected "%s"' %
                             (self.stake.outcome_name, f'{vec.uk_tote.UEXA} {vec.uk_tote.TOTEPOOL.title()}'))
        self.assertEqual(self.stake.market_name, vec.uk_tote.COMBINATION_EXACTA_BET.format(number=12),
                         msg='Actual bet type "%s", expected "%s"' %
                             (self.stake.market_name, vec.uk_tote.COMBINATION_EXACTA_BET.format(number=12)))
        selection_outcomes = self.stake.tote_outcomes.items_as_ordered_dict
        self.assertTrue(selection_outcomes, msg='No UK Tote selections found')
        self.assertEqual(list(selection_outcomes.keys()), self.selection_outcomes)

    def test_013_verify_stake_field(self):
        """
        DESCRIPTION: Verify "Stake" field
        EXPECTED: User is able to set the stake using the betslip keyboard
        EXPECTED: User is able to modify stake
        EXPECTED: "Total stake" value changes accordingly
        """
        self.enter_stake_amount(stake=(self.stake.name, self.stake))
        total_stake = self.get_betslip_content().total_stake
        expected_total_stake = '%.2f' % (self.bet_amount * 12)
        self.assertEqual(total_stake, expected_total_stake,
                         msg='Actual total stake value "%s" is not equal expected "%s"'
                             % (total_stake, expected_total_stake))

    def test_014_verify_odds_and_estimated_returns(self):
        """
        DESCRIPTION: Verify "Odds" and "Estimated Returns"
        EXPECTED: Odds and Estimated Returns values are "N/A" for Tote bets
        """
        est_returns = self.stake.est_returns
        self.assertEqual(est_returns, 'N/A',
                         msg=f'Est returns is "{est_returns}" not "N/A"')

    def test_015_verify_total_est_returns(self):
        """
        DESCRIPTION: Verify "Total Est. Returns"
        EXPECTED: Total Est. Returns value is "N/A"
        """
        total_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertEqual(total_estimate_returns, 'N/A',
                         msg=f'Total Est returns is "{total_estimate_returns}" not "N/A"')

    def test_016_tap_the_bet_now_button(self):
        """
        DESCRIPTION: Tap the "Bet Now" button
        EXPECTED: Exacta Tote bet is successfully placed
        EXPECTED: Exacta Tote Bet receipt is shown
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
