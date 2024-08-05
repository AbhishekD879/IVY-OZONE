import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  - Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.bet_placement
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C91381_Trader_modifies_the_Leg_Type_Each_Way_for_Multiples(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C91381
    NAME: Trader modifies the Leg Type (Each Way) for Multiples
    DESCRIPTION: This test case verifies offer for multiples displaying in Betslip when Leg Type was changed by Trader
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
    bet_amount = 3
    selection_ids = []
    prices = {0: '1/12'}
    expected_est_returns = [3.52, 6.55]
    expected_stake_value = 10

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test events
        """
        for i in range(0, 2):
            event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, max_bet=2, max_mult_bet=2,
                                                              lp_prices=self.prices, ew_terms=self.ew_terms)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self._logger.info(f'*** Created event with id: {self.eventID}, selection ids: {selection_ids.values()}')
            self.__class__.selection_ids.append(list(selection_ids.values())[0])

        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username, async_close_dialogs=False)

    def test_001_add_few_selections_from_different_racing_events_to_the_betslip(self):
        """
        DESCRIPTION: Add few selections from different Racing events to the Betslip
        EXPECTED: *   Selections are successfully added
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)

    def test_002_enter_stake_value_which_is_higher_than_maximum_limit_for_multiples(self, each_way=False):
        """
        DESCRIPTION: Enter stake value which is higher than maximum limit for multiples
        DESCRIPTION: 'Each Way' checkbox is unchecked
        """
        self.place_multiple_bet(number_of_stakes=1, each_way=each_way)

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        overask_overlay = wait_for_result(
            lambda: self.get_betslip_content().overask, name='Overask overlay to appear', timeout=10)
        self.assertTrue(overask_overlay, msg='Overask overlay is not shown')

    def test_004_trigger_leg_type_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(self, leg_type='E'):
        """
        DESCRIPTION: Trigger Leg Type and Stake modification by Trader and verify offer displaying in Betslip
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: *   The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: *   'E/W' with a tick is displayed below the new stake
        EXPECTED: *   'Cancel' and 'Place a bet' buttons enabled
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{betslip_id}"')

        self.prices = self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                               betslip_id=betslip_id, leg_type=leg_type,
                                                               max_bet=self.bet_amount)
        overask_trader_message = wait_for_result(
            lambda: self.get_betslip_content().overask_trader_section.trader_message,
            name='Overask trader message to appear', timeout=10)
        self.assertTrue(overask_trader_message, msg=f'Overask trader message has not appeared')

        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" '
                             f'is not as expected: "{cms_overask_trader_message}" from CMS')

        betslip_section = self.get_betslip_content()

        self.__class__.place_bet_button = betslip_section.confirm_overask_offer_button
        self.assertTrue(self.place_bet_button.is_enabled(), msg=f'"{self.place_bet_button.name}" button is disabled')

        self.__class__.cancel_button = betslip_section.cancel_button
        self.assertTrue(self.cancel_button.is_enabled(), msg=f'"{self.cancel_button.name}" button is disabled')

        sections = self.get_betslip_sections(multiples=True)
        self.__class__.multiples_section = sections.Multiples

        if leg_type == "E":
            stake_value = self.multiples_section.overask_trader_offer.stake_content.stake_value.value
            actual_stake_value = float(stake_value.strip('£'))
            self.assertEqual(actual_stake_value, float(self.expected_stake_value),
                             msg=f'Actual stake value "{actual_stake_value}" '
                                 f'is not as expected: "{float(self.expected_stake_value)}"')

            each_way_text = self.multiples_section.overask_trader_offer.stake_content.each_way.name
            self.assertEqual(each_way_text, 'E/W',
                             msg=f'Actual Stake mark: "{each_way_text}" '
                                 f'is not as expected: "E/W"')

            each_way_tick = self.multiples_section.overask_trader_offer.stake_content.each_way.each_way_tick
            self.assertTrue(each_way_tick, msg='"E/W" mark is not displayed')
        else:
            each_way = self.multiples_section.overask_trader_offer.stake_content.has_each_way
            self.assertFalse(each_way, msg='"E/W" is displayed')

    def test_005_verify_new_est_returns_value(self):
        """
        DESCRIPTION: Verify new 'Est Returns' value
        EXPECTED: *   The 'Est. Returns' value corresponds to **bet.[i].payout.potential** attribute from **readBet** response, where **i** is taken from the object where **isOffer="Y"**
        EXPECTED: *   The 'Est. Returns' value is equal to **N/A** if no attribute is returned
        EXPECTED: *   The 'Est. Returns' value is NOT highlighted
        """
        est_returns = self.multiples_section.overask_trader_offer.stake_content.est_returns.value
        self.assertTrue(est_returns, msg='"Est. returns" value is not shown on Trader Offer')
        self.assertEquals(est_returns, 'N/A', msg='The "Est. returns" value is not equal "N/A"')

    def test_006_tap_on_place_bet_or_cancel_buttons(self, place_bet=True, cancel_bet=False):
        """
        DESCRIPTION: Tap on 'Place bet' or 'Cancel' buttons
        EXPECTED: *   Tapping 'Place bet' button places bet(s) as per normal process
        EXPECTED: *   Tapping 'Cancel' button/and than 'Cancel offer' pop-up clears and closes Betslip
        """
        if place_bet:
            self.place_bet_button.click()
            self.check_bet_receipt_is_displayed()
        if cancel_bet:
            self.cancel_button.click()
            dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
            dialog.cancel_offer_button.click()
            dialog.wait_dialog_closed()
            if self.device_type != 'desktop':
                self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=3),
                                 msg='Betslip widget was not closed')
                self.site.open_betslip()
            actual_message = self.get_betslip_content().no_selections_title
            self.assertEqual(actual_message, vec.betslip.NO_SELECTIONS_TITLE,
                             msg=f'Actual title message "{actual_message}" '
                                 f'is not as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_007_repeat_steps_1_5_but_with_enabled_each_way_checkbox(self):
        """
        DESCRIPTION: Repeat steps #1-5 but with enabled 'Each Way' checkbox
        EXPECTED: *   'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: *   The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: *   'E/W' with a tick is NOT displayed below the new stake
        EXPECTED: *   The 'Estimate Returns' are 'N/A'
        EXPECTED: *   'Cancel' and 'Place a bet' buttons enabled
        """
        self.__class__.expected_betslip_counter_value = 0
        self.site.bet_receipt.footer.click_done()
        self.test_001_add_few_selections_from_different_racing_events_to_the_betslip()
        self.test_002_enter_stake_value_which_is_higher_than_maximum_limit_for_multiples(each_way=True)
        self.test_003_tap_place_bet_button()
        self.test_004_trigger_leg_type_and_stake_modification_by_trader_and_verify_offer_displaying_in_betslip(leg_type='W')
        self.test_005_verify_new_est_returns_value()

    def test_008_repeat_step_6(self):
        """
        DESCRIPTION: Repeat step #6
        """
        self.test_006_tap_on_place_bet_or_cancel_buttons(place_bet=False, cancel_bet=True)
