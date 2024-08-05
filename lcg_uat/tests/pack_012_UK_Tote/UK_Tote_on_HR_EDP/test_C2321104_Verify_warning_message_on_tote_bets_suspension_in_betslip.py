import voltron.environments.constants as vec
import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_012_UK_Tote.BaseUKTote import BaseUKTote


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.uk_tote
@pytest.mark.horseracing
@pytest.mark.liveserv_updates
@pytest.mark.races
@pytest.mark.login
@vtest
class Test_C2321104_Verify_warning_messages_for_Live_Updates_suspension_for_Tote_bets_in_BetSlip(BaseUKTote, BaseBetSlipTest):
    """
    TR_ID: C2321104
    NAME: Verify warning messages for Live Updates (suspension) for Tote bets in BetSlip
    DESCRIPTION: This test case verifies warning messages for Tote bets in the BetSlip, which appear when event/market/outcome are suspended
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is sufficient to cover the bet stake
    PRECONDITIONS: * Overask is disabled for the user in TI tool
    PRECONDITIONS: * User has added UK Tote bet (any pool type) to the betslip
    PRECONDITIONS: * Betslip is opened
    """
    keep_browser_open = True
    bet_amount = 3
    selection_id = None

    @classmethod
    def custom_tearDown(cls, **kwargs):
        ob_config = cls.get_ob_config()
        if cls.selection_id:
            ob_config.change_selection_state(selection_id=cls.selection_id, displayed=True, active=True)
        if cls.eventID:
            ob_config.change_event_state(event_id=cls.eventID, displayed=True, active=True)

    def test_000_login_and_place_bet(self):
        """
        DESCRIPTION: Login and place bet
        """
        event = self.get_uk_tote_event(uk_tote_exacta=True)

        self.__class__.eventID = event.event_id
        self.__class__.marketID = event.market_id

        self.site.login(username=tests.settings.betplacement_user)

        selection_outcomes = []

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
        self.assertTrue(outcomes, msg=f'No outcomes found in {selection_name} selection')

        ss_uk_tote_pool_outcomes = self.ss_req.ss_event_to_outcome_for_event(
            event_id=self.eventID)[0]['event']['children'][0]['market']['children']

        for index, (outcome_name, outcome) in enumerate(outcomes[:2]):
            selection_outcomes.append('%s %s' % (index + 1, outcome_name))
            checkboxes = outcome.items_as_ordered_dict
            self.assertTrue(checkboxes, msg='No checkboxes found for "%s"' % outcome_name)
            checkbox_name, checkbox = list(checkboxes.items())[index]
            checkbox.click()
            self.assertTrue(checkbox.is_selected(), msg='Checkbox "%s" is not selected for "%s" after click'
                                                        % (checkbox_name, outcome_name))
            if index > 0:
                for element in ss_uk_tote_pool_outcomes:
                    if element['outcome']['name'].strip('|') == outcome_name:
                        self.__class__.selection_id = element['outcome']['id']

        sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No one section was found')
        _, section = list(sections.items())[0]
        self.assertTrue(section.bet_builder.summary.add_to_betslip_button.is_enabled(),
                        msg='ADD TO BETSLIP button is not enabled')

        section.bet_builder.summary.add_to_betslip_button.click()

        self.site.open_betslip()

    def test_001_suspend_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend current event in TI
        EXPECTED: Error messages are appears:
        EXPECTED: * "Sorry, the **event** has been suspended" under bet info. (on a red background)
        EXPECTED: * "One of more of your selections has been suspended" above 'Total Stake' line info. (on a yellow background)
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=False)

        _, self.__class__.stake = self.get_betslip_sections().Singles.items()[0]

        self.assertTrue(self.stake.is_suspended(timeout=20), msg='Stake is not suspended')
        error = self.get_betslip_content().error
        self.assertEqual(error, vec.tote.TOTE_SUSPENSION_ERROR,
                         msg=f'Warning "{error}" is not the same '
                             f'as expected: "{vec.tote.TOTE_SUSPENSION_ERROR}"')

    def test_002_make_the_event_active_again_in_ti(self):
        """
        DESCRIPTION: Make the event active again in TI
        EXPECTED: Error messages are disappears
        """
        self.ob_config.change_event_state(event_id=self.eventID, displayed=True, active=True)

        self.assertFalse(self.stake.is_suspended(expected_result=False, timeout=20), msg='Stake is suspended')
        error = self.get_betslip_content().error
        self.assertFalse(error, msg=f'Warning message "{error}" is still present')

    def test_003_suspend_market_from_current_event_in_ti(self):
        """
        DESCRIPTION: Suspend market from current event in TI
        EXPECTED: Error messages are appears:
        EXPECTED: * "Sorry, the **market** has been suspended" under bet info. (on a red background)
        EXPECTED: * "One of more of your selections has been suspended" above 'Total Stake' line info. (on a yellow background)
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=False)

        self.assertTrue(self.stake.is_suspended(timeout=20), msg='Stake is not suspended')
        error = self.get_betslip_content().error
        self.assertEqual(error, vec.tote.TOTE_SUSPENSION_ERROR,
                         msg=f'Warning "{error}" is not the same '
                         f'as expected: "{vec.tote.TOTE_SUSPENSION_ERROR}"')

    def test_004_make_the_market_active_again_in_ti(self):
        """
        DESCRIPTION: Make the market active again in TI
        EXPECTED: Error messages are disappears
        """
        self.ob_config.change_market_state(event_id=self.eventID, market_id=self.marketID, displayed=True, active=True)

        self.assertFalse(self.stake.is_suspended(expected_result=False, timeout=20), msg='Stake is suspended')
        self.assertFalse(self.get_betslip_content().error,
                         msg=f'Warning message "{self.get_betslip_content().error}" is still present')

    def test_005_suspend_one_or_more_selections_from_current_bet_in_ti(self):
        """
        DESCRIPTION: Suspend one or more selections from current bet in TI
        EXPECTED: Error messages are appears:
        EXPECTED: * "Sorry, the **outcome** has been suspended" under bet info. (on a red background)
        EXPECTED: * "One of more of your selections has been suspended" above 'Total Stake' line info. (on a yellow background)
        """
        self.ob_config.change_selection_state(self.selection_id, displayed=True, active=False)

        self.assertTrue(self.stake.is_suspended(timeout=20), msg='Stake is not suspended')
        error = self.get_betslip_content().error

        self.assertEqual(error, vec.tote.TOTE_SUSPENSION_ERROR,
                         msg=f'Warning "{error}" is not the same '
                         f'as expected: "{vec.tote.TOTE_SUSPENSION_ERROR}"')

    def test_006_make_the_selections_active_again_in_ti(self):
        """
        DESCRIPTION: Make the selection(s) active again in TI
        EXPECTED: Error messages are disappears
        """
        self.ob_config.change_selection_state(self.selection_id, displayed=True, active=True)

        self.assertFalse(self.stake.is_suspended(expected_result=False, timeout=20), msg='Stake is suspended')
        self.assertFalse(self.get_betslip_content().error,
                         msg=f'Warning message "{self.get_betslip_content().error}" is still present')

    def test_007_enter_correct_stake_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter correct stake and tap "BET NOW"
        EXPECTED: Bet is successfully placed
        """
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, stake))

        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        self.assertTrue(self.site.bet_receipt.footer.has_done_button(),
                        msg='Done button is not shown, Bet was not placed')
