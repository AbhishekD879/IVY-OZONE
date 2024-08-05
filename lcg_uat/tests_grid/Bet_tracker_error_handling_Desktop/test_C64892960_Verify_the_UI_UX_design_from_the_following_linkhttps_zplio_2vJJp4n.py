import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64892960_Verify_the_UI_UX_design_from_the_following_linkhttps_zplio_2vJJp4n(Common):
    """
    TR_ID: C64892960
    NAME: Verify the UI/UX design from the following link.
    https://zpl.io/2vJJp4n
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online/in shop user login Credentials.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_application_and_login_with_valid_onlinein_shop_user2click_on_grid_tab_from_header_menu3click_on_bet_tracker_from_grid_hub_menu_items_listexpected_result1sports_web_application_should_be_launched2user_should_be_able_to_click_on_grid_tab_and_should_be_landed_on_grid_hub_menu3user_should_be_able_to_click_on_bet_tracker_from_grid_hub_menu_items_and_should_be_landed_on_bet_tracker_page_and_check_the_uiux_from_the_following_link_httpszplio2vjjp4n(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports application and login with valid online/in shop user.
        DESCRIPTION: 2.Click on grid tab from header menu.
        DESCRIPTION: 3.Click on bet tracker from grid hub menu items list.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launched.
        DESCRIPTION: 2.User should be able to click on grid tab and should be landed on grid hub menu.
        DESCRIPTION: 3.User should be able to click on bet tracker from grid hub menu items and should be landed on bet tracker page and check the UI/UX from the following link https://zpl.io/2vJJp4n
        EXPECTED: 1. 1.Sports web application should be launched.
        EXPECTED: 2.User should be able to click on grid tab and should be landed on grid hub menu.
        EXPECTED: 3.User should be able to click on bet tracker from grid hub menu items and should be landed on bet tracker page and check the UI/UX from the following link https://zpl.io/2vJJp4n
        """
        self.site.login()
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        grid_items.get(vec.retail.BET_TRACKER.title()).click()
        self.site.wait_content_state(state_name='BetTracker', timeout=30)
        actual_title = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_title, vec.retail.BET_TRACKER.title(),
                         msg=f'Actual Title: "{actual_title}" is not same as expected "{vec.retail.BET_TRACKER.title()}"')
        wait_for_result(lambda: self.site.bet_tracker.page_title.is_displayed(),
                        name='Bet Tracker header is not loaded',
                        timeout=20)
        header_font_size = self.site.bet_tracker.title_styles.css_property_value('font-size')
        self.assertEqual(header_font_size, '14px',
                         msg=f'Bet Tracker font size is not equal to Zepplin Font Size'
                             f'actual result "{header_font_size}"')
        header_font_type = self.site.bet_tracker.title_styles.css_property_value('font-family')
        self.assertIn('Helvetica Neue', header_font_type,
                      msg=f'Bet Tracker font family is not equal to Zeplin Font Family'
                          f' actual result "{header_font_type}"')
        header_font_color = self.site.bet_tracker.title_styles.css_property_value('color')
        self.assertIn(vec.colors.BET_TRACKER_TITLE_COLOR, header_font_color,
                      msg=f'Bet Tracker font family is not equal to Zeplin Font color'
                          f' actual result "{header_font_color}"')

        open_bets_tab_font_size = self.site.bet_tracker.cash_out_block.shop_bet_tab_styles.css_property_value('font-size')
        self.assertEqual(open_bets_tab_font_size, '12px',
                         msg=f'Bet Tracker tab menu font size is not equal to Zeplin Font Size'
                             f'actual result "{open_bets_tab_font_size}"')
        open_bets_tab_font_type = self.site.bet_tracker.cash_out_block.shop_bet_tab_styles.css_property_value('font-family')
        self.assertIn('Roboto Condensed', open_bets_tab_font_type,
                      msg=f'Bet Tracker tab menu font type is not equal to Zeplin Font family'
                          f'actual result "{open_bets_tab_font_type}"')
        open_bets_tab_font_color = self.site.bet_tracker.cash_out_block.shop_bet_tab_styles.css_property_value('color')
        self.assertIn(vec.colors.BET_TRACKER_OPEN_TAB_COLOR, open_bets_tab_font_color,
                      msg=f'Bet Tracker tab menu font type is not equal to Zeplin Font color'
                          f'actual result "{open_bets_tab_font_color}"')

        settled_tab_font_size = self.site.bet_tracker.cash_out_block.settle_bet_tab_styles.css_property_value(
            'font-size')
        self.assertEqual(settled_tab_font_size, '12px',
                         msg=f'Bet Tracker tab menu font size is not equal to Zeplin Font Size'
                             f'actual result "{settled_tab_font_size}"')
        settled_tab_font_type = self.site.bet_tracker.cash_out_block.settle_bet_tab_styles.css_property_value(
            'font-family')
        self.assertIn('Roboto Condensed', settled_tab_font_type,
                      msg=f'Bet Tracker tab menu font type is not equal to Zeplin Font family'
                          f'actual result "{settled_tab_font_type}"')
        settled_tab_font_color = self.site.bet_tracker.cash_out_block.settle_bet_tab_styles.css_property_value('color')
        self.assertIn(vec.colors.BET_TRACKER_SETTLE_TAB_COLOR, settled_tab_font_color,
                      msg=f'Bet Tracker tab menu font type is not equal to Zeplin Font color'
                          f'actual result "{settled_tab_font_color}"')

        coupon_input_border = self.site.bet_tracker.coupon_input_styles.css_property_value('border')
        self.assertEqual(coupon_input_border, vec.colors.BET_TRACKER_INPUT_FIELD_BORDER,
                         msg=f'Bet Tracker input field is not equal to Zeplin Font Size'
                             f'actual result "{coupon_input_border}"')
        coupon_input_background_color = self.site.bet_tracker.coupon_input_styles.css_property_value('background-color')
        self.assertIn(vec.colors.BET_TRACKER_INPUT_FIELD_BG_COLOR, coupon_input_background_color,
                      msg=f'Bet Tracker background color is not equal to Zeplin input background color'
                          f' actual result "{coupon_input_background_color}"')

        track_button_border = self.site.bet_tracker.track_button_styles.css_property_value('border-radius')
        self.assertEqual(track_button_border, '0px',
                         msg=f'Bet Tracker track button field is not equal to Zeplin track button border'
                             f'actual result "{track_button_border}"')
        track_button_background_color = self.site.bet_tracker.track_button_styles.css_property_value('background-color')
        self.assertIn(vec.colors.BET_TRACKER_TRACK_BG_COLOR, track_button_background_color,
                      msg=f'Bet Tracker background color is not equal to Zeplin input background color'
                          f' actual result "{track_button_background_color}"')

        info_icon_background_color = self.site.bet_tracker.tracker_info_styles.css_property_value('background-color')
        self.assertIn(vec.colors.BET_TRACKER_INFO_ICON_BG_COLOR, info_icon_background_color,
                      msg=f'Bet Tracker info icon color is not equal to Zeplin info background color'
                          f' actual result "{info_icon_background_color}"')
