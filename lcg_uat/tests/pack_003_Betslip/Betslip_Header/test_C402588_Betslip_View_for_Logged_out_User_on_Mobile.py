import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.betslip
@pytest.mark.mobile_only
@pytest.mark.medium
@vtest
class Test_C402588_Betslip_View_for_Logged_out_User_on_Mobile(BaseBetSlipTest):
    """
    TR_ID: C402588
    VOL_ID: C9697894
    NAME: Betslip View for Logged out User on Mobile
    DESCRIPTION: This test case verifies Betslip header if user is logged out
    PRECONDITIONS: Applies for Mobile only
    """
    keep_browser_open = True
    login_message = vec.betslip.NO_SELECTIONS_TITLE
    no_selections_message = vec.betslip.NO_SELECTIONS_MSG

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test event
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            self.__class__.eventID = event['event']['id']
            market = next((market for market in event['event']['children'] if market['market'].get('children')), None)
            outcomes_resp = market['market']['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id']
                                 for i in outcomes_resp if 'Unnamed' not in i['outcome']['name']}
            self.__class__.team1 = list(all_selection_ids.keys())[0]
            self.__class__.selection_id = all_selection_ids.get(self.team1)
        else:
            event_params = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.team1, selection_ids = event_params.team1, event_params.selection_ids
            self.__class__.selection_id = selection_ids[self.team1]

    def test_001_load_oxygen_on_mobile(self):
        """
        DESCRIPTION: Load Oxygen on mobile
        """
        # bet slip can't be open without bets added
        # self.site.open_betslip()

    def test_002_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: Betslip is opened
        EXPECTED: No 'Quick Deposit' link is displayed in Betslip header
        EXPECTED: 'Your Betslip is empty' text is shown
        EXPECTED: 'Please add one or more selections to place a bet' text is shown
        EXPECTED: 'GO BETTING' button is shown
        """
        # betslip = self.get_betslip_content()
        # no_selections_title = betslip.no_selections_title
        # self.assertFalse(betslip.has_deposit_link(expected_result=False),
        #                  msg='"Quick Deposit" link is displayed in Betslip header')
        # self.assertEqual(no_selections_title, self.login_message,
        #                  msg=f'Actual message: {no_selections_title} '
        #                  f'does not match expected: {self.login_message}')
        # self.assertEqual(betslip.no_selections_message, self.no_selections_message,
        #                  msg=f'Actual message: {betslip.no_selections_message} '
        #                  f'does not match expected: {self.no_selections_message}')
        # self.assertTrue(betslip.has_start_betting_button(),
        #                 msg='"GO BETTING" button does not exist')

    def test_003_close_betslip(self):
        """
        DESCRIPTION: Close Betslip
        """
        # self.get_betslip_content().close_button.click()

    def test_004_add_a_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add a selection to the Betslip
        EXPECTED: Yellow Circle is displayed on 'Betslip' icon in the top right corner displaying '1' as a number of added selections
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.get_betslip_content().close_button.click()

        self.verify_betslip_counter_change(expected_value=1)

    def test_005_open_betslip_page(self):
        """
        DESCRIPTION: Open Betslip page
        EXPECTED: Betslip is opened
        EXPECTED: No 'Quick Deposit' link is displayed in Betslip header
        EXPECTED: Your Selections: N (where N - number of selections) and 'REMOVE ALL' button is shown in the header
        EXPECTED: Added selection is displayed in the Betslip content area
        """
        self.site.open_betslip()
        betslip = self.get_betslip_content()
        self.assertFalse(betslip.has_deposit_link(expected_result=False),
                         msg='"Quick Deposit" link is displayed in Betslip header')
        expected_msg = f'{vec.betslip.YOUR_SELECTIONS} 1'
        actual_msg = f'{betslip.your_selection_header.title_text} {betslip.your_selection_header.count}'
        self.assertEqual(actual_msg, expected_msg,
                         msg=f'Actual "{actual_msg}" != Expected "{expected_msg}"')
        self.assertTrue(betslip.remove_all_button.is_displayed(),
                        msg=f'"{vec.betslip.REMOVE_ALL_SELECTIONS}" is not displayed')

        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section, msg='No items found in Betslip content area')
        self.assertEqual(len(singles_section), 1,
                         msg=f'Singles selection count "{self.get_betslip_content().selections_count}" is not the same as expected "1"')
        self.assertTrue(singles_section.get(self.team1), msg=f'Selection "{self.team1}" is not found')
