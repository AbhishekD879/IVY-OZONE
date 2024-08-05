import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C15321612_From_OX_99_Verify_the_user_is_able_to_remove_and_undo_selections_from_traders_offer(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C15321612
    NAME: [From OX 99] Verify the user is able to remove and undo selections from trader's offer
    DESCRIPTION: This test case verifies removing and undo for selections by a user for trader's offer by overask functionality
    PRECONDITIONS: User is logged in
    PRECONDITIONS: ======
    PRECONDITIONS: [How to accept/decline/make an Offer with Overask functionality](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955)
    PRECONDITIONS: [How to disable/enable Overask functionality for User or Event Type](https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983)
    """
    keep_browser_open = True
    selection_ids = []
    event_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        self.__class__.max_mult_bet = self.max_bet + 0.1
        for i in range(0, 3):
            event_params = self.ob_config.add_UK_racing_event(max_bet=self.max_bet,
                                                              number_of_runners=3,
                                                              max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)

        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_add_a_few_selections_and_go_betslip_singles_section(self, single=True, double=False, multiple=False):
        """
        DESCRIPTION: Add a few selections and go Betslip, 'Singles' section
        """
        self.__class__.expected_betslip_counter_value = 0
        if single:
            self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        if double:
            self.open_betslip_with_selections(selection_ids=self.selection_ids[:2])
        if multiple:
            self.open_betslip_with_selections(selection_ids=self.selection_ids[:3])

    def test_002_enter_the_value_in_stake_fields_that_do_not_exceed_max_allowed_bet_limit_for_all_of_the_added_selections(self, single=True, multiple=False):
        """
        DESCRIPTION: Enter the value in 'Stake' fields that do not exceed max allowed bet limit for all of the added selections
        EXPECTED: The bet is sent to Openbet system for review
        """
        if single:
            self.__class__.bet_amount = self.max_bet + 1
            self.place_single_bet(number_of_stakes=1)
        if multiple:
            self.__class__.bet_amount = self.max_mult_bet + 1
            self.place_multiple_bet(number_of_stakes=1)

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *  Overask overlay appears
        EXPECTED: ![](index.php?/attachments/get/31295)
        EXPECTED: ![](index.php?/attachments/get/31296)
        """
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: Confirmation is sent and received in Oxygen app
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.event_ids[0])
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.max_bet,
                                       price_type='S')

    def test_005_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Selection with the maximum bet offer is expanded
        EXPECTED: *   The maximum bet offer for selected on step #3 bet and [X] remove buttons are shown to the user
        EXPECTED: *   Message 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' appears on the grey background below the checked selection
        EXPECTED: *   'Place Bet  and 'Cancel' buttons are present
        EXPECTED: *   'Place Bet  and 'Cancel' buttons are enabled
        """
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

    def test_006_tap_the_remove_button_x(self, single=True, multiple=False):
        """
        DESCRIPTION: Tap the remove button [X]
        EXPECTED: Selection is changed in the betslip:
        EXPECTED: * selection name is grayed out
        EXPECTED: * market name is grayed out
        EXPECTED: * event name is grayed out
        EXPECTED: * price disappears
        EXPECTED: * stake box disappears
        EXPECTED: * Est. Returns for that individual bet (Available for accas (double, trixie, etc))
        EXPECTED: * Remove [X] button disappears
        EXPECTED: * [REMOVED] text appears
        EXPECTED: * [UNDO] button appears
        EXPECTED: ![](index.php?/attachments/get/31272)
        EXPECTED: ![](index.php?/attachments/get/31273)
        """
        if single:
            sections = self.get_betslip_sections().Singles
        if multiple:
            sections = self.get_betslip_sections(multiples=True).Multiples
        self.__class__.stake_name, self.__class__.stake = list(sections.items())[0]

        self.assertTrue(self.stake.remove_button.is_displayed(),
                        msg=f'Remove button was not found for stake "{self.stake_name}"')
        self.stake.select()
        self.site.wait_content_state_changed(timeout=15)
        self.assertTrue(self.stake.leg_remove_marker.is_displayed(),
                        msg=f'"Removed" text is not displayed')
        self.assertTrue(self.stake.has_undo_button,
                        msg=f'Undo button was not found for stake')

    def test_007_tap_undo_button(self):
        """
        DESCRIPTION: Tap [UNDO] button
        EXPECTED: Selection is changed to the previous state:
        EXPECTED: * selection name isn't grayed out
        EXPECTED: * market name isn't grayed out
        EXPECTED: * event name isn't grayed out
        EXPECTED: * price appears
        EXPECTED: * stake box appears
        EXPECTED: * Est. Returns for that individual bet (Available for accas (double, trixie, etc))
        EXPECTED: * Remove [X] button appears
        EXPECTED: * [REMOVED] text disappears
        EXPECTED: * [UNDO] button disappears
        """
        self.stake.undo_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.stake.is_displayed(), msg='selections is not restored')
        self.assertTrue(self.stake.has_remove_button(), msg=f'Remove button is not present for "{self.stake_name}"')
        actual_removed_text = self.stake.name
        self.assertNotIn(vec.betslip.OVERASK_ELEMENTS.removed, actual_removed_text,
                         msg=f'Expected removed text: "{vec.betslip.OVERASK_ELEMENTS.removed}" is in'
                             f'Actual removed text: "{actual_removed_text}"')
        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()

    def test_008_repeat_steps_2_7_for_double(self):
        """
        DESCRIPTION: Repeat steps 2-7 for Double
        """
        self.test_001_add_a_few_selections_and_go_betslip_singles_section(single=False, double=True)
        self.test_002_enter_the_value_in_stake_fields_that_do_not_exceed_max_allowed_bet_limit_for_all_of_the_added_selections(single=False, multiple=True)
        self.test_003_verify_betslip()
        self.test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system()
        self.test_005_verify_betslip()
        self.test_006_tap_the_remove_button_x(single=False, multiple=True)
        self.test_007_tap_undo_button()

    def test_009_repeat_steps_2_7_for_multiple(self):
        """
        DESCRIPTION: Repeat steps 2-7 for Multiple
        """
        self.test_001_add_a_few_selections_and_go_betslip_singles_section(single=False, multiple=True)
        self.test_002_enter_the_value_in_stake_fields_that_do_not_exceed_max_allowed_bet_limit_for_all_of_the_added_selections(single=False, multiple=True)
        self.test_003_verify_betslip()
        self.test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system()
        self.test_005_verify_betslip()
        self.test_006_tap_the_remove_button_x(single=False, multiple=True)
        self.test_007_tap_undo_button()
