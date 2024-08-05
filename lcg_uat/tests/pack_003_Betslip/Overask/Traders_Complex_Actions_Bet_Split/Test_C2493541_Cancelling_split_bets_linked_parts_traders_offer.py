import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C2493541_Cancelling_split_bets_linked_parts_traders_offer(BaseBetSlipTest):
    """
    TR_ID: C2493541
    NAME: Cancelling split bets & linked parts trader's offer
    DESCRIPTION: This test case verifies bet split and linking within Overask functionality
    DESCRIPTION: Instruction how to split & link Overask bets: https://confluence.egalacoral.com/display/SPI/How+to+split+a+Bet+in+Overask+functionality
    PRECONDITIONS: - For selected User Overask functionality is enabled in backoffice tool (see instruction: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983 )
    PRECONDITIONS: - User is logged in to application
    """
    keep_browser_open = True
    max_bet = None
    stake_part1 = 1.50
    price_part1 = 1.50
    stake_part2 = 0.50
    price_part2 = 0.50

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        EXPECTED: Events are created
        """
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)

        self.__class__.eventID, self.__class__.team1, self.__class__.team2, self.__class__.selection_ids = \
            event_params.event_id, event_params.team1, event_params.team2, event_params.selection_ids

        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)

    def test_001_add_selection_to_the_betslip__open_betslip(self):
        """
        DESCRIPTION: Add selection to the Betslip > Open Betslip
        EXPECTED: Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids[self.team1])

    def test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection__tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake value which is higher then maximum limit for added selection > Tap 'Bet Now' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        self.__class__.bet_amount = self.max_bet + 0.10
        self.place_single_bet(number_of_stakes=1)

        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title: Bet review notification is not shown to the user')

    def test_003_in_ti_trigger__bet_split_for_several_parts__link_some_of_split_bets__stakeoddsprice_type_modification_submit_changes(
            self, linked=True):
        """
        DESCRIPTION: In TI trigger:
        DESCRIPTION: - Bet Split for several parts
        DESCRIPTION: - Link some of split bets
        DESCRIPTION: - Stake/Odds/Price Type modification
        DESCRIPTION: > Submit changes
        EXPECTED:
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')

        if linked:
            self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventID,
                                         bet_id=[bet_id], betslip_id=betslip_id,
                                         stake_part1=self.stake_part1, price_part1=self.price_part1,
                                         stake_part2=self.stake_part2, price_part2=self.price_part2, linked=True)
        else:
            self.bet_intercept.split_bet(account_id=account_id, event_id=self.eventID,
                                         bet_id=[bet_id], betslip_id=betslip_id,
                                         stake_part1=self.stake_part1, price_part1=self.price_part1,
                                         stake_part2=self.stake_part2, price_part2=self.price_part2, linked=False)

    def test_004_in_app_verify_bet_parts_with_modified_values_displaying_in_betslip(self, linked=True):
        """
        DESCRIPTION: In app: Verify Bet parts with modified values displaying in Betslip
        EXPECTED: *   The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: *  The bet parts are linked with 'link' symbol
        EXPECTED: *   'Accept & Bet' and 'Cancel' buttons are displayed
        EXPECTED: *   Bets are selected by default and 'Accept & Bet' button is enabled
        EXPECTED: **From OX 99**
        EXPECTED: *   The Bet parts are shown to the user with the changed values highlighted
        EXPECTED: *   Parent selection doesn't have a Remove button
        EXPECTED: *   Remove button displays only on the child selection
        EXPECTED: *   Buttons 'Cancel' and 'Place Bet' are displayed
        EXPECTED: New Design!
        EXPECTED: ![](index.php?/attachments/get/33780) ![](index.php?/attachments/get/33781)
        """
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" '
                             f'is not as expected: "{cms_overask_trader_message}" from CMS')

        singles_section = self.get_betslip_content().overask_trader_section.items

        if linked:
            for section in range(len(singles_section)):
                if section in [0]:
                    self.assertFalse(singles_section[section].has_remove_button(),
                                     msg=f'Remove button is present for "{singles_section[section].name}"')
                    price_color = singles_section[section].stake_value.background_color_value
                    self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                     msg=f'"Modified price" is not highlighted in yellow')
                if section in [1]:
                    self.assertTrue(singles_section[section].has_remove_button(),
                                    msg=f'Remove button is not present for "{singles_section[section].name}"')
                    price_color = singles_section[section].stake_value.background_color_value
                    self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                     msg=f'"Modified price" is not highlighted in yellow')
        else:
            for section in range(len(singles_section)):
                if section in [0]:
                    self.assertTrue(singles_section[section].has_remove_button(),
                                    msg=f'Remove button is present for "{singles_section[section].name}"')
                    price_color = singles_section[section].stake_value.background_color_value
                    self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                     msg=f'"Modified price" is not highlighted in yellow')
                if section in [1]:
                    self.assertTrue(singles_section[section].has_remove_button(),
                                    msg=f'Remove button is not present for "{singles_section[section].name}"')
                    price_color = singles_section[section].stake_value.background_color_value
                    self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                                     msg=f'"Modified price" is not highlighted in yellow')

        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='Place bet button is not displayed')
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg='Cancel button is disabled')

    def test_005_tap_cancel_button(self):
        """
        DESCRIPTION: Tap 'Cancel' button
        EXPECTED: *   Bets are not placed
        EXPECTED: *   Selection added in step 1 is displayed in Betslip
        EXPECTED: **From OX 99**
        EXPECTED: * 'Cancel Offer?' pop up with a message 'Moving away from this screen will cancel your offer. Are you sure you want to go ahead?' and 'No, Return' and 'Cancel Offer' buttons, pop-up appears on the grey background
        EXPECTED: ![](index.php?/attachments/get/31093)
        """
        self.get_betslip_content().cancel_button.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        self.assertTrue(self.dialog, msg='"Cancel Offer?" pop up is not displayed')

        self.assertTrue(self.dialog.cancel_offer_button, msg='Cancel button is not present on "cancel pop-up dialog"')
        self.assertTrue(self.dialog.no_return_button, msg='No Return button is not present on "cancel pop-up dialog"')
        self.assertEqual(self.dialog.cancel_offer_msg.name, vec.betslip.OVERASK_ELEMENTS.confirm_cancel_dialog_message,
                         msg=f'"{self.dialog.cancel_offer_msg}" is not same as "{vec.betslip.OVERASK_ELEMENTS.confirm_cancel_dialog_message}")')

    def test_006_from_ox_99click__tap_cancel_offer_button(self):
        """
        DESCRIPTION: **From OX 99**
        DESCRIPTION: Click / tap 'Cancel Offer' button
        EXPECTED: **From OX 99**
        EXPECTED: *  Betslip closes
        EXPECTED: *  Selection is NOT present in the betslip
        EXPECTED: *  User stays on the prev page
        """
        self.dialog.cancel_offer_button.click()
        self.dialog.wait_dialog_closed()
        if self.device_type != 'desktop':
            self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=10),
                             msg='Betslip widget was not closed')
            self.site.open_betslip()
        actual_message = self.get_betslip_content().no_selections_title
        self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual title message "{actual_message}" '
                             f'is not as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')
        self.site.wait_content_state(state_name='HomePage')

    def test_007_repeat_steps_1_5do_not_link_split_bets_in_step_3(self):
        """
        DESCRIPTION: Repeat steps 1-5
        DESCRIPTION: (do not link split bets in step 3)
        EXPECTED: *   Bets are not placed
        EXPECTED: *   Selection added in step 1 is displayed in Betslip
        """
        self.test_001_add_selection_to_the_betslip__open_betslip()
        self.test_002_enter_stake_value_which_is_higher_then_maximum_limit_for_added_selection__tap_bet_now_button()
        self.test_003_in_ti_trigger__bet_split_for_several_parts__link_some_of_split_bets__stakeoddsprice_type_modification_submit_changes(
            linked=False)
        self.test_004_in_app_verify_bet_parts_with_modified_values_displaying_in_betslip(linked=False)
        self.test_005_tap_cancel_button()
