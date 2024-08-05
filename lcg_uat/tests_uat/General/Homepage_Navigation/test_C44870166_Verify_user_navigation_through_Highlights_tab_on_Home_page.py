import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


@pytest.mark.prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.high
@pytest.mark.other
@pytest.mark.quick_links
@pytest.mark.featured
@pytest.mark.desktop
@pytest.mark.uat
@vtest
class Test_C44870166_Verify_user_navigation_through_Highlights_tab_on_Home_page(BaseBetSlipTest, ComponentBase):
    """
    TR_ID: C44870166
    NAME: Verify user navigation through Highlights tab on Home page
    DESCRIPTION: Verify user sees 'Highlights' tab in the homepage and user can scroll down the Highlights page
    DESCRIPTION: Verify user can place single and multiple bets using Highlights page selections.
    PRECONDITIONS: User should be logged in
    """
    keep_browser_open = True
    index, count = 0, 0

    def test_000_preconditions(self):
        """
        DESCRIPTION: User should be logged in
        EXPECTED: User should logged in successfully
        """
        self.site.login()
        self.__class__.is_mobile = True if self.device_type == 'mobile' else False

    def test_001_load_application(self):
        """
        DESCRIPTION: Load Application
        EXPECTED: Application page is loaded and user is landed on Home page with Highlights tab expanded by default
        EXPECTED: For Logged in User : If user has any Private Markets, 'Your Enhanced Markets' tab will be opened by default.
        NOTE : OB configuration cannot be done through automation
        """
        self.site.wait_content_state('Homepage')
        if self.is_mobile:
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            if self.brand == 'bma':
                self.assertEqual(current_tab, vec.SB.TABS_NAME_FEATURED.upper(),
                                 msg=f'Module Ribbon tab name: "{current_tab}" is not the same as '
                                     f'expected: "{vec.SB.TABS_NAME_FEATURED.upper()}"')
            if self.brand == 'ladbrokes':
                self.assertEqual(current_tab, vec.SB.MOBILE_FEATURED_MODULE_NAME,
                                 msg=f'Module Ribbon tab name: "{current_tab}" is not the same as '
                                     f'expected: "{vec.SB.MOBILE_FEATURED_MODULE_NAME}"')
        else:
            home_page_modules = self.site.home.desktop_modules.items_as_ordered_dict
            self.assertTrue(home_page_modules, msg='No module found on Home Page')
            featured_section = home_page_modules.get(vec.Inplay.IN_PLAY_LIVE_STREAM_SECTION_NAME)
            self.assertTrue(featured_section, msg='"Featured" section not found')

    def test_002_scroll_up_and_down_through_highlights_page(self):
        """
        DESCRIPTION: Scroll up and down through Highlights Page
        EXPECTED: Mobile : User is able to view all the events displayed on Highlights page including Surface bets. Quick links
        and Featured modules which are configured in CMS, In-Play events if there are any.
        """
        self.site.contents.scroll_to_bottom()
        self.site.contents.scroll_to_top()
        if self.is_mobile:
            if self.site.home.tab_content.has_surface_bets():
                surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
                self.assertTrue(surface_bets, msg='No Surface Bets found')
            if self.site.home.tab_content.has_quick_links():
                quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
                self.assertTrue(quick_links, msg='No Quick links found on the page')
            if self.site.home.tab_content.has_in_play_module():
                self.__class__.in_play_sports = self.site.home.tab_content.in_play_module.items_as_ordered_dict
                self.assertTrue(self.in_play_sports, msg=f'No items are present on "{vec.bma.IN_PLAY}" module')

    def test_003_tap_on_any_selection(self, expected_betslip_counter_value=0):
        """
        DESCRIPTION: Tap on any selection
        EXPECTED: for Mobile : Quick bet window should open
        EXPECTED: Tablet and Desktop : Selection gets added to bet slip
        """
        bet_buttons_list = self.site.home.bet_buttons
        self.assertTrue(bet_buttons_list, msg='No bet buttons on UI')
        for index in range(0, 10):
            index += 2
            bet_btn = bet_buttons_list[index]
            if bet_btn.is_enabled():
                self.scroll_to_we(bet_btn)
                bet_btn.click()
                self.count += 1
            else:
                continue
            if self.is_mobile:
                if self.count == 1:
                    self.site.add_first_selection_from_quick_bet_to_betslip()
            expected_betslip_counter_value += 1
            self.verify_betslip_counter_change(expected_value=expected_betslip_counter_value)
            if self.site.header.bet_slip_counter.counter_value == '2':
                self.site.open_betslip()
                self.assertTrue(self.site.has_betslip_opened(), msg='Betslip is not opened')
                break

    def test_004_add_multiple_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add multiple selections to the bet slip
        EXPECTED: Selections get added to the bet slip and bet slip counter updates
        """
        # This test step is covered in step 3

    def test_005_place_bet(self):
        """
        DESCRIPTION: Place bet
        EXPECTED: Mobile : User should be able to place bet from Quick bet window in case of single selection. In case of multiple selections, user should be able to place bet from bet slip.
        EXPECTED: Tablet & Desktop : User should be able to place bet from bet slip.
        """
        expected_number_of_selections = 2
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(len(singles_section) == expected_number_of_selections,
                        msg=f'No of selections: "{len(singles_section)}" is not the same as '
                            f'expected: "{expected_number_of_selections}"')

        for stake_name, stake in singles_section.items():
            if stake.is_suspended(timeout=30):
                self.assertTrue(stake.is_suspended(timeout=30), msg=f'Stake "{stake_name}" is not suspended')
                result = stake.amount_form.input.is_enabled(timeout=10, expected_result=False)
                self.assertFalse(result, msg=f'Amount field is not disabled for "{stake_name}"')
                self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(expected_result=False),
                                 msg='Bet Now button is not disabled')
                betnow_error = self.get_betslip_content().wait_for_error()

                if self.brand == 'ladbrokes':
                    result = wait_for_result(
                        lambda: betnow_error == vec.Betslip.SELECTION_DISABLED,
                        name='Betslip error to change',
                        timeout=5)
                    self.assertTrue(result, msg=f'Bet Now section warning message "{betnow_error}"'
                                                f'is not the same as expected: "{vec.Betslip.SELECTION_DISABLED}"')
                else:
                    result = wait_for_result(
                        lambda: betnow_error == vec.Betslip.SINGLE_DISABLED,
                        name='Betslip error to change',
                        timeout=5)
                    self.assertTrue(result, msg=f'Bet Now section warning message "{betnow_error}"'
                                                f'is not the same as expected: "{vec.Betslip.SINGLE_DISABLED}"')
                stake.remove_button.click()
            else:
                break
        singles_section_value = self.get_betslip_sections().Singles
        self.place_and_validate_single_bet(number_of_stakes=len(singles_section_value), timeout=5)
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_006_repeat_steps_1_4_for_a_logged_out_user(self):
        """
        DESCRIPTION: Repeat steps 1-4 for a logged out user
        """
        self.site.logout()
        self.test_001_load_application()
        self.test_002_scroll_up_and_down_through_highlights_page()
        self.test_003_tap_on_any_selection()
