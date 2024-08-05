import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Can not grant Freebet in prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C51875596_Vanilla_Verify_Free_Bets_section_after_placing_a_free_bet(BaseSportTest, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C51875596
    NAME: [Vanilla] Verify Free Bets section after placing a free bet
    DESCRIPTION: This test case verifies updating list of Free Bets on the Sports Free Bets page: Amount, balance & disappearing from Free Bets list
    PRECONDITIONS: - User has FreeBet(s) available with next 'Single/Multiple Redemption Values' on any 'Category'/'Class'/'Type'/'Event'/'Market'/'Selection' Bet Levels
    PRECONDITIONS: - Instruction how to create a 'Redemption Value' & add a Free Bet to a user: https://confluence.egalacoral.com/display/SPI/How+to+Manually+Add+Freebet+Token+to+Event (Select Reward Token = 2428)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event and grant free bet
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.expected_event_name = event.team1 + ' v ' + event.team2
        self.__class__.team1 = event.team1
        self.__class__.eventID = event.event_id
        user = tests.settings.freebet_user
        self.ob_config.grant_freebet(username=user, level='event', id=event.event_id)
        self.site.login(user)

    def test_001_coralnavigate_to_my_account__offers__free_bets__sports_free_betsladbrokesnavigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Navigate to My Account > 'Offers & Free Bets' > Sports Free Bets
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Navigate to My Account > 'Promotions' > Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        EXPECTED: Sports Free Bets page is opened
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

    def test_002_remember_the_amount_balance__list_of_free_bets(self):
        """
        DESCRIPTION: Remember the Amount, balance & list of 'Free Bets'
        EXPECTED:
        """
        if self.brand == 'bma':
            cash_balance = self.site.freebets.balance.cash_balance
            self.assertTrue(cash_balance, msg='User\'s cash balance is not shown')

            self.assertEqual(cash_balance, self.site.header.user_balance,
                             msg=f'User\'s balance "{cash_balance}" shown on Freebets page is not equal to '
                                 f'balance shown on balance btn "{self.site.header.user_balance}"')
        total_balance = self.site.freebets.balance.total_balance
        self.assertTrue(total_balance, msg='User\'s total balance is not shown')

    def test_003_go_to_any_sport_page_where_free_bets_from_preconditions_apply(self):
        """
        DESCRIPTION: Go to any <Sport> page where 'Free Bets' from preconditions apply
        EXPECTED: Corresponding <Sport> page is opened
        """
        freebet_sections = list(self.site.freebets.freebets_content.items_as_ordered_dict.values())
        self.assertTrue(freebet_sections, '"freebet  section" are not displayed')
        self.__class__.available_count = len(freebet_sections)
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state_changed()

    def test_004__add_selection_to_quick_betbetslip__place_a_bet_using_free_bets(self):
        """
        DESCRIPTION: - Add selection to 'Quick Bet'/'Betslip'
        DESCRIPTION: - Place a bet using 'Free Bets'
        EXPECTED: Bet is successfully placed
        """
        selection_name = self.team1.upper() if self.brand == 'ladbrokes' else self.team1
        bet_button = self.get_selection_bet_button(selection_name=selection_name, market_name=None)
        self.device.driver.implicitly_wait(1)
        bet_button.click()
        if self.device_type == 'mobile':
            self.site.wait_for_quick_bet_panel()
            self.site.quick_bet_panel.add_to_betslip_button.click()
            self.site.wait_quick_bet_overlay_to_hide()
        self.site.open_betslip()
        self.place_single_bet(freebet=True)
        self.site.bet_receipt.close_button.click()

    def test_005_coralnavigate_to_my_account__offers__free_bets__sports_free_betsladbrokesnavigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets__verify_free_bets_amount_and_balance(self):
        """
        DESCRIPTION: **Coral:**
        DESCRIPTION: Navigate to My Account > 'Offers & Free Bets' > Sports Free Bets
        DESCRIPTION: **Ladbrokes:**
        DESCRIPTION: Navigate to My Account > 'Promotions' > Free Bets
        DESCRIPTION: or
        DESCRIPTION: Navigate to My Account > Sports Free Bets
        DESCRIPTION: - Verify 'Free Bets' amount and balance
        EXPECTED: Free Bets amount and balance are updated according to available Free Bets
        """
        self.test_001_coralnavigate_to_my_account__offers__free_bets__sports_free_betsladbrokesnavigate_to_my_account__promotions__free_betsornavigate_to_my_account__sports_free_bets()
        self.test_002_remember_the_amount_balance__list_of_free_bets()

    def test_006_verify_the_list_of_free_bets(self):
        """
        DESCRIPTION: Verify the list of Free Bets
        EXPECTED: List of Free Bets is updated according to available Free Bets
        """
        after_using_freebet = list(self.site.freebets.freebets_content.items_as_ordered_dict.values())
        new_list_of_freebet_count = len(after_using_freebet)
        self.assertGreater(self.available_count, new_list_of_freebet_count, msg='free bets is not updated')
