import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2
@pytest.mark.crl_stg2
@pytest.mark.crl_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.connect
@vtest
class Test_C64894034_Verify_if_the_user_is_able_to_launch_the_connect_shop_bet_tracker_page_from_sportsbook(Common):
    """
    TR_ID: C64894034
    NAME: Verify if the user is able to launch the connect shop bet tracker page from sportsbook.
    DESCRIPTION:
    PRECONDITIONS: 1. User should have valid sportsbook URL.
    """
    keep_browser_open = True

    def test_001_1_1_1_launch_the_sportsbook2_click_on_connect_from_header_menu3_click_on_shop_bet_trackerexpected_result1_user_should_be_able_to_launch_the_sportsbook_url2_user_should_be_able_to_click_on_connect_icon3_user_should_be_landed_on_shop_bet_tracker_pageexpected_result1_1_user_should_be_able_to_launch_the_sportsbook_url2_user_should_be_able_to_click_on_connect_icon3_user_should_be_landed_on_shop_bet_tracker_page(self):
        """
        DESCRIPTION: 1. 1. 1. Launch the sportsbook.
        DESCRIPTION: 2. Click on connect from header menu.
        DESCRIPTION: 3. Click on Shop bet tracker.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. User should be able to launch the sportsbook URL
        DESCRIPTION: 2. User should be able to click on connect icon.
        DESCRIPTION: 3. User should be landed on shop bet tracker page.
        DESCRIPTION: Expected Result:
        DESCRIPTION: 1. 1. User should be able to launch the sportsbook URL
        DESCRIPTION: 2. User should be able to click on connect icon.
        DESCRIPTION: 3. User should be landed on shop bet tracker page.
        EXPECTED: 1. 1. 1. User should be able to launch the sportsbook URL
        EXPECTED: 2. User should be able to click on connect icon.
        EXPECTED: 3. User should be landed on shop bet tracker page.
        """
        self.site.wait_content_state(state_name="Homepage")
        if self.device_type == 'mobile':
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.retail.TITLE).click()
        else:
            self.site.header.top_menu.items_as_ordered_dict.get(vec.retail.TITLE).click()
        self.site.wait_content_state(state_name='connect')
        menu_items = self.site.connect.menu_items.items_as_ordered_dict
        menu_items[vec.retail.BET_TRACKER].click()
        wait_for_result(lambda: self.site.bet_tracker.page_title.is_displayed(),
                        name='Bet Tracker header is not loaded',
                        timeout=20)
        actual_header = self.site.bet_tracker.page_title.text
        self.assertEqual(actual_header, vec.retail.BET_TRACKER.upper(),
                         msg=f'Actual header "{actual_header}" is not same as Expected header "{vec.retail.BET_TRACKER.upper()}"')
