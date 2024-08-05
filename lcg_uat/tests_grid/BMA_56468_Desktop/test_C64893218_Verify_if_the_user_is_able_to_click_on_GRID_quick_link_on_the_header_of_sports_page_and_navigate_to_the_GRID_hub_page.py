import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.grid
@vtest
class Test_C64893218_Verify_if_the_user_is_able_to_click_on_GRID_quick_link_on_the_header_of_sports_page_and_navigate_to_the_GRID_hub_page(Common):
    """
    TR_ID: C64893218
    NAME: Verify if the user is able to click on
    GRID quick link on the header of sports page and navigate to the GRID hub page.
    DESCRIPTION:
    PRECONDITIONS: 1.User should have valid Ladbrokes sports URL.
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_sports_url2_click_on_grid_quick_link_on_the_headerexpected_result1sports_application_should_be_launched_successfully2user_should_be_able_to_click_on_the_grid_quick_link_and_navigate_to_the_grid_hub__page(self):
        """
        DESCRIPTION: 1. 1. Launch Ladbrokes sports URL.
        DESCRIPTION: 2. Click on grid quick link on the header.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1.Sports application should be launched successfully.
        DESCRIPTION: 2.User should be able to click on the grid quick link and navigate to the GRID HUB  page.
        EXPECTED: 1. 1.Sports application should be launched successfully.
        EXPECTED: 2.User should be able to click on the grid quick link and navigate to the GRID HUB  page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE.title()).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='thegrid')
