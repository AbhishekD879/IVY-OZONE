import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898509_Verify_that_the_X_button_in_the_counter_offer_closes_the_counter_offer_overlay_but_the_counter_offer_remains_active(BaseBetSlipTest):
    """
    TR_ID: C59898509
    NAME: Verify that the X button in the counter offer closes the counter offer overlay, but the counter offer remains active
    """
    keep_browser_open = True
    bet_username = tests.settings.betplacement_user
    max_bet = 2
    suggested_max_bet = 2.5
    prices = {0: '1/12', 1: '1/2', 2: '1/3'}

    def test_001_make_a_bet_that_triggers_overask(self):
        """
        DESCRIPTION: Make a bet that triggers Overask
        EXPECTED: Your bet should have gone through to Overask
        """
        self.site.login(username=self.bet_username)
        event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet,
                                                                                 lp_prices=self.prices)
        self.__class__.eventID, selection_id = event_params.event_id, list(event_params.selection_ids.values())[0]
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=selection_id)
        self.__class__.bet_amount = self.max_bet + 1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_make_any_type_of_counter_offer_in_the_ti(self):
        """
        DESCRIPTION: Make any type of counter offer in the TI
        EXPECTED: A counter offer should be seen on the counter offer
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.bet_username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        self.site.wait_splash_to_hide(5)
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')

    def test_003_click_on_the_x_in_the_top_left_hand_corner(self):
        """
        DESCRIPTION: Click on the X in the top left-hand corner.
        EXPECTED: The counter offer overlay should close.
        """
        if self.device_type == 'mobile':
            self.get_betslip_content().close_button.click()
        else:
            betslip_tabs = self.get_betslip_content().betslip_tabs.items_as_ordered_dict
            betslip_tabs[vec.sb.MY_BETS_FOOTER_ITEM.upper()].click()

        self.site.wait_content_state_changed()
        self.assertTrue(self.site.header.right_menu_button.is_displayed(),
                        msg='"The counter offer overlay" was closed as right menu button is diplayed')

    def test_004_click_on_the_bet_slip_counter_in_the_top_right_hand_or_any_selection_should_open_the_overlay_and_show_that_your_counter_offer_is_still_active_provided_that_the_timer_has_not_run_out(self):
        """
        DESCRIPTION: Click on the bet slip counter in the top right-hand or any selection, should open the overlay and show that your counter offer is still active (provided that the timer has not run out)
        EXPECTED: The counter offer should still be active.
        """
        if self.device_type == 'mobile':
            self.site.header.bet_slip_counter.click()
        else:
            self.device.refresh_page()
        self.site.wait_splash_to_hide(5)
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
