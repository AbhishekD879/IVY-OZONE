import pytest
import tests
import voltron.environments.constants as vec
from collections import defaultdict
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # events can not be created on prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.overask
@pytest.mark.desktop
@vtest
class Test_C16396574_Bet_placement_when_one_bet_was_modified_and_another_rejected(BaseBetSlipTest):
    """
    TR_ID: C16396574
    NAME: Bet placement when one bet was modified  and another rejected
    DESCRIPTION: This test case verifies bet placement when one bet was modified and another rejected
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
    max_bet = 0.3
    max_mult_bet = 0.5
    prices = [{0: '1/12', 1: '1/10', 2: '1/9'},
              {0: '1/13', 1: '1/11', 2: '1/11'}]
    new_price = '1.5'
    selection_ids = []
    event_ids = []
    event_names = []

    def test_001_add_two_selections_to_the_betslip(self):
        """
        DESCRIPTION: Add two selections to the Betslip
        EXPECTED: Selection is successfully added
        """
        for i in range(0, 2):
            event_params = self.ob_config.add_autotest_premier_league_football_event(
                default_market_name='|Draw No Bet|', lp=self.prices[i],
                max_bet=self.max_bet,
                max_mult_bet=self.max_mult_bet)
            eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
            self.event_ids.append(eventID)
            self.event_names.append(f'{event_params.team1} v {event_params.team2}')

        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_mult_bet + 0.5
        sections = self.get_betslip_sections(multiples=True)
        self.assertTrue(sections, msg=f'"{sections}" is not added to the betslip')
        singles_section = sections.Singles
        for stake in self.zip_available_stakes(section=singles_section, number_of_stakes=2).items():
            self.enter_stake_amount(stake=stake)

        self.__class__.est_returns_before = self.get_betslip_content().total_estimate_returns
        bet_now_button = self.get_betslip_content().bet_now_button
        self.assertTrue(bet_now_button.is_enabled(), msg=f'"{bet_now_button.name}" button is disabled')
        bet_now_button.click()
        overask = self.get_betslip_content().wait_for_overask_panel()
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002__enter_stake_value_which_is_higher_then_maximum_limit_for_one_added_selection_enter_stake_value_which_is_higher_then_maximum_limit_for_another_added_selection(self):
        """
        DESCRIPTION: * Enter stake value which is higher then maximum limit for one added selection
        DESCRIPTION: * Enter stake value which is higher then maximum limit for another added selection
        EXPECTED:
        """
        # Covered in Step #1

    def test_003_tap_place_bet_button(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        EXPECTED: *   Overask is triggered for the User
        EXPECTED: *   The bet review notification is shown to the User
        """
        # Covered in Step #1

    def test_004__trigger_any_modification_by_trader_for_the_first_bet_trigger_rejecting_the_bet_by_a_trader_in_openbet_system_for_the_second_bet(self):
        """
        DESCRIPTION: * Trigger any modification by Trader for the first bet
        DESCRIPTION: * Trigger rejecting the bet by a trader in OpenBet system for the second bet
        EXPECTED: * 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' message and 'Offer expires: X:XX' counter are shown�on the top
        EXPECTED: * 'i'icon is displayed on the left side of the message
        EXPECTED: * The changed bet is shown to the user on the Betslip (highlighted in yellow color)
        EXPECTED: * 'This bet has not been accepted by traders!' message for the rejected bet is shown to the user
        EXPECTED: * The Estimate returns are updated according to new value
        EXPECTED: * 'Cancel' and 'Place a bet' buttons enabled
        EXPECTED: ![](index.php?/attachments/get/34018) ![](index.php?/attachments/get/34019)
        """
        bets_details = self.bet_intercept.find_bets_for_review(events_id=self.event_ids)
        acct_id = bets_details['acct_id']
        betslip_id = bets_details['bet_group_id']
        flag = False
        data = defaultdict(dict)

        for bet_id, bet_type in bets_details.items():
            if not flag:
                data['bet1']['id'] = bet_id
                data['bet1']['action'] = 'D'
                data['bet1']['bettype'] = bet_type
                flag = True
            else:
                data['bet2']['id'] = bet_id
                data['bet2']['price'] = self.new_price
                data['bet2']['action'] = 'O'
                data['bet2']['bettype'] = bet_type
                data['bet2']['stake'] = self.bet_amount
                data['bet2']['price_changed'] = 'Y'
        self.bet_intercept.multiple_actions_bets(acct_id=acct_id, betslip_id=betslip_id, bets_details=data)
        wait_for_result(lambda: self.get_betslip_content().overask_trader_section.trader_offer_info_icon.is_displayed(),
                        name='Waiting for the icon to be displayed',
                        timeout=20)
        self.assertTrue(self.get_betslip_content().overask_trader_section.trader_offer_info_icon,
                        msg='"i" icon is not displayed')
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        overask_warning_message = singles_section.overask_trader_offer.stake_content.stake_message
        self.assertEqual(overask_warning_message, vec.betslip.OVERASK_MESSAGES.bet_is_declined,
                         msg=f'Actual overask warning message: "{overask_warning_message}" is not equal '
                             f'to expected: "{vec.betslip.OVERASK_MESSAGES.bet_is_declined}"')

        stake_name, stake = list(singles_section.items())[1]
        self.assertEqual(stake.offered_price.background_color_value, vec.colors.OVERASK_MODIFIED_PRICE_COLOR,
                         msg=f'Modified price for "{stake_name}" is not highlighted in '
                             f'yellow "{stake.offered_stake.background_color_value}"')
        est_returns_after = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(est_returns_after, self.est_returns_before,
                            msg=f'Est returns before:"{self.est_returns_before}" and '
                                f'Est returns after:"{est_returns_after}" are equal')
        self.assertTrue(self.get_betslip_content().has_cancel_button(),
                        msg='"Cancel" button is not enabled')
        self.assertTrue(self.get_betslip_content().confirm_overask_offer_button.is_enabled(),
                        msg='"Place Bet" button is not enabled')

    def test_005_tap_place_bet_or_cancel_buttons(self):
        """
        DESCRIPTION: Tap 'Place bet' or 'Cancel' buttons
        EXPECTED: The bets are placed as per normal process
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()
