import pytest
import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C91382_Trader_modifies_the_Stake_Odds_and_Leg_Type_Each_Way(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C91382
    NAME: Trader modifies the Stake, Odds and Leg Type (Each Way)
    DESCRIPTION: This test case verifies offers displaying in Betslip when Stake, Price and Leg Type was changed by Trader
    PRECONDITIONS: 1. User is logged in to application
    PRECONDITIONS: 2. For selected User Overask functionality is enabled in backoffice tool
    PRECONDITIONS: 3. Leg Type (Each Way) is available for Racing selections (Each way terms are shown if isEachWayAvailable='true'):
    PRECONDITIONS: For verifying specific event use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - the event ID
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    prices = {0: '2/1', 1: '1/3'}

    def test_000_pre_conditions(self):
        self.__class__.max_bet = self.ob_config.overask_stake_config_items()[0]
        event = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=2, lp_prices=self.prices,
                                                   max_bet=self.max_bet)
        self.__class__.selection_id = list(event.selection_ids.values())[0]
        self.__class__.event_id = event.event_id
        self.__class__.marketID = event.market_id
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)

    def test_001_add_selectionfrom_racing_event_to_the_betslip(self):
        """
        DESCRIPTION: Add selection from Racing event to the Betslip
        EXPECTED: Selection is successfully added
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)

    def test_002___enter_stake_value_which_is_higher_than_maximum_limit_for_added_selection_each_way_checkbox_is_unchecked(self, ew=False):
        """
        DESCRIPTION: *  Enter stake value which is higher than maximum limit for added selection
        DESCRIPTION: * 'Each Way' checkbox is unchecked
        """
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1, each_way=ew)

    def test_003_tap_bet_now_place_bet_from_ox_99_button(self):
        """
        DESCRIPTION: Tap 'Bet Now' /'Place bet' (From OX 99) button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_004_trigger_stake_price_odds_and_leg_type_modification_by_trader_and_verify_offer_displaying_in_betslip(self, ew=True):
        """
        DESCRIPTION: Trigger Stake, Price (Odds) and Leg Type modification by Trader and verify offer displaying in Betslip
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message
                     and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new Price is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'E/W' with a tick is displayed below the new stake
        EXPECTED: * The Estimate returns are updated according to new stake
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/31458)
        EXPECTED: ![](index.php?/attachments/get/31459)
        """
        leg_type = 'E' if ew else 'W'
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.event_id)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=1,
                                       new_price='1/2', leg_type=leg_type, price_changed='Y')
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')

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

        sections = self.get_betslip_sections().Singles
        acpt_stake_name, acpt_stake = list(sections.items())[0]
        price_color = acpt_stake.offered_price.background_color_value
        self.assertEqual(price_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Accepted single price is not highlighted in yellow for "{acpt_stake_name}"')

        stake_color = acpt_stake.offered_stake.background_color_value
        self.assertEqual(stake_color, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Accepted single stake is not highlighted in yellow for "{acpt_stake_name}"')
        if ew:
            self.assertTrue(acpt_stake.ew_text)
            self.assertTrue(acpt_stake.ew_tick.is_displayed())
        else:
            self.assertTrue(acpt_stake.win_only_text)

        self.assertTrue(self.get_betslip_content().total_estimate_returns)
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(timeout=3),
                        msg='Bet button is not active, but was expected to be')
        self.assertTrue(self.get_betslip_content().cancel_button.is_enabled(), msg='Cancel button is disabled')

    def test_005_tap_on_confirmplace_bet_from_ox_99_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on 'Confirm'/'Place bet' (From OX 99) or 'Cancel' buttons
        EXPECTED: * Tapping 'Accept & Bet ([number of accepted bets])'/ 'Place bet' button places bet(s) as per normal process
        EXPECTED: * Tapping 'Cancel' button/and than 'Cancel offer' pop-up (From OX 99) clears offer and selection(s) is shown without stake
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_006_repeat_steps_1_4_with_enabled_each_way_checkbox(self):
        """
        DESCRIPTION: Repeat steps #1-4 with enabled 'Each Way' checkbox
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown on the top
        EXPECTED: * Selection is expanded
        EXPECTED: * The new Price is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * The new stake is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'Win Only' is displayed below the new stake
        EXPECTED: * The Estimate returns are updated according to new stake
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        """
        self.test_001_add_selectionfrom_racing_event_to_the_betslip()
        self.test_002___enter_stake_value_which_is_higher_than_maximum_limit_for_added_selection_each_way_checkbox_is_unchecked(ew=True)
        self.test_003_tap_bet_now_place_bet_from_ox_99_button()
        self.test_004_trigger_stake_price_odds_and_leg_type_modification_by_trader_and_verify_offer_displaying_in_betslip(ew=False)

    def test_007_tap_on_accept__bet_place_bet_from_ox_99_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap on ''Accept & Bet '/'Place bet' (From OX 99) or 'Cancel' buttons
        """
        self.test_005_tap_on_confirmplace_bet_from_ox_99_or_cancel_buttons()
