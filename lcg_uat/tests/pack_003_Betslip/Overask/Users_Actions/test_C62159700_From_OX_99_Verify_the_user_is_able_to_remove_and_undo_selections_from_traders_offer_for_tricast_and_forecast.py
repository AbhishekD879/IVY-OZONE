import pytest
import tests
import voltron.environments.constants as vec
from time import sleep
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
class Test_C62159700_From_OX_99_Verify_the_user_is_able_to_remove_and_undo_selections_from_traders_offer_for_tricast_and_forecast(BaseBetSlipTest, BaseRacing):
    """
    TR_ID: C62159700
    NAME: [From OX 99] Verify the user is able to remove and undo selections from trader's offer for tricast and forecast
    DESCRIPTION: This test case verifies removing and undo for selections by a user for trader's offer by overask functionality for tricast and forecast
    PRECONDITIONS: User is logged in
    PRECONDITIONS: ======
    PRECONDITIONS: How to accept/decline/make an Offer with Overask functionality
    PRECONDITIONS: How to disable/enable Overask functionality for User or Event Type
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event
        EXPECTED: Event is created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]

        event_params = self.ob_config.add_UK_racing_event(max_bet=self.max_bet,
                                                          number_of_runners=3,
                                                          forecast_available=True,
                                                          tricast_available=True)
        self.__class__.eventID = event_params.event_id

        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_add_tricast_bet_to_betslip(self, tricast=True):
        """
        DESCRIPTION: Add 'tricast' Bet to Betslip
        EXPECTED:
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.__class__.expected_betslip_counter_value = 0
        if tricast:
            expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', tricast=True)
        else:
            expected_selection_name = self.place_forecast_tricast_bet_from_event_details_page(sport_name='horse-racing', forecast=True)

        self.site.open_betslip()
        self.__class__.sections = self.get_betslip_sections().Singles
        self.assertTrue(self.sections, msg='No stakes found')
        for actual_selection in self.sections:
            self.assertIn(actual_selection.strip(), expected_selection_name,
                          msg=f'Actual selection name: "{actual_selection}" is not in expected selections: '
                          f'"{expected_selection_name}"')

    def test_002_enter_the_value_in_stake_fields_that_do_not_exceed_the_max_allowed_bet_limit_for_all_of_the_added_selections(self):
        """
        DESCRIPTION: Enter the value in 'Stake' fields that do not exceed the max allowed bet limit for all of the added selections
        EXPECTED: The bet is sent to the Openbet system for review
        """
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet(number_of_stakes=1)

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: Overask overlay appears
        EXPECTED: ![](index.php?/attachments/get/160879433)
        """
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=15)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: Confirmation is sent and received in the Oxygen app
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.max_bet,
                                       price_type='S')

    def test_005_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: Selection with the maximum bet offer is expanded
        EXPECTED: The maximum bet offer for selected on step #3 bet and [X] remove buttons are shown to the user
        EXPECTED: Message 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' appears on the grey background below the checked selection
        EXPECTED: 'Place Bet and 'Cancel' buttons are present
        EXPECTED: 'Place Bet and 'Cancel' buttons are enabled
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

    def test_006_tap_the_remove_button_x(self):
        """
        DESCRIPTION: Tap the remove button [X]
        EXPECTED: Selection is changed in the bet slip:
        EXPECTED: selection name is grayed out
        EXPECTED: market name is grayed out
        EXPECTED: the event name is grayed out
        EXPECTED: price disappears
        EXPECTED: stake box disappears
        EXPECTED: Est. Returns for that individual bet (Available for tricast)
        EXPECTED: Remove [X] button disappears
        EXPECTED: [REMOVED] text appears
        EXPECTED: [UNDO] button appears
        EXPECTED: ![](index.php?/attachments/get/160879434)
        EXPECTED: ![](index.php?/attachments/get/160879435)
        """
        self.__class__.stake_name, self.__class__.stake = list(self.sections.items())[0]

        self.assertTrue(self.stake.remove_button.is_displayed(),
                        msg=f'Remove button was not found for stake "{self.stake_name}"')
        self.stake.select()
        self.site.wait_content_state_changed(timeout=15)
        self.assertTrue(self.stake.leg_remove_marker.is_displayed(),
                        msg=f'"Removed" text is not displayed')
        self.assertTrue(self.stake.has_undo_button,
                        msg=f'Undo button was not found for stake')

    def test_007_tap_the_undo_button(self):
        """
        DESCRIPTION: Tap the [UNDO] button
        EXPECTED: Selection is changed to the previous state:
        EXPECTED: selection name isn't grayed out
        EXPECTED: market name isn't grayed out
        EXPECTED: the event name isn't grayed out
        EXPECTED: price appears
        EXPECTED: stake box appears
        EXPECTED: Est. Returns for that individual bet (Available for tricast)
        EXPECTED: Remove [X] button appears
        EXPECTED: [REMOVED] text disappears
        EXPECTED: [UNDO] button disappears
        """
        self.stake.undo_button.click()
        sleep(1)
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

    def test_008_repeat_steps_2_7_for_forecast(self):
        """
        DESCRIPTION: Repeat steps 2-7 for Forecast
        """
        self.test_001_add_tricast_bet_to_betslip(tricast=False)
        self.test_002_enter_the_value_in_stake_fields_that_do_not_exceed_the_max_allowed_bet_limit_for_all_of_the_added_selections()
        self.test_003_verify_betslip()
        self.test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system()
        self.test_005_verify_betslip()
        self.test_006_tap_the_remove_button_x()
        self.test_007_tap_the_undo_button()
