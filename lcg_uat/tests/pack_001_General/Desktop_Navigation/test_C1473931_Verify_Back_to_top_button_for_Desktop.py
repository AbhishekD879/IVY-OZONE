import voltron.environments.constants as vec
import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.desktop_only
@pytest.mark.navigation
@pytest.mark.screen_resolution
@pytest.mark.timeout(900)
@pytest.mark.reg157_fix
@vtest
class Test_C1473931_Verify_Back_to_top_button_for_Desktop(Common):
    """
    TR_ID: C1473931
    VOL_ID: C9697921
    NAME: Verify Back to top button for Desktop
    DESCRIPTION: This test case verifies 'Back to top' button for Desktop.
    PRECONDITIONS: Oxygen app is loaded
    """
    keep_browser_open = True
    device_resolution_1 = (970, 415)
    device_resolution_2 = (1280, 720)
    device_resolution_3 = (1920, 1080)
    device_name = tests.desktop_default
    back_to_top_text = vec.sb_desktop.BACK_TO_TOP

    def test_001_scroll_the_page_down(self, page_name='Home', content_state='Home'):
        """
        DESCRIPTION: Scroll the page down
        EXPECTED: * 'Back to top' button appears when full Main Header is hidden
        EXPECTED: * 'Back to top' button is located in the bottom right corner of the page
        EXPECTED: * 'Back to top' button became sticky
        EXPECTED: * 'Up' arrow and 'Back to top' inscription are displayed at the button
        """
        try:
            self.site.open_sport(name=page_name)
        except VoltronException:
            self.navigate_to_page(name=page_name)

        self.site.wait_content_state(content_state)
        self.site.contents.scroll_to_bottom()

        # todo: fix https://jira.egalacoral.com/browse/VOL-3654
        # self.assertFalse(self.site.header.is_displayed(scroll_to=False, expected_result=False), msg=f'Main Header is shown')
        self.__class__.back_to_top_button = self.site.back_to_top_button
        self.assertTrue(self.back_to_top_button.is_displayed(),
                        msg=f'"Back to top" button is not located in the bottom')
        back_to_top_name = self.back_to_top_button.name
        self.assertEqual(back_to_top_name, self.back_to_top_text,
                         msg=f'Actual text {back_to_top_name} does not match expected {self.back_to_top_text}')
        self.assertTrue(self.back_to_top_button.icon.is_displayed(),
                        msg=f'"Up" arrow is not displayed at the button {self.back_to_top_button}')

    def test_002_resize_the_page_to_more_than_1920px(self):
        """
        DESCRIPTION: Resize the page to more than 1920px
        EXPECTED: 'Back to top' button is located in the bottom right corner of the window
        """
        self.device.set_viewport_size(*self.device_resolution_3)
        sleep(5)  # few seconds needed for browser to 'stabilize' after resolution change
        self.site.contents.scroll_to_bottom()
        self.assertTrue(self.back_to_top_button.is_displayed(),
                        msg=f'"Back to top" button is not located in the bottom')

    def test_003_resize_the_page_to_less_than_970px(self):
        """
        DESCRIPTION: Resize the page to less than 970px
        EXPECTED: 'Back to top' button is located in the bottom right corner of the window and visible all the time
        """
        self.device.set_viewport_size(*self.device_resolution_1)
        sleep(5)  # few seconds needed for browser to 'stabilize' after resolution change
        self.site.contents.scroll_to_bottom()
        self.assertTrue(self.back_to_top_button.is_displayed(),
                        msg=f'"Back to top" button is not located in the bottom')

    def test_004_hover_the_mouse_over_the_back_to_top_button(self):
        """
        DESCRIPTION: Hover the mouse over the 'Back to top' button
        EXPECTED: * Hover state is activated
        EXPECTED: * Pointer changed the view from 'Normal select' to 'Link select' for realizing
        the possibility to click on the particular area
        """
        self.back_to_top_button.mouse_over()
        button_opacity = self.site.back_to_top_button.css_property_value('opacity')
        self.assertEqual(button_opacity, '1', msg=f'Hover state is not activated')
        pointer = self.site.back_to_top_button.css_property_value('cursor')
        self.assertEqual(pointer, 'pointer', msg=f'Hover state is not activated')

    def test_005_click_on_the_back_to_top_button(self):
        """
        DESCRIPTION: Click on the 'Back to top' button
        EXPECTED: * User is redirected to the top of the page
        EXPECTED: * 'Back to top' button disappears
        """
        self.back_to_top_button.click()
        self.assertTrue(self.site.header.is_displayed(), msg=f'Main Header is hidden')
        self.assertFalse(self.back_to_top_button.is_displayed(expected_result=False, timeout=5),
                         msg=f'"Back to top" button is shown at the top of the page')

    def test_006_navigate_to_different_pages_across_application_and_repeat_steps__1_5(self):
        """
        DESCRIPTION: Navigate to different pages across application and repeat steps  1-5
        """
        pages = {'horse-racing': 'horse-racing',
                 f'sport/{vec.siteserve.FOOTBALL_TAB}'.lower(): vec.siteserve.FOOTBALL_TAB,
                 f'sport/{vec.siteserve.TENNIS_TAB}'.lower(): vec.siteserve.TENNIS_TAB,
                 'az-sports': 'AZ Sports',
                 'lotto': 'Lotto'}

        for page_name, content_state in pages.items():
            # Set device resolution to default size
            self.device.set_viewport_size(*self.device_resolution_2)
            sleep(5)  # few seconds needed for browser to 'stabilize' after resolution change

            self.test_001_scroll_the_page_down(page_name=page_name, content_state=content_state)
            self.test_002_resize_the_page_to_more_than_1920px()
            self.test_003_resize_the_page_to_less_than_970px()
            self.test_004_hover_the_mouse_over_the_back_to_top_button()
            self.test_005_click_on_the_back_to_top_button()
