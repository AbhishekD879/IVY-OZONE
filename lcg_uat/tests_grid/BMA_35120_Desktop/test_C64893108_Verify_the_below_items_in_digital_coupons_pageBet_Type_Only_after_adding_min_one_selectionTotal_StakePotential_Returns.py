import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893108_Verify_the_below_items_in_digital_coupons_pageBet_Type_Only_after_adding_min_one_selectionTotal_StakePotential_Returns(Common, ComponentBase):
    """
    TR_ID: C64893108
    NAME: Verify the below items in digital coupons page
    Bet Type ( Only after adding min one selection)
    Total Stake
    Potential Returns
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    PRECONDITIONS: 2.User should have valid online users.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application_and_login_with_valid_user_credentials2click_on_grid_tab_from_main_header3click_on_digital_coupons_from_the_grid_hub_menu_itemsexpected_result1sports_web_application_should_be_launch_2user_should_be_able_to_open_grid_tab_from_main_header3user_should_see_the_below_items_in_digital_coupons_page_at_the_bottom_1bet_type__only_after_adding_min_one_selection2total_stake3potential_returns(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application and login with valid user credentials.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on digital coupons from the Grid hub menu items.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports web application should be launch .
        DESCRIPTION: 2.User should be able to open grid tab from main header.
        DESCRIPTION: 3.User should see the below items in digital coupons page at the bottom .
        DESCRIPTION: 1.Bet Type ( Only after adding min one selection)
        DESCRIPTION: 2.Total Stake
        DESCRIPTION: 3.Potential Returns
        EXPECTED: 1. 1.Sports web application should be launch .
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should see the below items in digital coupons page at the bottom .
        EXPECTED: 1.Bet Type ( Only after adding min one selection)
        EXPECTED: 2.Total Stake
        EXPECTED: 3.Potential Returns
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

        sections = self.site.in_shop_coupons.tab_content.accordions_list.items_as_ordered_dict
        section = list(sections.values())[0]
        events = section.items_as_ordered_dict
        event = list(events.values())[0]
        selections = event.selections
        self.scroll_to_we(selections[0])
        selections[0].click()
        self.site.in_shop_coupons.footer_text.scroll_to()
        generate_bet_frame = self.site.in_shop_coupons.tab_content.generate_bet_frame
        self.assertTrue(generate_bet_frame.bet_type.is_displayed(), msg=f'Bet type: "{generate_bet_frame.bet_type.text} is not displayed')
        self.assertTrue(generate_bet_frame.get_stake_value, msg='Stake value in the stake field is not displayed')
        self.assertTrue(generate_bet_frame.potential_returns.is_displayed(), msg='Potential returns value is not displayed()')
