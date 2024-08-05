import pytest
import tests
import re
from tests.base_test import vtest
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from datetime import datetime
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Cannot create events on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.user_account
@vtest
class Test_C16706455_Vanilla_Coral_Verify_My_Freebets_Bonuses_page(BaseUserAccountTest, BaseBetSlipTest):
    """
    TR_ID: C16706455
    NAME: [Vanilla Coral] Verify 'My Freebets/Bonuses' page
    DESCRIPTION: This Test Case verified 'My Freebets/Bonuses' page
    PRECONDITIONS: 1. User is logged ( freebets list is received in user request only after login)
    PRECONDITIONS: 2. User has Free Bets available on his account
    """
    keep_browser_open = True
    amount = r'(-?[0-9]+(\.[0-9]+)?)'
    currency = '£'

    def test_000_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in
        """
        self.username = tests.settings.betplacement_user
        self.site.login(username=self.username)
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        home_team_selection_id = list(self.event.selection_ids.values())[0]
        self.ob_config.grant_freebet(username=self.username, level='selection', id=home_team_selection_id)

    def test_001_tap_account_button_on_the_header(self):
        """
        DESCRIPTION: Tap Account button on the header
        EXPECTED: Account Menu is displayed
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')

    def test_002_tap_offers__free_bets_options_from_the_list(self):
        """
        DESCRIPTION: Tap 'OFFERS & FREE BETS' options from the list
        EXPECTED: 'OFFERS & FREE BETS' menu is open
        """
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
            actual_menu_items = list(self.site.right_menu.items_as_ordered_dict)
            self.assertTrue((item in vec.bma.OFFERS_FREE_BETS_MENU_ITEMS for item in actual_menu_items),
                            msg=f'Actual offers & free bets items: "{actual_menu_items}"'
                                f' are not same as Expected offers & free bets items: '
                                f'"{vec.bma.OFFERS_FREE_BETS_MENU_ITEMS}"')
            self.site.right_menu.click_item(vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[1])
        else:
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[3])

    def test_003_tap_sports_free_bets_option(self):
        """
        DESCRIPTION: Tap 'SPORTS FREE BETS' option
        EXPECTED: 'My Freebets/Bonuses' page consists of:
        EXPECTED: * Back button
        EXPECTED: * 'My Freebets/Bonuses' title
        EXPECTED: * Cash Balance
        EXPECTED: * Total Balance
        EXPECTED: * Free bets section
        """
        self.assertTrue(wait_for_result(lambda: self.site.freebets.header_line, timeout=20),
                        msg='User is not navigated to "Free Bets" page')
        freebet_title_header = self.site.freebets.content_title_text
        self.assertEqual(freebet_title_header, 'MY FREEBETS/BONUSES',
                         msg=f'Freebet name "{freebet_title_header}" is not the same as expected')
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebet_items, msg='No Free Bets found on page')
        for freebet_item_name, freebet_item in list(freebet_items.items())[:10]:
            self.assertTrue(freebet_item_name, msg='Freebet title is not present')
            self.assertTrue(freebet_item.freebet_value,
                            msg=f'Freebet: "{freebet_item_name}" value is not present')

        if self.brand == 'ladbrokes':
            auto_freebet = list(freebet_items.values())[-1]
            match = re.search(self.amount, auto_freebet.name)
            free_bet_value = f'{vec.bma.FREE_BET.upper()}: {self.currency}{match.group()}'
            self.assertTrue(auto_freebet.freebet_text,
                            msg=f'Freebet text "{auto_freebet.freebet_text}" is not displayed')
            self.assertEqual(auto_freebet.freebet_title, free_bet_value,
                             msg=f'Freebet name "{auto_freebet}" is not the same as expected "{free_bet_value}"')
        else:
            free_bet = self.site.freebets.freebets_content.section_header
            auto_freebet = f'{free_bet.total_balance_with_currency} {free_bet.header_title}'
            match = re.search(self.amount, auto_freebet)
            free_bet_value = f'{self.currency}{match.group()} {vec.bma.FREE_BETS.upper()}'
            self.assertTrue(free_bet.has_fb_icon(), msg=f'"Free Bet Icon" is not displayed')
            self.assertTrue(self.site.freebets.header_line.back_button, msg=f'"Back button" is not displayed')
            self.assertEqual(auto_freebet, free_bet_value,
                             msg=f'Freebet name "{auto_freebet}" is not the same as expected "{free_bet_value}"')

    def test_004_verify_back_button(self):
        """
        DESCRIPTION: Verify Back button
        EXPECTED: User is navigated to the previous page after tapping Back button
        """
        if self.brand == 'bma':
            self.site.freebets.header_line.back_button.click()
            self.site.wait_content_state("Homepage")

    def test_005_verify_cash_balance(self):
        """
        DESCRIPTION: Verify Cash Balance
        EXPECTED: * Cash Balance is equal to user balance on the Header
        """
        self.navigate_to_page("/freebets")
        self.site.wait_content_state_changed()
        self.assertTrue(wait_for_result(lambda: self.site.freebets.header_line, timeout=20),
                        msg='User is not navigated to "Free Bets" page')
        if self.brand == 'bma':
            cash_balance = self.site.freebets.balance.cash_balance
            self.assertTrue(cash_balance, msg='User\'s cash balance is not shown')

            self.assertEqual(cash_balance, self.site.header.user_balance,
                             msg=f'User\'s balance "{cash_balance}" shown on Freebets page is not equal to '
                             f'balance shown on balance btn "{self.site.header.user_balance}"')

        total_balance = self.site.freebets.balance.total_balance
        self.assertTrue(total_balance, msg='User\'s total balance is not shown')

    def test_006_verify_total_balance(self):
        """
        DESCRIPTION: Verify Total Balance
        EXPECTED: Total balance is sum of all free bets and customer cash balance
        """
        # Covered is step 5

    def test_007_verify_free_bets_section(self):
        """
        DESCRIPTION: Verify Free bets section
        EXPECTED: Free bets section consists of:
        EXPECTED: * Expandable/collapsible panel
        EXPECTED: * Free bets icon
        EXPECTED: * Currency symbol + amount of all free bets available
        EXPECTED: * Free bets label
        EXPECTED: * List of all free bets
        EXPECTED: * CMS-controlled text message in case if there are no free bets available
        """
        freebet_items = self.site.freebets.freebets_content.items_as_ordered_dict
        self.assertTrue(freebet_items, msg='No Free Bets found on page')
        date_now = datetime.utcnow()
        for freebet_item_name, freebet_item in list(freebet_items.items())[:10]:
            self.assertTrue(freebet_item_name, msg='Freebet title is not present')
            if freebet_item.has_expires():
                expiration_date = freebet_item.expires
                self.assertIn(' day', expiration_date)
            else:
                expiration_date = freebet_item.used_by
                self.assertTrue(expiration_date, msg=f'Freebet: "{freebet_item_name}" expiration date is not present')
                self.assertTrue(date_now <= expiration_date,
                                msg=f'Freebet: "{freebet_item_name}" offer is expired')
            self.assertTrue(freebet_item.freebet_value,
                            msg=f'Freebet: "{freebet_item_name}" value is not present')
        # Freebet icon covered in step 3

    def test_008_verify_free_bets_item(self):
        """
        DESCRIPTION: Verify Free bets item
        EXPECTED: Free bets item consists of:
        EXPECTED: * Free bet description
        EXPECTED: * 'Use by' label + DD/MM/YYYY date if free bet expires in more than 7 days inclusive
        EXPECTED: **OR**
        EXPECTED: 'Expires' + number of day left if free bet expires in less than 7 days
        EXPECTED: * Free bet icon + Free bet value with appropriate currency
        EXPECTED: * '>' icon and link to the Freebet Details page
        """
        # Covered is step 7

    def test_009_tap_on_any_free_bet_item(self):
        """
        DESCRIPTION: Tap on any 'Free bet' item
        EXPECTED: 'FREEBET INFORMATION' page is opened
        """
        self.__class__.freebet_before = list(self.site.freebets.freebets_content.items_as_ordered_dict.values())
        self.freebet_before[0].click()
        self.site.wait_content_state_changed()

    def test_010_place_a_bet_on_selection_by_using_free_bet(self):
        """
        DESCRIPTION: Place a bet on selection by using free bet
        EXPECTED: Bet placement is placed successfully
        """
        selection = list(self.event.selection_ids.values())[0]
        self.open_betslip_with_selections(selection_ids=selection)
        self.place_single_bet(freebet=True)
        self.check_bet_receipt_is_displayed(timeout=10)

    def test_011_go_to_my_freebetsbonuses_page(self):
        """
        DESCRIPTION: Go to 'My Freebets/Bonuses' page
        EXPECTED: * Page is opened
        EXPECTED: * Used on step #11 Free bet is not displayed within list of all free bets tokens
        """
        self.navigate_to_page("/freebets")
        self.site.wait_content_state_changed()
        freebet_after = list(self.site.freebets.freebets_content.items_as_ordered_dict.values())
        self.assertNotEqual(self.freebet_before, freebet_after, msg="Used freebet is still displayed")
