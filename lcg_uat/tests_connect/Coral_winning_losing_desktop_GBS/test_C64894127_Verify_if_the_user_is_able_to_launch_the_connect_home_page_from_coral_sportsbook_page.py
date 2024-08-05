import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.connect
@vtest
class Test_C64894127_Verify_if_the_user_is_able_to_launch_the_connect_home_page_from_coral_sportsbook_page(Common):
    """
    TR_ID: C64894127
    NAME: Verify if the user is able to launch the connect home page from coral sportsbook page.
    PRECONDITIONS: 1. User should have valid coral sportsbook URL.
    """
    keep_browser_open = True

    def test_001_1_1_1_launch_coral_sports_url2_click_on_connect_from_the_header_menuexpected_result1_sports_application_should_be_launch_successfully2_user_should_be_landed_on_connect_home_pageexpected_result1_1_sports_application_should_be_launch_successfully2_user_should_be_landed_on_connect_home_page(self):
        """
        DESCRIPTION: 1. 1. 1. Launch coral sports URL.
        DESCRIPTION: 2. Click on connect from the header menu.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. Sports application should be launch successfully.
        DESCRIPTION: 2. User should be landed on connect home page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. 1. Sports application should be launch successfully.
        DESCRIPTION: 2. User should be landed on connect home page.
        EXPECTED: 1. 1. 1. Sports application should be launch successfully.
        EXPECTED: 2. User should be landed on connect home page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='connect')
