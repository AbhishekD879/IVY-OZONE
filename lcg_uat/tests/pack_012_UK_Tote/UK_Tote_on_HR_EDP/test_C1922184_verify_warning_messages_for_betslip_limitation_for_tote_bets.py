import voltron.environments.constants as vec
from random import uniform

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.uk_tote
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.high
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C1922184_Verify_warning_messages_for_Betslip_limitation_for_Tote_bets(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C1922184
    NAME: Verify warning messages for Betslip limitation for Tote bets
    DESCRIPTION: This test case verifies warning messages for Tote bets in the betslip, which appear in the following cases:
    DESCRIPTION: when user tries to place a bet with stake below minimum stake
    DESCRIPTION: when user tries to place a bet with stake above maximum stake
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is sufficient to cover the bet stake
    PRECONDITIONS: * Overask is disabled for the user in TI tool
    PRECONDITIONS: * User has added UK Tote bet (any pool type) to the betslip
    PRECONDITIONS: * Betslip is opened
    """
    keep_browser_open = True
    currency = '£'
    increment = None

    def enter_bet_amount_and_verify_error_message(self, bet_amount, expected_error_message):
        """
        Enters bet amount into appropriate betslip's field, clicks BET NOW and verifies error message
        :param bet_amount:
        :param expected_error_message:
        """
        stake_name, stake = list(self.singles_section.items())[0]
        stake_bet_amounts = {
            stake_name: bet_amount,
        }

        self.enter_stake_amount(stake=(stake_name, stake), stake_bet_amounts=stake_bet_amounts)
        self.get_betslip_content().bet_now_button.click()

        actual_error_message = self.get_betslip_content().bet_amount_warning_message
        self.assertEqual(actual_error_message, expected_error_message,
                         msg=f'Incorrect error message is displayed when entering bet amount {bet_amount}.\n'
                             f'Actual error message is "{actual_error_message}"\n'
                             f'Expected error message is "{expected_error_message}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login and add UK Tote bet (any pool type) to the betslip
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)
        # ToDo: add possibility to get any type of tote event after siteserve refactoring is completed
        self.__class__.eventID = event.event_id

        self.__class__.min_stake_per_line = event.min_stake_per_line
        self.__class__.max_stake_per_line = event.max_stake_per_line
        self.__class__.min_total_stake = event.min_total_stake
        self.__class__.max_total_stake = event.max_total_stake
        self.__class__.increment = event.stake_increment

        self.__class__.min_stake_error_message = vec.betslip.TOTE_BET_ERRORS.small_stake.format(
            stake_per_line='%.2f' % self.min_stake_per_line,
            stake_per_bet='%.2f' % self.min_total_stake,
            currency=self.currency)
        self.__class__.max_stake_error_message = vec.betslip.TOTE_BET_ERRORS.large_stake.format(
            stake_per_line='%.2f' % self.max_stake_per_line,
            stake_per_bet='%.2f' % self.max_total_stake,
            currency=self.currency)

        self.site.login(username=tests.settings.disabled_overask_user)
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')

        tab_opened = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(
            vec.racing.RACING_EDP_MARKET_TABS.totepool)
        self.assertTrue(tab_opened, msg='UK Tote tab is not opened')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found')
        selection_name, section = list(sections.items())[0]
        exacta_opened = section.grouping_buttons.click_button(vec.uk_tote.UK_TOTE_TABS.exacta)
        self.assertTrue(exacta_opened, msg='Exacta tab is not opened')
        outcomes = list(section.pool.items_as_ordered_dict.items())
        self.assertTrue(outcomes, msg=f'No outcomes found in "{selection_name}" selection')

        selection_outcomes = []
        for index, (outcome_name, outcome) in enumerate(outcomes[:2]):
            selection_outcomes.append(f'{index + 1} {outcome_name}')
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg=f'No checkboxes found for "{outcome_name}"')
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(),
                            msg=f'Checkbox "{checkbox_name}" is not selected for "{outcome_name}" after click')

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        _, section = list(sections.items())[0]
        self.assertTrue(section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

        section.bet_builder.summary.add_to_betslip_button.click()
        self.site.open_betslip()

        self.__class__.singles_section = self.get_betslip_sections().Singles

    def test_001_enter_stake_that_is_less_than_minimum_allowed_value_for_unit_stake_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter stake that is **less** than minimum allowed value for **unit** stake and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake too small. The minimum stake per line is <MinStakePerLine> The minimum stake per bet is<MinStakePerBet>"**
        """
        bet_amount = round(uniform(0.01, self.min_stake_per_line - 0.01), 2)
        self.enter_bet_amount_and_verify_error_message(bet_amount=bet_amount,
                                                       expected_error_message=self.min_stake_error_message)

    def test_002_enter_stake_that_is_less_than_minimum_allowed_value(self):
        """
        DESCRIPTION: Enter stake that is **less** than minimum allowed value for **total** stake (but more than minimum allowed value for unit stake) and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake too small. The minimum stake per line is <MinStakePerLine> The minimum stake per bet is<MinStakePerBet>"**
        """
        bet_amount = round(uniform(self.min_stake_per_line + 0.01, self.min_total_stake - 0.01), 2)
        self.enter_bet_amount_and_verify_error_message(bet_amount=bet_amount,
                                                       expected_error_message=self.min_stake_error_message)

    def test_003_enter_stake_that_is_more_than_maximum_allowed_value(self):
        """
        DESCRIPTION: Enter stake that is **more** than maximum allowed value for **unit** stake (but less than maximum allowed value for total stake) and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake too high. The maximum stake per line is <MaxStakePerLine> The maximum stake per bet is<MaxStakePerBet>"**
        """
        bet_amount = round(uniform(self.max_stake_per_line + 0.01, self.max_total_stake - 0.01), 2)
        self.enter_bet_amount_and_verify_error_message(bet_amount=bet_amount,
                                                       expected_error_message=self.max_stake_error_message)

    def test_004_enter_stake_that_is_more_than_maximum_allowed_value_for_total_stake_but_less_than_maximum(self):
        """
        DESCRIPTION: Enter stake that is **more** than maximum allowed value for **total** stake (but less than maximum allowed value for unit stake) and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake too high. The maximum stake per line is <MaxStakePerLine> The maximum stake per bet is<MaxStakePerBet>"**
        """
        bet_amount = self.max_total_stake + self.increment
        self.enter_bet_amount_and_verify_error_message(bet_amount=bet_amount,
                                                       expected_error_message=self.max_stake_error_message)

    def test_005_enter_stake_with_an_incorrect_increment_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter stake with an **incorrect** increment and tap "BET NOW"
        EXPECTED: Error message appears:
        EXPECTED: **"Stake must be in increments of £<incrementValue>"**
        """
        bet_amount = self.min_total_stake + self.increment / 2
        self.enter_bet_amount_and_verify_error_message(bet_amount=bet_amount,
                                                       expected_error_message='Stake must be in increments of %s'
                                                                              % '%.2f' % self.increment)
