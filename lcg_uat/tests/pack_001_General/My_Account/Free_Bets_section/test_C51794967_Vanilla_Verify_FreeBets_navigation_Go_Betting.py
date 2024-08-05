import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot grant freebets and create events in prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.user_account
@pytest.mark.freebets
@vtest
class Test_C51794967_Vanilla_Verify_FreeBets_navigation_Go_Betting(Common):
    """
    TR_ID: C51794967
    NAME: [Vanilla] Verify FreeBets navigation (‘Go Betting’)
    DESCRIPTION: This test case verifies "Go Betting" link on Sports Free Bets page
    PRECONDITIONS: - User has FreeBet(s) available
    PRECONDITIONS: - Instructions how to add freebet tokens for TEST2/STAGE users or existing PROD users with already granted tokens can be found here: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Account (Select Reward Token = 2428)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event and grant free bet
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.expected_event_name = event.team1 + ' v ' + event.team2
        self.__class__.user = self.gvc_wallet_user_client.register_new_user().username
        self.ob_config.grant_freebet(username=self.user, level='event', id=event.event_id)

    def test_001_login_to_the_account_with_freebets_available(self):
        """
        DESCRIPTION: Login to the account with FreeBet(s) available
        EXPECTED: User is logged in
        """
        self.site.login(username=self.user)

    def test_002_coralnavigate_to_my_account__offers__free_bets__sports_free_betsladbrokesnavigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Navigate to My Account > 'Offers & Free Bets' > Sports Free Bets
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Navigate to My Account > 'Promotions' > Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        EXPECTED: Sports Free Bets is displayed
        """
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        if self.brand == 'bma':
            self.site.right_menu.click_item(item_name=vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
            self.site.wait_content_state_changed()
            menu_items = self.site.right_menu.items_as_ordered_dict
            self.assertTrue(menu_items, msg='Offers menu has no items available.')
            self.site.right_menu.click_item(item_name=vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[1])
        else:
            self.site.right_menu.click_item(item_name=vec.bma.EXPECTED_RIGHT_MENU.sports_free_bets)
        self.site.wait_content_state_changed()
        self.__class__.freebets = list(self.site.freebets.freebets_content.items_as_ordered_dict.values())
        self.assertTrue(self.freebets, msg='freebets are not displayed.')

    def test_003_coraltap_on_free_bet_cardnavigation_arrow__tap_on_bet_now_buttonladbrokestap_on_go_betting_link(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Tap on Free Bet Card/Navigation Arrow > Tap on 'Bet Now' button
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Tap on "Go Betting" link
        EXPECTED: - User is redirected to applicable event for the selected FreeBet
        EXPECTED: - When navigating to an event there should be an event id or other info in response present [to edit later on
        EXPECTED: according more specific parameter in a response]
        """
        if self.brand == 'bma':
            self.freebets[0].click()
        self.site.freebet_details.bet_now.click()
        self.site.wait_content_state('EventDetails')
        actual_event_name = self.site.sport_event_details.event_name
        self.assertEqual(self.expected_event_name, actual_event_name, msg=f'Not navigated to applicable event {self.expected_event_name}')
