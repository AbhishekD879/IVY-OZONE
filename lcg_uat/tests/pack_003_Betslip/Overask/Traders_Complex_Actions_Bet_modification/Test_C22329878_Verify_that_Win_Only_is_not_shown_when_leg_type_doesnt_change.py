import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  #Overask cannot be triggered in prod.
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C22329878_Verify_that_Win_Only_is_not_shown_when_leg_type_doesnt_change(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: Trigger Bet Split
    NAME: Verify that ‘Win Only’ is not shown when leg type doesn't change
    DESCRIPTION: This test case verifies that ‘Win Only’ is shown only when leg type is changed from ‘E/W’
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Leg Type (Each Way) is available for Racing selections (Each way terms are shown if isEachWayAvailable='true'):
    PRECONDITIONS: For verifying specific event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 4. Open Dev Tools -> Network -> XHR tab in order to check 'readBet' response
    """
    keep_browser_open = True
    max_bet = 20.00
    bet_amount = 3.00
    prices = {0: '1/12'}
    suggested_max_bet = 0.25

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event for HR
        EXPECTED: Event Created
        """
        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices=self.prices,
                                                          max_bet=self.max_bet)
        self.__class__.event_name = event_params.ss_response['event']['name']
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)

    def test_001_add_a_selectionfrom_racing_event_to_the_betslip(self):
        """
        DESCRIPTION: Add a selection from Racing event to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002___enter_stake_value_which_is_higher_than_maximum_limit_each_way_checkbox_is_not_checked(self):
        """
        DESCRIPTION: *  Enter stake value which is higher than maximum limit
        DESCRIPTION: * 'Each Way' checkbox is NOT checked
        EXPECTED:
        """
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1, each_way=False)

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')

    def test_004__do_not_change_leg_type_from_win_to_each_way_make_stakeprice_modification_by_trader_and_verify_offer_displaying_in_betslip(
            self):
        """
        DESCRIPTION: * Do NOT change Leg Type (from Win to Each way)
        DESCRIPTION: * Make Stake/Price modification by Trader and verify offer displaying in Betslip
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: *  The new stake/price is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: *  ‘Each Way’ is NOT displayed below the new stake
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
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

        section = self.get_betslip_sections().Singles
        stake_name, stake = list(section.items())[0]
        self.assertEqual(stake.offered_stake.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for "{stake_name}" is not highlighted in yellow')

        self.assertFalse(stake.has_each_way_checkbox(expected_result=False, timeout=1),
                         msg='Each way check box is displayed')

        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg="Cancel button is disabled")
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg=f'"{self.get_betslip_content().confirm_overask_offer_button.name}" button is disabled')

    def test_005_tap_on_place_bet_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on 'Place bet' or 'Cancel' buttons
        EXPECTED: * Tapping 'Confirm'/ 'Place bet' (From OX 99) button places bet(s) as per normal process
        EXPECTED: * Tapping 'Cancel' button/and than 'Cancel offer' pop-up (From OX 99) clears offer and selection(s) is shown without stake
        """
        confirm_btn = self.get_betslip_content().confirm_overask_offer_button
        confirm_btn.click()
        self.check_bet_receipt_is_displayed(timeout=15)
        self.site.bet_receipt.footer.click_done()
