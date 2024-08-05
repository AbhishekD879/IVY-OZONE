import pytest
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.prod
@pytest.mark.user_account
@vtest
class Test_C44870141_Verify_user_navigates_to_the_Game_Stop_registration_site_when_clicking_on_Game_Stop_icon_on_the_page_bottom(Common):
    """
    TR_ID: C44870141
    NAME: "Verify user navigates to the 'Game Stop' registration site when clicking on 'Game Stop' icon on the page bottom
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True
    expected_url = "https://www.gamstop.co.uk/"

    def test_001_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED: Homepage is shown
        """
        self.site.wait_content_state(state_name="Homepage")

    def test_002_verify_the_presence_of__footer_items(self):
        """
        DESCRIPTION: Verify the presence of  Footer items
        """
        self.site.header.scroll_to_bottom()
        footer_items = self.site.footer.footer_section_bottom.items_as_ordered_dict
        self.assertTrue(footer_items, msg='No Footer items are present on the page')

    def test_003_click_on_gamstop(self):
        """
        DESCRIPTION: Click on GamStop
        EXPECTED: User is taken to the 'Game Stop' registration site (https://www.gamstop.co.uk/)
        """
        game_stop = self.site.footer.footer_section_bottom.game_stop
        self.assertTrue(game_stop.is_displayed(), msg="GameStop is not displayed")
        click(game_stop)
        self.device.switch_to_new_tab()
        wait_for_result(lambda: self.device.get_current_url() == self.expected_url, timeout=15)
        actual_url = self.device.get_current_url()
        self.assertEqual(actual_url, self.expected_url, msg=f'"Game Stop" registration site url is not equal'
                                                            f'Actual: "{actual_url}",'
                                                            f'Expected: "{self.expected_url}"')
