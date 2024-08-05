import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result
import voltron.environments.constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - can't grant odds boost tokens on prod
# @pytest.mark.hl - can't grant odds boost tokens on hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.bet_receipt
@pytest.mark.desktop
@pytest.mark.odds_boost
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.other
@vtest
class Test_C12835257_Odds_Boost_token_icon_displaying(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C12835257
    NAME: Odds Boost token icon displaying
    DESCRIPTION: This test case verifies displaying Odds Boost token value in Right menu and in My account (User menu).
    """
    keep_browser_open = True
    number_of_tokens = 2  # max 3
    bet_amount = 0.5

    def grant_odds_boost_token(self):
        self.ob_config.grant_odds_boost_token(username=self.username)
        self.__class__.expected_odds_boost_amount += 1

    def get_odds_boost_amount(self):
        self.site.right_menu.click_item(self.offers_title)
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu has no items available.')
        self.assertIn(self.odds_boost_title, menu_items.keys(),
                      msg=f'"{self.odds_boost_title}" not present in the Right column')
        odds_boost_menu_item = menu_items.get(self.odds_boost_title)
        self.assertTrue(odds_boost_menu_item, msg='Odds Boost menu item not found.')
        badge_text = odds_boost_menu_item.badge_text
        self.__class__.odds_boost_amount = int(badge_text) if badge_text else 0

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 'Odds Boost' Feature is enabled in CMS
        PRECONDITIONS: 'Odds Boost' item is enabled in Right menu in CMS
        PRECONDITIONS: 'My account' (User menu) Feature Toggle is enabled in CMS
        PRECONDITIONS: 'Odds Boost' item is enabled in My account (User menu) in CMS
        PRECONDITIONS: Add Odds Boost token to Any bet to the user
        PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
        PRECONDITIONS: Generate Upcoming token in http://backoffice-tst2.coral.co.uk/office
        PRECONDITIONS: How to create Upcoming Boosts https://confluence.egalacoral.com/display/SPI/How+to+create+Upcoming+Boosts
        PRECONDITIONS: Note: Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
        PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
        :return:
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        try:
            cms_right_menus = self.cms_config.get_cms_menu_items(menu_types='Right Menus').get('Right Menus')
        except AttributeError:
            raise CmsClientException('Right Menu item not found in System Configuration')

        odds_boost_menu = next((menu for menu in cms_right_menus if menu.get('linkTitle') == vec.odds_boost.PAGE.title), None)
        if not odds_boost_menu:
            raise CmsClientException('Odds Boost menu not enabled in Right Menu CMS')

        my_acc_menu = next((menu for menu in cms_right_menus if menu.get('linkTitle') == 'My Account'), None)
        if not my_acc_menu:
            raise CmsClientException('My Account menu not enabled in Right Menu CMS')

        self.__class__.selection_ids = self.ob_config.add_autotest_premier_league_football_event().selection_ids

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.add_card_and_deposit(self.username, amount=tests.settings.min_deposit_amount)
        self.site.login(username=self.username)

        self.site.logout()

        self.__class__.expected_odds_boost_amount = 0

        for i in range(self.number_of_tokens):
            self.grant_odds_boost_token()

        self.__class__.selection_number = 0

        self.site.login(username=self.username)

    def test_001_verify_that_sum_value_of_odds_boost_tokens_is_shown(self):
        """
        DESCRIPTION: Navigate to the 'My account' from Right menu (for mobile and tablet).
        DESCRIPTION: Navigate to 'My account' from the header of the page (for desktop).
        DESCRIPTION: Verify that sum value of Odds Boost tokens is shown.
        EXPECTED: * 'My account' menu is expanded
        EXPECTED: * Odds Boost item is available in the menu
        EXPECTED: * Sum value of Odds Boost tokens is displayed
        """
        if self.device_type == 'mobile':
            self.site.header.right_menu_button.click()
            right_menu = self.site.right_menu
        else:
            self.site.header.user_panel.my_account_button.click()
            right_menu = self.site.right_menu

        self.assertTrue(right_menu.is_displayed(), msg='Right menu failed to open')
        menu_items = right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Menu items not found in right menu')

        self.__class__.offers_title = self.site.window_client_config.offers_menu_title
        self.__class__.odds_boost_title = self.site.window_client_config.odds_boost_menu_title

        self.get_odds_boost_amount()

        # if actual number of oddsboost tokens is greater than expected, check that there are no other
        # active oddsboost offers in backoffice
        self.assertEqual(self.odds_boost_amount, self.expected_odds_boost_amount,
                         msg=f'Odds Boost amount equals "{self.odds_boost_amount}" '
                             f'but "{self.expected_odds_boost_amount}" is expected')

    def test_002_add_selection_to_the_betslip_boost_it_and_place_this_boosted_bet(self):
        """
        DESCRIPTION: Add selection to the Betslip, boost it and place this boosted bet.
        EXPECTED: Bet is placed successfully.
        """
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[self.selection_number])
        self.assertTrue(self.site.betslip.has_odds_boost_header, msg='Odds Boost header is not displayed on betslip')
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)
        odds_boost_header = self.site.betslip.odds_boost_header
        if odds_boost_header.boost_button.name != vec.odds_boost.BOOST_BUTTON.enabled:
            odds_boost_header.boost_button.click()
            result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                     name='"BOOST" button to become "BOOSTED" button with animation',
                                     timeout=2)
            self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        self.assertTrue(self.site.betslip.has_bet_now_button(), msg='Place Bet button is not present.')
        place_bet_button = self.site.betslip.bet_now_button
        self.assertTrue(place_bet_button.is_displayed(), msg='Place Bet button is not displayed.')
        self.assertTrue(place_bet_button.is_enabled(), msg='Place Bet button is not enabled.')
        place_bet_button.click()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

        self.__class__.expected_odds_boost_amount -= 1
        self.__class__.selection_number += 1

    def test_003_navigate_to_the_my_account_and_verify_that_sum_value_of_odds_boost_tokens_decreased_by_one(self):
        """
        DESCRIPTION: Navigate to the 'My account' and verify that sum value of Odds Boost tokens decreased by one.
        EXPECTED: Sum value of Odds Boost tokens is updated according to available number of Odds Boost tokens (decreased by one).
        """
        if self.device_type == 'mobile':
            self.site.header.right_menu_button.click()
            right_menu = self.site.right_menu
        else:
            self.site.header.user_panel.my_account_button.click()
            right_menu = self.site.right_menu

        self.assertTrue(right_menu.is_displayed(), msg='Right menu failed to open')

        self.get_odds_boost_amount()

        self.assertEqual(self.odds_boost_amount, self.expected_odds_boost_amount,
                         msg=f'Odds Boost amount equals "{self.odds_boost_amount}" '
                             f'but "{self.expected_odds_boost_amount}" is expected')

    def test_004_place_as_many_boosted_bets_as_there_are_number_of_odds_boost_tokens_available(self):
        """
        DESCRIPTION: Place as many boosted bets, as there are number of Odds Boost tokens available.
        EXPECTED: Bets are placed successfully.
        """
        for i in range(self.odds_boost_amount):
            self.__class__.expected_betslip_counter_value = 0
            self.test_002_add_selection_to_the_betslip_boost_it_and_place_this_boosted_bet()

    def test_005_navigate_to_the_my_account_and_verify_that_sum_value_of_odds_boost_tokens_isnt_shown(self):
        """
        DESCRIPTION: Navigate to the 'My account' and verify that sum value of Odds Boost tokens isn't shown.
        EXPECTED: * Right menu is expanded
        EXPECTED: * Odds Boost item is available in the menu
        EXPECTED: * No icon with Sum value of Odds Boost tokens is displayed
        """
        for i in range(self.odds_boost_amount):
            self.test_003_navigate_to_the_my_account_and_verify_that_sum_value_of_odds_boost_tokens_decreased_by_one()
