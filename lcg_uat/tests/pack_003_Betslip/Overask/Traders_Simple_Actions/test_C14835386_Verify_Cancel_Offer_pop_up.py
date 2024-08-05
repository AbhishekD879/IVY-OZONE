import pytest
import voltron.environments.constants as vec
import tests
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod   # Overask cannot be triggered in prod.
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.critical
@pytest.mark.betslip
@vtest
class Test_C14835386_Verify_Cancel_Offer_pop_up(BaseBetSlipTest):
    """
     TR_ID: C14835386
     NAME: Verify 'Cancel Offer?' pop-up
     DESCRIPTION: This test case verifies 'Cancel Offer?' pop-up appears during cancelling the bet offer from a trader triggered by overask functionality
     PRECONDITIONS: 1. Load the app
     PRECONDITIONS: 2. User is logged in to the app
     PRECONDITIONS: 3. Overask functionality is enabled for the user
     PRECONDITIONS: 4. Go to CMS >'System-configuration' section > Config' tab > find 'Overask' config
     PRECONDITIONS: 5. Initial Data' checkbox is present within 'Overask' config and unchecked by default
     PRECONDITIONS: 6. The Initial response of the config contains 'The initialDataConfig: false'
     PRECONDITIONS: 7. The Initial Data response on homepage is absent
     PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
     PRECONDITIONS: Overask:
     PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190983
     PRECONDITIONS: https://confluence.egalacoral.com/pages/viewpage.action?pageId=41190955
     PRECONDITIONS: ![](index.php?/attachments/get/109045765)
     """
    keep_browser_open = True
    max_bet = 1
    suggested_max_bet = 0.25
    prices = {0: '1/12'}

    def test_000_precondition(self):
        """
        creating an event
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices,
                                                          max_bet=self.max_bet)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_load_oxygen_app(self):
        """
         DESCRIPTION: Load Oxygen app
         EXPECTED: Homepage is loaded
         """
        # covered in previous step

    def test_002__add_selection_and_go_betslip_singles_section_enter_value_in_stake_field_that_exceedsmax_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button(
            self):
        """
         DESCRIPTION: * Add selection and go Betslip, 'Singles' section
         DESCRIPTION: * Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button
         EXPECTED: * Overask is triggered for the User
         EXPECTED: * The bet review notification is shown to the User
         """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask not triggered for the User')
        overask_title_message = self.get_betslip_content().overask.overask_title.is_displayed()
        self.assertTrue(overask_title_message, msg='Overask title message is not shown')
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask exceeds message is not shown')
        overask_offer_message = self.get_betslip_content().overask.overask_offer.is_displayed()
        self.assertTrue(overask_offer_message, msg='Overask bottom message is not shown')

    def test_003_trigger_stake_modification_by_trader_in_openbet_system(self):
        """
         DESCRIPTION: Trigger Stake modification by Trader in OpenBet system
         EXPECTED: Confirmation is sent and received in Oxygen app
         """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask not yet closed')
        cms_overask_trader_message = self.get_overask_trader_offer()
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

    def test_004_verify_betslip(self):
        """
         DESCRIPTION: Verify Betslip
         EXPECTED: 'Cancel' and 'Place a bet' buttons are present and enabled
         """
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg="Cancel button not present")
        place_bet_button = self.get_betslip_content().confirm_overask_offer_button
        self.assertTrue(place_bet_button.is_enabled(), msg=f'"{place_bet_button.name}" button is disabled')

    def test_005_click__tap_cancel_button(self):
        """
         DESCRIPTION: Click / tap 'Cancel' button
         EXPECTED: * 'Cancel Offer?' pop up with a message 'Moving away from this screen will cancel your offer. Are you sure you want to go ahead?' and 'No, Return' and 'Cancel Offer' buttons, pop-up appears on the grey background
         EXPECTED: ![](index.php?/attachments/get/31093) ![](index.php?/attachments/get/31097)
         """
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        self.assertTrue(dialog, msg='"Cancel Offer?" pop up is not displayed')
        cancel_offer_text = dialog.cancel_offer_button.name
        self.assertEqual(cancel_offer_text, vec.betslip.OVERASK_ELEMENTS.confirm_cancel_traders_offer,
                         msg=f'"{cancel_offer_text}" is not same as "{vec.betslip.OVERASK_ELEMENTS.confirm_cancel_traders_offer}"')
        cancel_offer_msg = dialog.cancel_offer_msg.name
        self.assertEqual(cancel_offer_msg, vec.betslip.OVERASK_ELEMENTS.confirm_cancel_dialog_message,
                         msg=f'"{cancel_offer_text}" is not same as "{vec.betslip.OVERASK_ELEMENTS.confirm_cancel_dialog_message}"')
        popup_bgcolor = dialog.background_color_name
        self.assertEqual(popup_bgcolor, 'transparent',
                         msg=f'"cancel offer pop-up" does not contain the grey background')
        no_returns_text = dialog.no_return_button.name
        self.assertEqual(no_returns_text, vec.betslip.OVERASK_ELEMENTS.cancel_cancel_traders_offer,
                         msg=f'"{no_returns_text}" is not same as "{vec.betslip.OVERASK_ELEMENTS.cancel_cancel_traders_offer}"')
