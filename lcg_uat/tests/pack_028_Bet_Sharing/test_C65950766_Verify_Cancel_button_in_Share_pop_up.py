import pytest
from voltron.environments import constants as vec
import tests
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@pytest.mark.bet_share
@pytest.mark.adhoc_suite
@pytest.mark.other
@vtest
class Test_C65950766_Verify_Cancel_button_in_Share_pop_up(BaseGolfTest):
    """
    TR_ID: C65950766
    NAME: Verify Cancel button in Share pop-up
    DESCRIPTION: This testcase verifies Cancel button in Share pop-up
    PRECONDITIONS: 
    """
    keep_browser_open = True
    bet_amount = 0.10
    device_name = 'iPhone 6 Plus' if not tests.use_browser_stack else tests.mobile_safari_default

    def enter_value_using_keyboard(self, value, on_betslip=True):
        keyboard = self.get_betslip_content().keyboard if on_betslip \
            else self.site.quick_bet_panel.selection.keyboard
        self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                        msg='Numeric keyboard is not shown')
        keyboard.enter_amount_using_keyboard(value=value)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'Lucky Dip is not Enabled in CMS')
        event = self.get_active_lucky_dip_events(category_id=16)[0][
            'event']
        self.__class__.sport_name = event['categoryCode'].upper()
        self.__class__.event_name = event['name'].upper()
        self.__class__.event_section_name = event['className'].upper() + " - " + event['typeName'].upper()
        self.__class__.start_time_local = self.convert_time_to_local(date_time_str=event['startTime'],
                                                                     ob_format_pattern=self.ob_format_pattern,
                                                                     future_datetime_format=self.my_bets_event_future_time_format_pattern,
                                                                     ss_data=True).upper()
        self.__class__.eventID = event['id']

    def test_001_launch_and_login_to_the_application(self):
        """
        DESCRIPTION: Launch and login to the Application
        EXPECTED: User should be able to launch and login to application successfully
        """
        self.site.wait_content_state("Homepage")
        self.site.login()

    def test_002_place_a_lucky_dip_bet_and_complete_lucky_dip_journey(self):
        """
        DESCRIPTION: Place a Lucky dip bet and complete Lucky dip journey
        EXPECTED: User is diplayed with Lucky dip Player card
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state('EVENTDETAILS')
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'),
                          None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.expand()
        self.lucky_dip_section.odds.click()
        quick_bet = self.site.quick_bet_panel.selection
        self.__class__.quick_bet = wait_for_result(lambda: quick_bet, timeout=5)
        self.assertTrue(self.quick_bet, msg="lucky dip landing page is not displayed for place bet")
        wait_for_haul(3)
        quick_bet_input = quick_bet.content.amount_form.input
        quick_bet_input.click()
        if not quick_bet.keyboard.is_displayed():
            quick_bet_input.click()
        self.assertTrue(quick_bet.content.amount_form.is_active(), msg='"Stake" box is not highlighted')
        self.assertTrue(quick_bet.keyboard.is_displayed(name='Betslip keyboard shown', timeout=10),
                        msg='Numeric keyboard is not opened')
        self.enter_value_using_keyboard(value=self.bet_amount, on_betslip=False)
        place_bet_button = self.site.quick_bet_panel.place_bet
        self.assertTrue(place_bet_button, msg="place bet button is not available")
        self.site.quick_bet_panel.place_bet.click()
        lucky_dip_got_it_animation = wait_for_result(
            lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=10), bypass_exceptions=VoltronException, timeout=5)
        self.assertTrue(lucky_dip_got_it_animation, msg='Lucky Dip Animation is not displayed to the user')

    def test_003_verify_whether_user_can_view_the_share_option_next_to_player_card_after_got_it_button(self):
        """
        DESCRIPTION: Verify whether user can view the Share option next to Player card after "Got it" button
        EXPECTED: User should be able see share icon for Lucky dip bet
        """
        #covered in above step

    def test_004_click_on_share_icon(self):
        """
        DESCRIPTION: Click on share icon
        EXPECTED: User should be able to click share icon.
        """
        self.site.lucky_dip_got_it_panel.lucky_Dip_share_button.click()
        self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_SHARE, timeout=5)

    def test_005_verify_pop_up_is_displaying_with_a_cms_config_inputs(self):
        """
        DESCRIPTION: Verify pop-up is displaying with a CMS config inputs.
        EXPECTED: User should be able to see pop-up with a CMS config inputs.eg-odds,stake,date etc
        """
        #covered  in C65969090

    def test_006_verify_cancel_button_in_pop_up(self):
        """
        DESCRIPTION: Verify CANCEL button in pop-up.
        EXPECTED: User should be able to click on CANCEL button.
        """
        share_dialog = self.site.dialog_manager.items_as_ordered_dict.get(vec.dialogs.DIALOG_MANAGER_SHARE)
        self.assertTrue(share_dialog, msg='"share" dialog is not displayed')
        share_dialog.cancel_button.click()

    def test_007_verify_user_has_reverted_back_to_the_previous_page(self):
        """
        DESCRIPTION: Verify user has reverted back to the previous page.
        EXPECTED: User should be able to see the previous page successfully.
        """
        luckey_dip_got_it_panel = wait_for_result(
            lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=5),
            timeout=5)
        self.assertTrue(luckey_dip_got_it_panel, msg='Lucky Dip Animation is not displayed to the user')
        # clicking on lucky Dip got it button
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        self.site.quick_bet_panel.lucky_dip_outright_bet_receipt.lucky_dip_close_button.click()
        self.site.open_my_bets_open_bets()
        open_bets = wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list,
                                    name='waiting for bets found on "Open Bets" page', expected_result=True,
                                    timeout=20)
        self.assertTrue(open_bets, msg='No bets found in open bet')
        open_bet_items = open_bets.items_as_ordered_dict
        lucky_dip_section = next((open_bet_item for open_bet_item_name, open_bet_item in open_bet_items.items() if open_bet_item_name.startswith('LUCKY DIP')), None)
        bet_leg_name, bet_leg = lucky_dip_section.first_item
        self.assertTrue(bet_leg.has_bet_share_button(), f'SHARE button is not available for bet : "{bet_leg_name}"')
        bet_leg.bet_share_button.click()
        self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_SHARE, timeout=5)
        share_dialog = self.site.dialog_manager.items_as_ordered_dict.get("Share")
        self.assertTrue(share_dialog, "SHARE dialog is not displayed after clicking on Share")
        share_dialog.cancel_button.click()