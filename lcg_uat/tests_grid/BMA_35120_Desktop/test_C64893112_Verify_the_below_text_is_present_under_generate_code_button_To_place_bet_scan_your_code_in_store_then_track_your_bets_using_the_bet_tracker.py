import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893112_Verify_the_below_text_is_present_under_generate_code_button_To_place_bet_scan_your_code_in_store_then_track_your_bets_using_the_bet_tracker_Odds_may_change_at_time_of_bet_placement(Common):
    """
    TR_ID: C64893112
    NAME: Verify the below text is present under generate code button " To place bet scan your code in-store, then track your bets using the bet tracker. Odds may change at time of bet placement"
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_digital_coupons_from_the_grid_hub_menu_itemsexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_see_the_below_text_under_generate_code_button___to_place_bet_scan_your_code_in_store_then_track_your_bets_using_the_bet_tracker_odds_may_change_at_time_of_bet_placement(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should see the below text under generate code button . " To place bet scan your code in-store, then track your bets using the bet tracker. Odds may change at time of bet placement"
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should see the below text under generate code button . " To place bet scan your code in-store, then track your bets using the bet tracker. Odds may change at time of bet placement"
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.open_sport(name=vec.retail.TITLE)
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.login()
        self.site.wait_content_state(state_name='thegrid')
        grid_items = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_items, msg='"Grid" page items not loaded')
        in_shop_coupons = grid_items.get(vec.retail.IN_SHOP_COUPONS)
        in_shop_coupons.click()
        self.site.wait_content_state(state_name='InShopCoupons')
        footer_text = self.site.in_shop_coupons.footer_text
        footer_text.scroll_to()
        self.assertTrue(footer_text.is_displayed(), msg=f'Footer text: "{vec.retail.FOOTER_TEXT_DIGITAL_COUPONS_PAGE}" is not displayed')
        self.assertEqual(footer_text.text, vec.retail.FOOTER_TEXT_DIGITAL_COUPONS_PAGE,
                         msg=f'Actual footer text: "{footer_text.text}" is not same as Expected footer text: "{vec.retail.FOOTER_TEXT_DIGITAL_COUPONS_PAGE}"')
