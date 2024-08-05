import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # can't grant free bets on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.other
@vtest
class Test_C10397812_Verify_Free_Bet_Available_message_is_shown_on_the_Betslip(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C10397812
    NAME: Verify Free Bet Available message is shown on the Betslip
    DESCRIPTION: This test case verifies, that if User has Free Bet available, Free Bet Available message is shown on Betslip.
    PRECONDITIONS: 1. User has Free Bet available on their account
    PRECONDITIONS: 2. User is logged in
    PRECONDITIONS: 3. User has no bets added to the Betslip.
    """
    keep_browser_open = True
    bet_amount = 0.5

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        username = tests.settings.betplacement_user
        self.ob_config.grant_freebet(username=username)

        event = self.ob_config.add_UK_racing_event(number_of_runners=5)
        self.__class__.selection_id1 = list(event.selection_ids.values())[0]
        self.__class__.selection_id2 = list(event.selection_ids.values())[1]
        self.__class__.selection_id3 = list(event.selection_ids.values())[2]
        self.__class__.eventID = self.ob_config.add_football_event_to_spanish_la_liga().event_id
        market_name = self.ob_config.football_config.spain.spanish_la_liga.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        self.site.login(username=username)

    def test_001_navigate_to_the_betslip(self):
        """
        DESCRIPTION: Navigate to the Betslip
        EXPECTED: Betslip is empty
        EXPECTED: There is no message about Free Bets available shown on an empty Betslip.
        """
        self.site.open_betslip()
        betslip = self.get_betslip_content()
        no_selections_title = betslip.no_selections_title
        self.assertEqual(no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual message: {no_selections_title} '
                         f'does not match expected: {vec.betslip.NO_SELECTIONS_TITLE}')

    def test_002_click_on_the_selection(self):
        """
        DESCRIPTION: Click on the selection
        EXPECTED: Quick Bet pop-up is open.
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='football')
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)

    def test_003_verify_that_no_messages_about_free_bet_expiry_are_shown_on_quick_bet_pop_up(self):
        """
        DESCRIPTION: Verify, that NO messages about Free Bet Expiry are shown on Quick Bet pop-up.
        EXPECTED: No messages about Free Bet Expiry are shown on Quick Bet pop-up.
        """
        self.assertFalse(self.site.freebet_details.expires, msg='Freebet expires is displayed')

    def test_004_press_add_to_betslip_button_and_navigate_to_betslip(self):
        """
        DESCRIPTION: Press "Add to Betslip" button and navigate to Betslip.
        EXPECTED: Betslip is open.
        EXPECTED: Message is shown:
        EXPECTED: You have a free bet available!
        """
        self.site.quick_bet_panel.add_to_betslip_button.click()
        self.site.open_betslip()
        self.site.wait_content_state_changed(timeout=3)
        actual_freebets_notificaton = self.site.contents.free_bets_notification.text
        self.assertEqual(actual_freebets_notificaton, vec.bma.FREEBETS_AVAILABLE_MESSAGE,
                         msg=f'Actual freebet notification "{self.site.contents.free_bets_notification}"is not Equal to Expected free bet notification "{vec.bma.FREEBETS_AVAILABLE_MESSAGE}"')

    def test_005_do_some_changes_in_scope_of_current_bet_placement_session_add_more_bets_delete_some_of_them_etc(self):
        """
        DESCRIPTION: Do some changes in scope of current bet placement session (add more bets, delete some of them etc)
        EXPECTED: Verify, that message "You have a free bet available!" is shown each time when User opens Betslip.
        """
        self.__class__.expected_betslip_counter_value = 1
        self.open_betslip_with_selections(selection_ids=(self.selection_id1, self.selection_id2))
        actual_freebets_notificaton = self.site.contents.free_bets_notification.text
        self.assertEqual(actual_freebets_notificaton, vec.bma.FREEBETS_AVAILABLE_MESSAGE,
                         msg=f'Actual freebet notification "{self.site.contents.free_bets_notification}"is not Equal to Expected free bet notification "{vec.bma.FREEBETS_AVAILABLE_MESSAGE}"')

    def test_006_press_close_button_on_free_bet_message(self):
        """
        DESCRIPTION: Press close button on Free Bet message.
        EXPECTED: Free Bet message is closed.
        """
        self.site.contents.free_bets_notification.close_button.click()
        self.site.wait_content_state_changed(timeout=3)
        self.assertFalse(self.site.contents.has_free_bets_notification(), msg='The freebet notification is not closed')

    def test_007_verify_that_free_bet_message_isnt_shown_in_the_same_bet_placement_session_add_more_bets_delete_some_of_them_etc(self):
        """
        DESCRIPTION: Verify, that Free Bet Message isn't shown in the same bet placement session (add more bets, delete some of them etc).
        EXPECTED: Free Bet Message isn't shown.
        """
        self.__class__.expected_betslip_counter_value = 1
        self.open_betslip_with_selections(selection_ids=(self.selection_id1, self.selection_id2, self.selection_id3))
        self.assertFalse(self.site.contents.has_free_bets_notification(), msg='The freebet notification is displayed')

    def test_008_clear_betslip_add_a_bet_to_the_betslip_again_and_open_the_betslip(self):
        """
        DESCRIPTION: Clear Betslip, add a bet to the Betslip again and open the Betslip.
        EXPECTED: Message is shown:
        EXPECTED: You have a free bet available!
        """
        self.clear_betslip()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id1)
        actual_freebets_notificaton = self.site.contents.free_bets_notification.text
        self.assertEqual(actual_freebets_notificaton, vec.bma.FREEBETS_AVAILABLE_MESSAGE,
                         msg=f'Actual freebet notification "{self.site.contents.free_bets_notification}"is not Equal to Expected free bet notification "{vec.bma.FREEBETS_AVAILABLE_MESSAGE}"')

    def test_009_place_a_betclose_the_betslipopen_empty_betslip(self):
        """
        DESCRIPTION: Place a bet
        DESCRIPTION: Close the Betslip
        DESCRIPTION: Open empty Betslip
        EXPECTED: "You have a free bet available!" message is NOT shown.
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0
        self.site.open_betslip()
        betslip = self.get_betslip_content()
        no_selections_title = betslip.no_selections_title
        self.assertEqual(no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual message: {no_selections_title} '
                         f'does not match expected: {vec.betslip.NO_SELECTIONS_TITLE}')
        self.assertFalse(self.site.contents.has_free_bets_notification(), msg='The freebet notification is displayed')
