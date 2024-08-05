import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893153_Verify_the_Font_sizes_colors_font_family_shadows_on_different_elements_on_bet_tracker_page(Common):
    """
    TR_ID: C64893153
    NAME: Verify the Font sizes, colors, font family, shadows for different elements on bet tracker page
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports web
    PRECONDITIONS: application URL.
    """
    keep_browser_open = True

    def test_001_1_1verify_text_sizes_and_font_family2verify_the_image_sizes3verify_the_box_borders_and_shadows4verify_the_background5verify_the_color_codesexpected_resultshould_be_as_per_designs(self):
        """
        DESCRIPTION: 1. 1.Verify text sizes and font family
        DESCRIPTION: 2.Verify the image sizes
        DESCRIPTION: 3.Verify the box borders and shadows
        DESCRIPTION: 4.Verify the background
        DESCRIPTION: 5.Verify the color codes
        DESCRIPTION: Expected Result:
        DESCRIPTION: Should be as per designs
        EXPECTED: 1. Should be as per designs
        """
        self.site.wait_content_state(state_name="Homepage")
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
                      msg=f'Bet Tracker font family is not equal to Zepplin Font Family'
                          f' actual result "{header_font_type}"')
        header_font_color = self.site.bet_tracker.title_styles.css_property_value('color')
        self.assertIn(vec.colors.BET_TRACKER_TITLE_COLOR, header_font_color,
                      msg=f'Bet Tracker font family is not equal to Zepplin Font color'
                          f' actual result "{header_font_color}"')

        open_tab_font_size = self.site.bet_tracker.cash_out_block.shop_bet_tab_styles.css_property_value('font-size')
        self.assertEqual(open_tab_font_size, '12px',
                         msg=f'Bet Tracker tab menu font size is not equal to Zepplin Font Size'
                             f'actual result "{open_tab_font_size}"')
        open_tab_font_type = self.site.bet_tracker.cash_out_block.shop_bet_tab_styles.css_property_value('font-family')
        self.assertIn('Roboto Condensed', open_tab_font_type,
                      msg=f'Bet Tracker tab menu font type is not equal to Zepplin Font family'
                          f'actual result "{open_tab_font_type}"')
        open_tab_font_color = self.site.bet_tracker.cash_out_block.shop_bet_tab_styles.css_property_value('color')
        self.assertIn(vec.colors.BET_TRACKER_OPEN_TAB_COLOR, open_tab_font_color,
                      msg=f'Bet Tracker tab menu font type is not equal to Zepplin Font color'
                          f'actual result "{open_tab_font_color}"')

        settle_tab_font_size = self.site.bet_tracker.cash_out_block.settle_bet_tab_styles.css_property_value('font-size')
        self.assertEqual(settle_tab_font_size, '12px',
                         msg=f'Bet Tracker tab menu font size is not equal to Zepplin Font Size'
                             f'actual result "{settle_tab_font_size}"')
        settle_tab_font_type = self.site.bet_tracker.cash_out_block.settle_bet_tab_styles.css_property_value('font-family')
        self.assertIn('Roboto Condensed', settle_tab_font_type,
                      msg=f'Bet Tracker tab menu font type is not equal to Zepplin Font family'
                          f'actual result "{settle_tab_font_type}"')
        settle_tab_font_color = self.site.bet_tracker.cash_out_block.settle_bet_tab_styles.css_property_value('color')
        self.assertIn(vec.colors.BET_TRACKER_SETTLE_TAB_COLOR, settle_tab_font_color,
                      msg=f'Bet Tracker tab menu font type is not equal to Zepplin Font color'
                          f'actual result "{settle_tab_font_color}"')

        coupon_input_border = self.site.bet_tracker.coupon_input_styles.css_property_value('border')
        self.assertEqual(coupon_input_border, vec.colors.BET_TRACKER_INPUT_FIELD_BORDER,
                         msg=f'Bet Tracker input field is not equal to Zepplin Font Size'
                             f'actual result "{coupon_input_border}"')
        coupon_input_background_color = self.site.bet_tracker.coupon_input_styles.css_property_value('background-color')
        self.assertIn(vec.colors.BET_TRACKER_INPUT_FIELD_BG_COLOR, coupon_input_background_color,
                      msg=f'Bet Tracker background color is not equal to Zepplin input background color'
                          f' actual result "{coupon_input_background_color}"')

        track_button_border = self.site.bet_tracker.track_button_styles.css_property_value('border-radius')
        self.assertEqual(track_button_border, '0px',
                         msg=f'Bet Tracker track button field is not equal to Zepplin track button border'
                             f'actual result "{track_button_border}"')
        track_button_background_color = self.site.bet_tracker.track_button_styles.css_property_value('background-color')
        self.assertIn(vec.colors.BET_TRACKER_TRACK_BG_COLOR, track_button_background_color,
                      msg=f'Bet Tracker background color is not equal to Zepplin input background color'
                          f' actual result "{track_button_background_color}"')

        info_icon_background_color = self.site.bet_tracker.tracker_info_styles.css_property_value('background-color')
        self.assertIn(vec.colors.BET_TRACKER_INFO_ICON_BG_COLOR, info_icon_background_color,
                      msg=f'Bet Tracker info icon color is not equal to Zepplin info background color'
                          f' actual result "{info_icon_background_color}"')
