import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.low
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C11386092_Open_bets_tab_when_there_are_no_open_bets_available(BaseBetSlipTest):
    """
    TR_ID: C11386092
    NAME: 'Open bets' tab when there are no open bets available
    DESCRIPTION: This test case verifies text and ''Start betting'(Coral)/'Go betting'(Ladbrokes) button in Open bets tab
    DESCRIPTION: Design:
    DESCRIPTION: Coral: https://app.zeplin.io/project/5be15c714af2fc23b84d2fd3/screen/5c4f0e0920f1230172b7f095
    DESCRIPTION: Ladbrokes: https://app.zeplin.io/project/5c0a3ccfc5c147300de2a69b/screen/5c4f22d544fe0d63959b3162
    """
    keep_browser_open = True
    default_days = 30
    open_bet_message = "No open bets placed within the last " + str(default_days) + " days."

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User is logged in;
        PRECONDITIONS: User has no open bets available
        """
        self.site.login(username=tests.settings.no_bet_history_user, async_close_dialogs=False)

    def test_001_navigate_to_open_bets_tab_on_my_bets_page_bet_slip_widget(self):
        """
        DESCRIPTION: Navigate to 'Open bets' tab on 'My Bets' page/ 'Bet Slip' widget
        EXPECTED: 'Open bets' tab has opened
        """
        if self.device_type == 'mobile':
            self.site.open_my_bets_open_bets()
        else:
            self.navigate_to_page('open-bets')
        result = wait_for_result(lambda: self.site.open_bets.tab_content.grouping_buttons.current == self.expected_active_btn_open_bets,
                                 name=f'to became active"{self.expected_active_btn_open_bets}"',
                                 timeout=2)
        self.assertTrue(result, msg=f'sorting type is not selected by default:"{self.expected_active_btn_open_bets}"')

    def test_002_verify_open_bets_tab(self):
        """
        DESCRIPTION: Verify 'Open bets' tab
        EXPECTED: Text 'You currently have no open bets ' is present
        EXPECTED: Button 'Start betting'(Coral)/'Go betting'(Ladbrokes) is displayed according to design
        """
        self.__class__.open_bets = self.site.open_bets.tab_content.accordions_list
        self.assertEqual(self.open_bets.no_bets_text.upper(), self.open_bet_message.upper(),
                         msg=f'Actual Message: "{self.open_bets.no_bets_text}", is not equal to'
                             f'Expected Message: "{self.open_bet_message}"')
        self.assertTrue(self.open_bets.start_betting_button, msg=f'"Start betting" button is not displayed')

    def test_003_tap_start_bettinggo_betting_button(self):
        """
        DESCRIPTION: Tap 'Start betting'/'Go betting' button
        EXPECTED: User is redirected to the Home page
        """
        self.open_bets.start_betting_button.click()
        self.site.wait_content_state('HomePage')
