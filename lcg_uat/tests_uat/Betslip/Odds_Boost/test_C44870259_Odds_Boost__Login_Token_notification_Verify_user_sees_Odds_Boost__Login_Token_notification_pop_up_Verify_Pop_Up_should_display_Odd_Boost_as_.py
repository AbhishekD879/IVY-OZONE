import pytest
import tests
from time import sleep
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
# @pytest.mark.prod  # Can not be tested in prod/beta as it requires to create Odds Boost offer in OB and trigger the popup after login
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870259_Odds_Boost__Login_Token_notification_Verify_user_sees_Odds_Boost__Login_Token_notification_pop_up_Verify_Pop_Up_should_display_Odd_Boost_as_header__Verify_Youve_xx_odds_Boost_available_Verify_all_buttons_on_the_notification_pop_up(Common):
    """
    TR_ID: C44870259
    NAME: "Odds Boost - Login Token notification -Verify user sees Odds Boost - Login Token notification pop up -Verify Pop Up  should display ""Odd Boost ""as header - Verify ""You've (xx) odds Boost available"" -Verify all buttons on the notification pop up
    DESCRIPTION: "Odds Boost - Login Token notification
    DESCRIPTION: -Verify user sees Odds Boost - Login Token notification pop up
    DESCRIPTION: -Verify Pop Up  should display ""Odd Boost ""as header
    DESCRIPTION: - Verify ""You've (xx) odds Boost available""
    DESCRIPTION: -Verify all buttons on the notification pop up (show more, Ok Thanks, Close etc)
    DESCRIPTION: -Verify tapping on ""Okay, Thanks "" button or anywhere outside Pop up, the pop up should be dismissed
    DESCRIPTION: - Verify 'Show More' takes user to Odds Boost - Detail Page
    """
    keep_browser_open = True

    def test_001_verify_user_sees_odds_boost___login_token_notification_pop_upverify_pop_up__should_display_odd_boost_as_header(self):
        """
        DESCRIPTION: Verify user sees Odds Boost - Login Token notification pop up
        DESCRIPTION: Verify Pop Up  should display ""Odd Boost ""as header
        EXPECTED: Login Token notification pop up should be displayed
        EXPECTED: Odds Boost  notification  popup with the buttons like show more, Ok Thanks, Close etc are displayed
        """
        username = tests.settings.odds_boost_user
        self.site.login(username=username, ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.assertTrue(self.dialog, msg=f'"{vec.odds_boost._tokens_info_dialog_title}" login token notification popup is not displayed')
        if self.brand == 'bma':
            self.assertEqual(self.dialog.name, vec.odds_boost._tokens_info_dialog_title.upper(),
                             msg=f'Odds boost header "{self.dialog.name}" is not same as "{vec.odds_boost._tokens_info_dialog_title.upper()}"')
        else:
            self.assertEqual(self.dialog.name, vec.odds_boost._tokens_info_dialog_title,
                             msg=f'Odds boost header "{self.dialog.name}" is not same as "{vec.odds_boost._tokens_info_dialog_title}"')
        odds_boost_content = (self.dialog.description).split('\n')
        self.assertIn(vec.odds_boost._tokens_info_dialog_show_more.upper(), odds_boost_content,
                      msg=f'Odds boost Show More "{vec.odds_boost._tokens_info_dialog_show_more.upper()}" is not available in "{odds_boost_content}"')
        self.assertIn(vec.odds_boost._tokens_info_dialog_ok_thanks.upper(), odds_boost_content,
                      msg=f'Odds boost NO, THANKS "{vec.odds_boost._tokens_info_dialog_ok_thanks.upper()}" is not available in "{odds_boost_content}"')
        self.assertTrue(self.dialog.header_object.close_button.is_displayed(),
                        'Close button is not displayed on Odds Boost header')

    def test_002_verify_show_more_takes_user_to_odds_boost___detail_page(self):
        """
        DESCRIPTION: Verify 'Show More' takes user to Odds Boost - Detail Page
        EXPECTED: Show more text takes the user to the odds boost detail page
        """
        self.dialog.show_more_button.click()
        self.site.wait_content_state(vec.odds_boost.PAGE.title)

    def test_003_navigate_to_my_accounts__offers__free_bets__odds_boost(self):
        """
        DESCRIPTION: Navigate to 'My accounts' > Offers & Free bets > Odds boost
        EXPECTED: My account' (User menu) menu is expanded > Offer & Free bets
        EXPECTED: Odds Boost item is available in the menu
        EXPECTED: Summary value 1 of the number of Odds Boost tokens is displaying in Odds Boost item
        """
        self.site.go_to_home_page()
        self.site.header.right_menu_button.click()
        self.assertTrue(self.site.is_right_menu_opened(), msg='"Right menu" is not opened')
        menu_items = self.site.right_menu.items_as_ordered_dict
        self.assertTrue(menu_items, msg='Right menu items not found')
        self.assertIn(vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1], menu_items.keys(),
                      msg=f'"{vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1]}" not present in the Right menu "{menu_items.keys()}"')
        self.site.right_menu.click_item(item_name=vec.bma.EXPECTED_LIST_OF_RIGHT_MENU[1])
        sleep(1)
        sub_menu_items = self.site.right_menu.items_as_ordered_dict
        if self.brand == 'bma':
            self.assertTrue(sub_menu_items, msg='"OFFERS & Free Bets" menu has no items available.')
            self.assertIn(vec.odds_boost._tokens_info_dialog_title.upper(), sub_menu_items.keys(),
                          msg=f'"ODDS BOOST" not present in OFFERS & FREE BETS menu "{sub_menu_items.keys()}"')
            odds_boost_content = sub_menu_items.get(vec.odds_boost._tokens_info_dialog_title.upper())
            self.assertTrue(odds_boost_content.badge_text, msg='Odds boost badge count is not displayed')
            self.site.right_menu.click_item(item_name=vec.odds_boost._tokens_info_dialog_title.upper())
        else:
            self.assertTrue(sub_menu_items, msg='"Promotions" menu has no items available.')
            self.assertIn(vec.bma.PROMOTIONS_MENU_ITEMS[1], sub_menu_items.keys(),
                          msg=f'"Odds Boosts" not present in Promotions menu "{sub_menu_items.keys()}"')
            odds_boost_content = sub_menu_items.get(vec.bma.PROMOTIONS_MENU_ITEMS[1])
            self.assertTrue(odds_boost_content.badge_text, msg='Odds boost badge count is not displayed')
            self.site.right_menu.click_item(item_name=vec.bma.PROMOTIONS_MENU_ITEMS[1])
        self.site.wait_content_state(vec.odds_boost.PAGE.title)
