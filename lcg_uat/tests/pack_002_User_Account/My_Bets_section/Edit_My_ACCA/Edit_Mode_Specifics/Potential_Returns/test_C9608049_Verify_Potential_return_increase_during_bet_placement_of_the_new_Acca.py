import pytest
import tests
import json
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.helpers import do_request
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod //cannot update price in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@pytest.mark.desktop
@vtest
class Test_C9608049_Verify_Potential_return_increase_during_bet_placement_of_the_new_Acca(BaseCashOutTest):
    """
    TR_ID: C9608049
    NAME: Verify Potential return increase during bet placement of the new Acca
    DESCRIPTION: This test case verifies Potential return increase during bet placement of the new Acca
    PRECONDITIONS: **Configurations:
    PRECONDITIONS: Enable My ACCA feature toggle in CMS
    PRECONDITIONS: CMS -> System Configuration -> Structure -> EMA -> Enabled
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: Login into App
    PRECONDITIONS: Place Multiple bet
    PRECONDITIONS: Navigate to the Bet History from Right/User menu
    PRECONDITIONS: Go to 'Open Bets' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Go to 'Cash Out' Tab -> verify that 'Edit My Acca' button is available
    PRECONDITIONS: Tap on 'Edit My Acca' button in 'Open Bets' Tab -> verify that user is in 'My Acca Edit' mode
    PRECONDITIONS: Remove the selection from 'My Acca Edit' mode
    PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
    """
    keep_browser_open = True
    increased_price = '5/2'

    def get_bet_with_my_acca_edit(self):
        """
        Get bet with My ACCA edit functionality
        """
        _, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_DOUBLE_STAKE_TITLE, event_names=self.event.event_name,
            number_of_bets=1)
        self.assertTrue(bet, msg=f'Cannot find bet for "{self.event.event_name}"')
        return bet

    def get_stake_potential_returns_from_validatebet(self):
        url = f'{tests.settings.bpp}validateBet'
        placebet_request = self.get_web_socket_response_by_url(url=url)
        post_data = placebet_request.get('postData')
        header_data = placebet_request.get('headers')
        data = json.dumps(post_data)
        req = do_request(url=url, data=data, headers=header_data)
        self.__class__.stake = req['bet'][0]['subjectToCashout']['newBetStake']
        self.__class__.potential_returns = req['bet'][0]['betPotentialWin']

    def test_000_preconditions(self):
        """
           PRECONDITIONS: Login into App
           PRECONDITIONS: Place Multiple bet
           PRECONDITIONS: Navigate to the Bet History from Right/User menu
           PRECONDITIONS: Tap on 'Edit My Acca' button in 'Open Bets' Tab -> verify that user is in 'My Acca Edit' mode
           PRECONDITIONS: Remove the selection from 'My Acca Edit' mode
           PRECONDITIONS: NOTE: 'Edit My ACCA' button is shown only for the bets which placed on an ACCA - Single line Accumulators (it can be DOUBLE, TREBLE, ACCA4 and more)
        """
        if not self.cms_config.get_system_configuration_structure()['EMA']['enabled']:
            self.cms_config.set_my_acca_section_cms_status(ema_status=True)
        event_params = self.create_several_autotest_premier_league_football_events(number_of_events=2)
        self.__class__.event = event_params[0]
        selection_ids = [self.event.selection_ids, event_params[1].selection_ids]
        self.__class__.selection = list(event_params[0].selection_ids.values())[0]
        selection_name = self.event.team1
        event_name = f'{selection_name} - {self.event.event_name} {self.event.local_start_time}'
        self.site.login(username=tests.settings.betplacement_user)
        self.open_betslip_with_selections(selection_ids=[list(i.values())[0] for i in selection_ids])
        self.place_multiple_bet(number_of_stakes=1)
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.click_done()

        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[2])
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[6])
        self.site.wait_content_state_changed()
        actual_history_menu = list(self.site.right_menu.items_as_ordered_dict)
        self.assertEqual(actual_history_menu, vec.bma.HISTORY_MENU_ITEMS,
                         msg=f'Actual items: "{actual_history_menu}" are not equal with the'
                             f'Expected items: "{vec.bma.HISTORY_MENU_ITEMS}"')
        self.site.right_menu.click_item(vec.bma.HISTORY_MENU_ITEMS[0])
        self.site.wait_content_state('bet-history')
        if self.device_type == 'mobile':
            self.site.open_my_bets_open_bets()
        else:
            self.site.bet_history.tabs_menu.items_as_ordered_dict.get(vec.bet_history.OPEN_BETS_TAB_NAME).click()
        self.site.wait_content_state('open-bets')

        self.__class__.bet = self.get_bet_with_my_acca_edit()
        self.assertTrue(self.bet.edit_my_acca_button.is_displayed(),
                        msg=f'Bet with "{selection_name}" does not have My ACCA button on header')
        self.assertEqual(self.bet.edit_my_acca_button.name, vec.ema.EDIT_MY_BET,
                         msg=f'"{vec.ema.EDIT_MY_BET}" button has incorrect name')
        self.__class__.est_returns_value = self.bet.est_returns.stake_value
        self.bet.edit_my_acca_button.click()
        self.__class__.selection_leg = self.bet.items_as_ordered_dict.get(event_name)
        self.assertTrue(self.selection_leg.edit_my_acca_remove_icon.is_displayed(), msg='Remove icon is not displayed')
        self.selection_leg.edit_my_acca_remove_icon.click()

    def test_001_change_price_increasedecrease_for_one_of_selection_from_my_acca_edit_mode(self):
        """
        DESCRIPTION: Change price (increase/decrease) for one of selection from 'My Acca Edit' mode
        EXPECTED: Price is increased/decreased
        EXPECTED: The new potential returns increased/decreased
        """
        before_price = self.selection_leg.odds_value
        self.ob_config.change_price(selection_id=self.selection, price=self.increased_price)
        sleep(5)
        after_price = wait_for_result(lambda: self.selection_leg.odds_value, timeout=30)
        self.assertGreater(after_price, before_price, msg='price is not increased or decreased')

        actual_est_returns_value = self.bet.est_returns.stake_value
        self.assertLess(actual_est_returns_value, self.est_returns_value,
                        msg=f'New Potential Returns value "{actual_est_returns_value}" is not updated')

    def test_002_tap_confirm_button_and_verify_that_the_new_acca_is_successfully_placed_at_the_new_potential_returns(self):
        """
        DESCRIPTION: Tap 'Confirm' button and verify that the new Acca is successfully placed at the new potential returns
        EXPECTED: The new Acca is successfully placed at the new potential returns
        """
        self.get_stake_potential_returns_from_validatebet()
        self.assertEquals(self.bet.est_returns.stake_value, self.potential_returns,
                          msg=f'validateBet request potential returns "{self.potential_returns}" not displayed as same "{self.bet.est_returns.stake_value}"')
        self.assertEquals(self.bet.stake.stake_value, self.stake,
                          msg=f'validateBet request stake value "{self.stake}" is not displayed as same "{self.bet.stake.stake_value}"')

        self.assertTrue(self.bet.confirm_button.is_displayed(), msg='"Confirm" Button is not displayed')
        self.bet.confirm_button.click()
        result = wait_for_result(
            lambda: list(self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict.values())[0].cash_out_successful_message == vec.ema.EDIT_SUCCESS.caption,
            name='"Acca Edited Successfully" message to be displayed', timeout=20)
        sucsess_msg = self.bet.cash_out_successful_message
        self.assertTrue(result, msg=f'Message "{sucsess_msg}" '
                                    f'is not the same as expected "{vec.ema.EDIT_SUCCESS.caption}"')

    def test_003_verify_that_updated_prices_are_shown_against_each_open_selections(self):
        """
        DESCRIPTION: Verify that updated prices are shown against each Open Selections
        EXPECTED: Updated prices are shown against each Open Selections
        """

        # covered in step1

    def test_004_verify_that_new_stake_information_is_shown(self):
        """
        DESCRIPTION: Verify that New stake information is shown
        EXPECTED: New stake information is taken from *ValidateBet* request ('NewBetStake' attribute) and is displayed
        """

        # covered in step2

    def test_005_verify_that_new_potential_returns_are_shown(self):
        """
        DESCRIPTION: Verify that New Potential Returns are shown
        EXPECTED: New Potential Returns are taken from *ValidateBet* request ('BetPotentialWin' attribute) and displayed
        """

        # covered in step2
