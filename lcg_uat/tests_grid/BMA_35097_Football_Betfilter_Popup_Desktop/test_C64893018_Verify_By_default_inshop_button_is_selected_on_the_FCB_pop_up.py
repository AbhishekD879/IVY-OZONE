import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.grid
@pytest.mark.desktop
@vtest
class Test_C64893018_Verify_By_default_inshop_button_is_selected_on_the_FCB_pop_up(Common):
    """
    TR_ID: C64893018
    NAME: Verify By default inshop button is selected on the FCB pop up
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid ladbrokes sports URL/App URL.
    """
    keep_browser_open = True

    def test_001_1_1launch_ladbrokes_sports_urlapp2click_on_grid_tab_from_sports_main_header3click_on_football_bet_filter__from_the_grid_main_menu4verify_by_default_inshop_pop_up_is_selectedexpected_resultby_default_bet_inshop_option_should_be_selected_on_the_fcb_pop_up(self):
        """
        DESCRIPTION: 1. 1.Launch ladbrokes sports URL/App.
        DESCRIPTION: 2.Click on grid tab from sports main header
        DESCRIPTION: 3.Click on Football bet filter  from the grid main menu.
        DESCRIPTION: 4.Verify by default inshop pop up is selected
        DESCRIPTION: Expected Result:
        DESCRIPTION: By default 'bet inshop' option should be selected on the FCB pop up
        EXPECTED: 1. By default 'bet inshop' option should be selected on the FCB pop up
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
        result = self.device.driver.execute_script(
            "return window.getComputedStyle(document.querySelector('#football-filter-confirm-inshop'), '::before').getPropertyValue('content')")
        if result == 'none':
            raise VoltronException('"Bet In-shop" option is not selected by default')
        else:
            self._logger.info('"Bet In-shop" option is selected by default')
