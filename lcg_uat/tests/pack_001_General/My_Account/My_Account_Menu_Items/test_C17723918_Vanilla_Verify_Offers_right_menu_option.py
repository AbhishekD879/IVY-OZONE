import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


# @pytest.mark.tst2
# @pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.medium
@pytest.mark.portal_only_test
@pytest.mark.navigation
@pytest.mark.desktop
@vtest
class Test_C17723918_Vanilla_Verify_Offers_right_menu_option(Common):
    """
    TR_ID: C17723918
    NAME: [Vanilla] Verify Offers right menu option
    DESCRIPTION: This test case is to verify all option menus under Offers&Free bets right menu option
    PRECONDITIONS: User has account on QA env
    """
    keep_browser_open = True

    def test_001_log_in_to_test_env(self):
        """
        DESCRIPTION: Log in to test env
        EXPECTED: User is logged in, My Account button appears
        """
        self.site.wait_content_state("HomePage")
        self.site.login()

    def test_002_clicktap_my_account_button(self):
        """
        DESCRIPTION: Click/tap My Account button
        EXPECTED: Right menu is displayed
        """
        self.assertTrue(self.site.header.right_menu_button, msg='"Right menu" is not displayed')
        self.site.header.right_menu_button.click()
        self.site.wait_content_state_changed()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')

    def test_003_clicktap_offersfree_bets_menu_option(self):
        """
        DESCRIPTION: Click/tap Offers&Free bets menu option
        EXPECTED: Offers&Free bets menu is displayed with the following options:
        EXPECTED: - Odds Boost
        EXPECTED: - Sports free bets
        EXPECTED: - Sports promotions
        EXPECTED: - Games promotions
        EXPECTED: - Voucher codes
        """
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
        self.site.wait_content_state_changed(timeout=15)
        self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1],
                         msg='"Offers & Free Bets Menu" is not displayed')
        offers_freebets_menu_actual = list(self.site.right_menu.items_as_ordered_dict)
        offers_freebets_menu_expected = vec.bma.OFFERS_FREE_BETS_MENU_ITEMS if self.brand == 'bma' \
            else vec.bma.PROMOTIONS_MENU_ITEMS
        self.assertEqual(offers_freebets_menu_actual, offers_freebets_menu_expected,
                         msg=f'Actual items: "{offers_freebets_menu_actual}" are not equal with the'
                             f'Expected items: "{offers_freebets_menu_expected}"')

    def test_004_clicktap_odds_boost_option(self):
        """
        DESCRIPTION: Click/tap Odds Boost option
        EXPECTED: Odds boost page is displayed with the following information:
        EXPECTED: - Today's Odds Boost
        EXPECTED: - Boosts available now
        EXPECTED: - Upcoming boosts
        EXPECTED: - Terms and conditions
        """
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[0])
        else:
            self.site.right_menu.click_item(vec.bma.PROMOTIONS_MENU_ITEMS[1])
        self.site.wait_content_state(state_name='oddsboost')
        odds_boost_menu = list(self.site.odds_boost_page.sections.items_as_ordered_dict.keys())
        odds_boost_menu_actual = [item.lower() for item in odds_boost_menu]
        odds_boost_menu_expected = [item.lower() for item in vec.bma.ODDS_BOOST_MENU_ITEMS]
        self.assertEqual(odds_boost_menu_actual, odds_boost_menu_expected,
                         msg=f'Actual items: "{odds_boost_menu_actual}" are not equal with the'
                             f'Expected items: "{odds_boost_menu_expected}"')

    def test_005_reopen_right_menu__offersfree_bets_and_clicktap_sports_free_bets_option(self):
        """
        DESCRIPTION: Reopen right menu-> Offers&Free bets and click/tap Sports free bets option
        EXPECTED: User is taken to My freebets/bonuses page
        EXPECTED: Page contains the list of all freebets available to the user.
        """
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
        wait_for_result(lambda: self.site.right_menu.header.title == vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1],
                        name='Waiy for "Offers&Free bets" title',
                        timeout=15)
        self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1],
                         msg='"Offers & Free Bets Menu" is not displayed')

        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[1])
        else:
            self.site.right_menu.click_item(vec.bma.PROMOTIONS_MENU_ITEMS[0])
        self.site.wait_content_state_changed(timeout=15)
        page_title = self.site.freebets.header_line.page_title.text
        if self.brand == 'bma':
            self.assertEqual(page_title, vec.bma.FREEBETS.upper(),
                             msg=f'MY FREE BETS/BONUSES "{page_title}" title is not '
                                 f'equal to the "{vec.bma.FREEBETS.upper()}"')
        else:
            self.assertEqual(page_title, vec.bma.FREE_BET.upper(), msg=f'FREE BET "{page_title}" title is not equal '
                                                                       f'to the "{vec.bma.FREE_BET.upper()}"')
        self.assertTrue(self.site.freebets.freebets_content, msg='List of Freebets not available')

    def test_006_reopen_right_menu__offersfree_bets_and_clicktap_sports_promotions_option(self):
        """
        DESCRIPTION: Reopen right menu-> Offers&Free bets and click/tap Sports promotions option
        EXPECTED: User is taken to My Promotions page with the list of all promotions available to the user
        """
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
        wait_for_result(lambda: self.site.right_menu.header.title == vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1],
                        name='Waiy for "Offers&Free bets" title',
                        timeout=15)
        self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1],
                         msg='"Offers & Free Bets Menu" is not displayed')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[2])
        else:
            self.site.right_menu.click_item(vec.bma.PROMOTIONS_MENU_ITEMS[2])
        self.site.wait_content_state(state_name='Promotions')
        promotions = self.site.promotions.tab_content.items_as_ordered_dict
        self.assertTrue(promotions, msg='No promotions found on page')

    def test_007_reopen_right_menu__offersfree_bets_and_clicktap_games_promotions_option(self):
        """
        DESCRIPTION: Reopen right menu-> Offers&Free bets and click/tap Games promotions option
        EXPECTED: User is taken to My Offers page
        """
        self.site.header.right_menu_button.click()
        self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
        wait_for_result(lambda: self.site.right_menu.header.title == vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1],
                        name='Waiy for "Offers&Free bets" title',
                        timeout=15)
        self.assertEqual(self.site.right_menu.header.title.lower(), vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1].lower(),
                         msg='"Offers & Free Bets Menu" is not displayed')
        if self.brand == 'bma':
            self.site.right_menu.click_item(vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[3])
        else:
            self.site.right_menu.click_item(vec.bma.PROMOTIONS_MENU_ITEMS[3])
        self.site.wait_content_state_changed(timeout=15)
        current_url = self.device.get_current_url()
        self.assertIn('promo/offers', current_url, msg='"My Offers" page not found')

    def test_008_reopen_right_menu__offers_and_clicktap_voucher_codes_option(self):
        """
        DESCRIPTION: Reopen right menu-> Offers and click/tap Voucher codes option
        EXPECTED: User is taken to Redeem Voucher page
        """
        if self.brand == 'bma':
            self.site.header.right_menu_button.click()
            self.site.right_menu.click_item(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
            wait_for_result(lambda: self.site.right_menu.header.title == vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1],
                            name='Waiy for "Offers&Free bets" title',
                            timeout=15)
            self.assertEqual(self.site.right_menu.header.title, vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1],
                             msg='"Offers & Free Bets Menu" is not displayed')
            self.site.right_menu.click_item(vec.bma.OFFERS_FREE_BETS_MENU_ITEMS[4])
            self.site.wait_content_state_changed(timeout=15)
            page_title = self.site.voucher_code.header_line.page_title.text.lower()
            self.assertEqual(page_title, vec.betslip.VOUCHER_FORM.lower(),
                             msg=f'Actual Page Tile "{page_title}" is not equal to the '
                                 f'expected title "{vec.betslip.VOUCHER_FORM.lower()}"')
