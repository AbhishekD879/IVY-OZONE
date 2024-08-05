import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893019_Verify_the_static_text_displayed_under_the_FCB_pop_up_options_1inshop_betting_2Online(Common):
    """
    TR_ID: C64893019
    NAME: Verify the static text displayed under the FCB pop up options 1.inshop betting 2.Online
    PRECONDITIONS: 1.User should have valid ladbrokes sports URL/App URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_urlapp2click_on_grid_tab_from_sports_main_header3click_on_football_bet_filter__from_the_grid_main_menu4verify_the_text_displayed_under_the_options1bet_inshop2bet_onlineexpected_resultfor_bet_inshop__generate_barcode_to_bet_inshop__should_be_selectedfor_bet_online__bet_online_to_place_a_bet_online_should_be_displayed(self):
        """
        DESCRIPTION: 1.Launch ladbrokes sports URL/App.
        DESCRIPTION: 2.Click on grid tab from sports main header
        DESCRIPTION: 3.Click on Football bet filter  from the grid main menu.
        DESCRIPTION: 4.Verify the text displayed under the options
        DESCRIPTION: 1.Bet inshop
        DESCRIPTION: 2.Bet online
        EXPECTED: 1. For Bet inshop "Build your coupon now and place your bet later in your Ladbrokes shop." should be selected
        EXPECTED: For Bet online "Build your coupon, add your selections to your betslip, place and track your bets, all online." should be displayed
        """
        self.site.wait_content_state("Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        grid_menu = self.site.grid.menu_items.items_as_ordered_dict
        self.assertTrue(grid_menu, msg='"Grid" page items not loaded')
        grid_menu.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        your_betting_options = your_betting_popup.items_as_ordered_dict
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop, your_betting_options,
                      msg='"Bet in shop" is not displayed')
        self.assertIn(vec.retail.EXPECTED_YOUR_BETTING.bet_online, your_betting_options,
                      msg='"Bet online" is not displayed')
        bet_inshop_text = your_betting_options[vec.retail.EXPECTED_YOUR_BETTING.bet_in_shop].filter_text
        bet_online_text = your_betting_options[vec.retail.EXPECTED_YOUR_BETTING.bet_online].filter_text
        self.assertEqual(bet_inshop_text, vec.retail.BET_IN_SHOP_TEXT,
                         msg=f'Actual text "{bet_inshop_text}" is not matching with expected text "{vec.retail.BET_IN_SHOP_TEXT}"')
        self.assertEqual(bet_online_text, vec.retail.BET_ONLINE_TEXT,
                         msg=f'Actual text "{bet_online_text}" is not matching with expected text "{vec.retail.BET_ONLINE_TEXT}"')
