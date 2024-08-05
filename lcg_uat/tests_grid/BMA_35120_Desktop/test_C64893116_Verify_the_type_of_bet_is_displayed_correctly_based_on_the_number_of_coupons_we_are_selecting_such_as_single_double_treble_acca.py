import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893116_Verify_the_type_of_bet_is_displayed_correctly_based_on_the_number_of_coupons_we_are_selecting_such_as_single_doubletrebleacca(Common, ComponentBase):
    """
    TR_ID: C64893116
    NAME: Verify the type of bet is displayed correctly based on the number of coupons we are selecting such as single, double,treble,acca
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True
    bet_types = [vec.bet_finder.FB_BET_FILTER_SINGLE.title(), vec.bet_finder.FB_BET_FILTER_DOUBLE.title(),
                 vec.bet_finder.FB_BET_FILTER_TREBLE.title(), vec.bet_finder.FB_BET_FILTER_FOURFOLD.title()]

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_digital_coupons_from_the_grid_hub_menu_items4select_few_selections_and_check_the_bet_type_at_the_bottomexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_digital_coupons_and__open_digital_coupons_page4by_changing_the_selections_bet_type_should_changeexample_if_you_select_3_selections_then_it_should_show_treble_bet(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: 4.Select few selections and check the bet type at the bottom.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should be able to click on digital coupons and  open digital coupons page.
        DESCRIPTION: 4.By changing the selections bet type should change
        DESCRIPTION: Example: if you select 3 selections then it should show treble bet.
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on digital coupons and  open digital coupons page.
        EXPECTED: 4.By changing the selections bet type should change
        EXPECTED: Example: if you select 3 selections then it should show treble bet.
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

        self.sections = self.site.in_shop_coupons.tab_content.accordions_list.items_as_ordered_dict
        count = 0
        try:
            for section in self.sections.values():
                events = section.items_as_ordered_dict
                event = list(events.values())[0]
                selections = event.selections
                self.scroll_to_we(selections[0])
                selections[0].click()
                self.site.in_shop_coupons.footer_text.scroll_to()
                generate_bet_frame = self.site.in_shop_coupons.tab_content.generate_bet_frame
                self.assertTrue(generate_bet_frame.bet_type.is_displayed(),
                                msg=f'Bet type: "{generate_bet_frame.bet_type.text} is not displayed')
                self.assertEqual(generate_bet_frame.bet_type.text, self.bet_types[count],
                                 msg=f'Actual Bet type:"{generate_bet_frame.bet_type.text}" is not same as Expected Bet type:"{self.bet_types[count]}"')
                if count == 4:
                    break
                count += 1
                self.sections = self.site.in_shop_coupons.tab_content.accordions_list.items_as_ordered_dict
        except IndexError:
            self._logger.info(f'*** Sections are insufficient. Exoected number of sections are: "4", found: "{len(self.sections)}"')
