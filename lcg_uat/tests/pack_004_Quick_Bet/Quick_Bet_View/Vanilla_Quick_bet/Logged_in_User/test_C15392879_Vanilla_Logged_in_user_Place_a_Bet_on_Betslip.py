import pytest
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events in prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C15392879_Vanilla_Logged_in_user_Place_a_Bet_on_Betslip(BaseBetSlipTest):
    """
    TR_ID: C15392879
    NAME: [Vanilla] [Logged in user] Place a Bet on Betslip
    DESCRIPTION: This test case verifies bet placement when the user is Logged in
    PRECONDITIONS: *Betslep should be enabled in CMS
    PRECONDITIONS: *User should be logged in and have a positive deposit
    PRECONDITIONS: *Selection should be added to betslip
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create required events
        """
        self.__class__.selection1 = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.selection2 = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.__class__.selection3 = self.ob_config.add_autotest_premier_league_football_event().selection_ids
        self.site.login()
        self.open_betslip_with_selections(list(self.selection1.values())[0])

    def test_001_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 1.  Betslip is opened
        EXPECTED: 2.  Added single selections are present
        EXPECTED: 3. 'Place bet' button is disabled
        EXPECTED: ![](index.php?/attachments/get/10272583)
        """
        self.assertTrue(self.site.has_betslip_opened(), msg='Bet Slip is not opened')
        self.__class__.singles_section = self.get_betslip_sections().Singles
        selection = self.singles_section.get(list(self.selection1.keys())[0])
        self.assertTrue(selection, msg='added selection is not present in betslip')
        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(), msg='"Place Bet" button is enabled before entering stake')

    def test_002_enter_at_least_one_stake_for_any_single_selection(self):
        """
        DESCRIPTION: Enter at least one stake for any single selection
        EXPECTED: 1. Stake is entered and displayed correctly
        EXPECTED: 2. 'Place bet' button becomes enabled
        """
        stake = list(self.singles_section.items())[0]
        self.enter_stake_amount(stake=stake)
        self.__class__.bet_button = self.get_betslip_content().bet_now_button
        self.assertTrue(self.bet_button.is_enabled(), msg='"Place Bet" button is enabled after entering stake')

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: Bet is placed successfully as for logged in user
        """
        self.bet_button.click()
        self.check_bet_receipt_is_displayed()

    def test_004_add_several_selections_from_different_events_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from different events to the Betslip
        EXPECTED: Betslip counter is increased
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=(list(self.selection1.values())[0], list(self.selection2.values())[0], list(self.selection3.values())[0]))

    def test_005_open_betslip(self):
        """
        DESCRIPTION: Open Betslip
        EXPECTED: 1.  Betslip is opened
        EXPECTED: 2.  Added multiple selections are present
        """
        self.assertTrue(self.site.has_betslip_opened(), msg='Bet Slip is not opened')
        single_section = self.get_betslip_sections().Singles
        for selection_name in [list(self.selection1.keys())[0], list(self.selection2.keys())[0], list(self.selection3.keys())[0]]:
            selection = single_section.get(selection_name)
            self.assertTrue(selection, msg='added selection is not present in betslip')

    def test_006_add_stake_for_any_selection_in_multiples_section_and_repeat_steps_3(self):
        """
        DESCRIPTION: Add stake for any selection in Multiples section and Repeat steps #3
        """
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
