import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #  we cannot trigger price change on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C11780007_Actual_from_OX_99_Verify_displaying_price_change_notification_where_user_has_entered_a_stake(BaseBetSlipTest):
    """
    TR_ID: C11780007
    NAME: **[Actual from OX 99]** Verify displaying price change notification where user has entered a stake
    DESCRIPTION: This test case verifies displaying price change notification where user has entered a stake
    PRECONDITIONS: Login into App
    PRECONDITIONS: Add selection to the Betslip
    PRECONDITIONS: Enter Stake into 'Stake' field
    """
    keep_browser_open = True
    prices = {0: '1/20'}
    new_price = '1/10'
    bet_amount = 0.05

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_tennis_event_to_autotest_trophy(lp_prices=self.prices)
        selection_ids = event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.site.login()
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" is not added to the betslip')
        stake_name, self.__class__.stake = list(selections.items())[0]
        self.enter_stake_amount(stake=(stake_name, self.stake))

    def test_001_trigger_price_change_for_added_selection(self):
        """
        DESCRIPTION: Trigger price change for added selection
        EXPECTED: The selection price change is displayed via push with text:
        EXPECTED: 'Price change from x to y '
        """
        self.__class__.old_price = self.stake.odds
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price)

    def test_002_verify_that_notification_box_is_displayed_at_the_bottom_of_the_betslip(self):
        """
        DESCRIPTION: Verify that notification box is displayed at the bottom of the betslip
        EXPECTED: Info message is displayed at the bottom of the betslip: 'Some of the prices have changed!'
        """
        actual_error_betslip_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(actual_error_betslip_msg, vec.Betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Actual BetSlip error message "{actual_error_betslip_msg}" != 'f'Expected "{vec.Betslip.PRICE_CHANGE_BANNER_MSG}" ')
        new_price = self.stake.odds
        self.assertNotEqual(self.old_price, new_price, msg=f'Actual price"{self.old_price}" is same as updated price "{new_price}')

    def test_003_for_ladbrokes_only_verify_that_notification_box_is_displayed_at_the_top_of_the_betslip_with_animations_and_is_removed_after_5_seconds(self):
        """
        DESCRIPTION: **FOR LADBROKES ONLY** Verify that notification box is displayed at the top of the betslip with animations and is removed after 5 seconds
        EXPECTED: **FOR LADBROKES ONLY** Info message is displayed at the top of the betslip with animations and is removed after 5 seconds
        EXPECTED: 'Some of the prices have changed'
        """
        # covered in above step

    def test_004_verify_that_place_bet_button_text_is_updated(self):
        """
        DESCRIPTION: Verify that 'Place bet' button text is updated
        EXPECTED: The Place bet button text is updated to:
        EXPECTED: Coral: 'ACCEPT & PLACE BET'
        EXPECTED: Ladbrokes: 'ACCEPT AND PLACE BET'
        """
        bet_button_now = self.site.betslip.bet_now_button.name
        self.assertEquals(vec.betslip.ACCEPT_BET, bet_button_now,
                          msg=f'Button text is "{bet_button_now}" not match with text "{vec.betslip.ACCEPT_BET}"')
