import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.grid
@vtest
class Test_C64893060_Verify_the_FCB_popup_default_selection_is_bet_in_shop_for_anonymous_user(Common):
    """
    TR_ID: C64893060
    NAME: Verify the FCB popup default selection is bet in shop for  anonymous user.
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_web_application2click_on_grid_tab_from_main_header3click_on_football_bet_filter_from_the_grid_hub_menu_items4check_the_default_selection_on_fcb_popupexpected_result1sports_web_application_should_be_launch2user_should_be_able_to_open_grid_tab_from_main_header3user_should_be_able_to_click_on_football_bet_filter4default_selection_should_be_bet_in_shop(self):
        """
        DESCRIPTION: 1. 1.Launch Ladbrokes sports web application.
        DESCRIPTION: 2.Click on grid tab from main header.
        DESCRIPTION: 3.Click on football bet filter from the Grid hub menu items.
        DESCRIPTION: 4.Check the default selection on FCB popup.
        EXPECTED: 1.Sports web application should be launch.
        EXPECTED: 2.User should be able to open grid tab from main header.
        EXPECTED: 3.User should be able to click on football bet filter.
        EXPECTED: 4.Default selection should be bet in shop.
        """
        self.site.wait_content_state('homepage')
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
        self.site.grid.menu_items.items_as_ordered_dict.get(vec.retail.FB_BET_FILTER_NAME).click()
        your_betting_popup = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_YOUR_BETTING)
        self.assertTrue(your_betting_popup, msg='"your Betting" popup not displayed')
        result = self.device.driver.execute_script("return window.getComputedStyle(document.querySelector('#football-filter-confirm-inshop'), '::before').getPropertyValue('content')")
        if result == 'none':
            raise VoltronException('"Bet In-shop" is not selected by default')
        else:
            self._logger.info('"Bet In-shop" is selected by default')
