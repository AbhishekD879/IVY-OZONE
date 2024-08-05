import pytest
from tests.Common import Common
from tests.base_test import vtest
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.high
@pytest.mark.lotto
@pytest.mark.descoped  # this feature is no longer applicable so descoped the test case
@pytest.mark.desktop
@pytest.mark.back_button
@pytest.mark.safari
@vtest
class Test_C29583_Lottery_Main_Page(Common):
    """
    TR_ID: C29583
    NAME: Lottery Main Page
    DESCRIPTION: This Test Case verifies Lottery Main Page elements.
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-2307 - Lottery Main page and navigation
    DESCRIPTION: BMA-8873 - Lotto - design changes
    PRECONDITIONS: 1. Lotto icon should be preconfigured in Sports Menu Ribbon and/or A-Z Page via CMS
    PRECONDITIONS: 2. Launch application
    """
    keep_browser_open = True

    def test_001_navigate_to_lotto_page(self):
        """
        DESCRIPTION: Navigate to 'Lotto' page
        EXPECTED: 'Lotto' page is opened with following elements:
        EXPECTED: *   'Lotto' header and icon
        EXPECTED: *   Back button
        EXPECTED: *   Breadcrumbs trail (Desktop only)
        EXPECTED: *   Banner section
        EXPECTED: *   Lottery Selector carousel
        EXPECTED: *   Lottery title and help icon
        EXPECTED: *   'Reset Numbers' button
        EXPECTED: *   Selected Numbers line
        EXPECTED: *   'Lucky' buttons
        EXPECTED: *   'Include Bonus Ball?' checkbox
        EXPECTED: *   Odds
        EXPECTED: *   Field for bet value entering
        EXPECTED: *   'Options' expandable/collapsible section
        EXPECTED: *   'Draw' checkboxes
        EXPECTED: *   'Place Bet' button is shown by default
        """
        self.navigate_to_page(name='lotto')
        self.site.wait_content_state(state_name='Lotto')

        content = self.site.lotto
        tab_content = content.tab_content

        expected_title = vec.lotto.LOTTO if self.brand == 'ladbrokes'else vec.lotto.LOTTO.upper()

        sport_title = content.header_line.page_title.sport_title
        self.assertEqual(expected_title, sport_title,
                         msg=f'Page title is not "{expected_title}", but "{sport_title}"')
        has_back_button = self.site.has_back_button
        self.assertTrue(has_back_button,
                        msg='Back button isn\'t displayed on page header')
        self.assertTrue(content.lotto_carousel.is_displayed(),
                        msg='Lottery Selector Carousel isn\'t present on Lotto page')
        self.assertTrue(tab_content.info_panel.is_displayed(),
                        msg='Lottery title isn\'t present on Lotto page')
        self.assertTrue(tab_content.info_panel.info_btn.is_displayed(),
                        msg='Help icon is not present on Lotto page')
        self.assertTrue(tab_content.lucky_buttons.is_displayed(),
                        msg='Lucky buttons aren\'t present on Lotto page')
        self.assertTrue(tab_content.reset_numbers.is_displayed(),
                        msg='Reset Numbers button is not present on Lotto page')
        self.assertTrue(tab_content.number_selectors.is_displayed(),
                        msg='Number Selectors Line is not present on Lotto')

        list(tab_content.number_selectors.items_as_ordered_dict.values())[-1].click()
        choose_lucky_num_dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CHOOSE_YOUR_LUCKY_NUMBERS_BELOW,
                                                            verify_name=False,
                                                            timeout=15)
        self.assertTrue(choose_lucky_num_dialog, msg='"Choose Your Lucky Numbers" dialog is not shown')
        self.assertTrue(choose_lucky_num_dialog.is_displayed(), msg='Lucky number dialog is not displayed')
        choose_lucky_num_dialog.close_dialog()
        choose_lucky_num_dialog.wait_dialog_closed()
        self.assertTrue(self.site.lotto.tab_content.options.is_displayed(),
                        msg='Options section isn\'t shown on Lotto page')
        self.assertTrue(self.site.lotto.tab_content.place_bet.is_displayed(),
                        msg='Place bet button isn\'t shown on Lotto page')
        self.assertTrue(tab_content.bet_input.is_displayed(),
                        msg='Field for bet amount is not present on Lotto page')
        self.softAssert(self.assertTrue, tab_content.has_include_bonus_ball(),  # config issue
                        msg='Include Bonus ball is not present on Lotto page')
        self.assertTrue(tab_content.odds.is_displayed(),
                        msg='odd is not present on Lotto page')
        self.assertTrue(tab_content.draw_checkboxes.is_displayed(),
                        msg='odd is not present on Lotto page')

    def test_002_tap_back_button(self):
        """
        DESCRIPTION: Tap 'Back' button
        EXPECTED: 'Back' button takes user to the previous page he/she navigated from
        """
        self.site.back_button_click()
        self.site.wait_content_state('HomePage')

    def test_003_verify_main_applications_header_and_footer_presence(self):
        """
        DESCRIPTION: Verify main application's header and footer presence
        EXPECTED: Main application's header and footer are present on the page
        """
        self.assertTrue(self.site.header.is_displayed(), msg='Header is not displayed')
        self.assertTrue(self.site.footer.is_displayed(), msg='Footer is not displayed')
