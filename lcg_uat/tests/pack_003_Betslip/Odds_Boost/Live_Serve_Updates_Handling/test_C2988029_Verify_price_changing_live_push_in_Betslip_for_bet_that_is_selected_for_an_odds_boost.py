import pytest
import tests
from time import sleep
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - can't grant odds boost tokens on prod
# @pytest.mark.hl - can't grant odds boost tokens on hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C2988029_Verify_price_changing_live_push_in_Betslip_for_bet_that_is_selected_for_an_odds_boost(BaseBetSlipTest):
    """
     TR_ID: C2988029
     NAME: Verify price changing (live push) in Betslip for bet that is selected for an odds boost
     DESCRIPTION: This test case verifies price changing (live push) in Betslip for bet that is selected for an odds boost
     PRECONDITIONS: Enable Odds Boost in CMS
     PRECONDITIONS: Load Application
     PRECONDITIONS: Login into App by user with Odds boost token generated
     PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
     PRECONDITIONS: Add selection to the Betslip
     PRECONDITIONS: Add Stake and tap 'Boost' button
     PRECONDITIONS: Change price for this bet in https://backoffice-tst2.coral.co.uk/ti
     """
    keep_browser_open = True
    bet_amount = 0.7
    prices = '1/2'
    change_price = '5/3'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Enable Odds Boost in CMS
        PRECONDITIONS: Load Application
        PRECONDITIONS: Login into App by user with Odds boost token generated
        PRECONDITIONS: How to generate Odds Boost: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
        PRECONDITIONS: Add selection to the Betslip
        PRECONDITIONS: Add Stake and tap 'Boost' button
        PRECONDITIONS: Change price for this bet in https://backoffice-tst2.coral.co.uk/ti
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost', {})
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp_prices=self.prices)
        selection_ids = event_params.selection_ids
        _, selection_id = list(selection_ids.items())[0]
        offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        username = tests.settings.betplacement_user
        self.ob_config.grant_odds_boost_token(username=username, level='selection', id=selection_id,
                                              offer_id=offer_id)
        self.site.login(username=username, async_close_dialogs=False,
                        ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, close_free_bets_notification=False)
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=selection_id)
        singles_section = self.get_betslip_sections().Singles
        stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=(stake_name, self.stake))
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.odds_boost_header.boost_button.click()
        result = wait_for_result(
            lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
            name='"BOOST" button to become "BOOSTED" button with animation',
            timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        self.__class__.odds_value_before_price_change = self.stake.odds
        self.__class__.boosted_price_value = self.stake.boosted_odds_container.price_value
        self.ob_config.change_price(selection_id=selection_id, price=self.change_price)
        sleep(10)

    def test_001_verify_that_notification_messages_are_displayedverify_message_content(self):
        """
         DESCRIPTION: Verify that notification messages are displayed
         DESCRIPTION: Verify message content
         EXPECTED: **Before OX99**
         EXPECTED: - Inline message is displayed at the top of Bet slip
         EXPECTED: - Text: 'Some of the prices have changed, please re-boost your bet!' (displayed until user takes an action such as re-boost or navigates away from page)'
         EXPECTED: **After OX99**
         EXPECTED: - No message at the top for Coral
         EXPECTED: - **Only Ladbrokes:** Message 'Some of the prices have changed, please Re-Boost your bet!' is shown for 5s
         EXPECTED: - Message 'Price changed from XX to XX' is shown above the selection
         EXPECTED: ![](index.php?/attachments/get/33751)
         EXPECTED: ![](index.php?/attachments/get/33750)
         """
        error = self.stake.wait_for_error_message(timeout=10)
        expected_error = vec.betslip.STAKE_PRICE_CHANGE_MSG.format(
            old=self.prices, new=self.change_price)
        self.assertEqual(error, expected_error,
                         msg=f'Received error "{error}" is not the same as expected "{expected_error}"')

    def test_002_verify_that_inline_message_is_displayed_at_the_bottomverify_message_content(self):
        """
         DESCRIPTION: Verify that inline message is displayed at the bottom
         DESCRIPTION: Verify message content
         EXPECTED: **Before OX99**
         EXPECTED: - Inline message is displayed at the bottom
         EXPECTED: - Text: 'Some of the prices have changed, please re-boost your bet!' (displayed until user takes an action such as re-boost or navigates away from page)
         EXPECTED: **After OX99**
         EXPECTED: - Notification message: 'The price has changed and new boosted odds will be applied to your bet. Hit Re-Boost to see your new boosted prices' is shown at the bottom of Betslip
         EXPECTED: ![](index.php?/attachments/get/33752)
         EXPECTED: ![](index.php?/attachments/get/33753)
         """
        expected_error_message = vec.betslip.REBOOST_PRICE_CHANGE_BANNER_MSG
        general_error_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertTrue(general_error_msg, msg=f'Expected error message: "{expected_error_message}" has not appeared')
        self.assertEqual(general_error_msg, expected_error_message,
                         msg=f'Actual text : "{general_error_msg}" is not same as'
                             f'Expected text: "{expected_error_message}"')

    def test_003_verify_that_boost_button_text_changes_to_re_boost(self):
        """
         DESCRIPTION: Verify that boost button text changes to 'RE-BOOST'
         EXPECTED: Boost button text changes to 'RE-BOOST'
         """
        re_boost_name = self.odds_boost_header.boost_button.name
        self.assertEqual(re_boost_name, vec.odds_boost.BOOST_BUTTON.reboost,
                         msg=f'Actual text: "{re_boost_name}" is not same as the'
                             f'Expected text: "{vec.odds_boost.BOOST_BUTTON.reboost}"')

    def test_004_verify_that_the_boost_button_remains_selected(self):
        """
         DESCRIPTION: Verify that the boost button remains selected
         EXPECTED: The boost button remains selected
         """
        self.assertTrue(self.stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')

    def test_005_verify_that_the_non_boosted_striked_out_price_is_updated(self):
        """
         DESCRIPTION: Verify that the non-boosted striked out price is updated
         EXPECTED: The non-boosted striked out price is updated (according to the settle value in https://backoffice-tst2.coral.co.uk/ti from preconditions)
         """
        odds_value = self.stake.odds
        self.assertNotEqual(odds_value, self.odds_value_before_price_change,
                            msg=f'Actual odd value: "{odds_value}" is same as'
                                f'Expected odds vasle: "{self.odds_value_before_price_change}."')

    def test_006_verify_that_boosted_price_remains_unchanged(self):
        """
         DESCRIPTION: Verify that boosted price remains unchanged
         EXPECTED: The boosted price remains unchanged
         """
        previous_value = self.stake.boosted_odds_container.price_value
        self.assertEqual(previous_value, self.boosted_price_value,
                         msg=f'Actual odd value: "{previous_value}" is not same as'
                             f'Expected odds vasle: "{self.boosted_price_value}."')

    def test_007_verify_that_the_place_bet_button_displays_accept__place_bet(self):
        """
         DESCRIPTION: Verify that the 'Place bet' button displays: 'ACCEPT & PLACE BET'
         EXPECTED: The 'Place bet' button displays: 'ACCEPT & PLACE BET'
         EXPECTED: **After OX99**
         EXPECTED: Coral: 'ACCEPT & PLACE BET'
         EXPECTED: Ladbrokes: ''ACCEPT AND PLACE BET'
         """
        accept_place_bet_button = self.site.betslip.bet_now_button.name
        self.assertEqual(accept_place_bet_button, vec.betslip.ACCEPT_BET,
                         msg=f'Actual text: "{accept_place_bet_button}" is not same as the '
                             f'Expected text: "{vec.betslip.ACCEPT_BET}"')

    def test_008_tap_accept__place_bet_button__verify_that_the_updated_boosted_prices_are_retrieved__verify_that_the_bet_is_placed_at_the_boosted_odds(
            self):
        """
         DESCRIPTION: Tap 'ACCEPT & PLACE BET' button
         DESCRIPTION: - Verify that the updated boosted prices are retrieved
         DESCRIPTION: - Verify that the bet is placed at the boosted odds
         EXPECTED: - Updated boosted prices are retrieved
         EXPECTED: - The bet is placed at the boosted odds
         """
        self.site.betslip.bet_now_button.click()
        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Bet receipt sections not found')
        single_sections = sections.get(vec.betslip.SGL)
        self.assertTrue(single_sections, msg='single sections not found')
        sleep(2)
        boosted_value = single_sections.item_odds
        self.assertNotEqual(boosted_value, self.boosted_price_value,
                            msg=f'Boosted odds "{boosted_value}" are same as expected "{self.boosted_price_value}"')
