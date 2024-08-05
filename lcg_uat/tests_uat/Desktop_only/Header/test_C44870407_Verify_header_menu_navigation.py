import pytest
import tests
from voltron.environments import constants as vec
from tests.Common import Common
from tests.base_test import vtest
from voltron.pages.shared.components.base import ComponentBase


@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870407_Verify_header_menu_navigation(Common, ComponentBase):
    """
    TR_ID: C44870407
    NAME: Verify header menu navigation
    DESCRIPTION: Verify that the following links are displayed as per GDs and navigates user to respective URLs.
    DESCRIPTION: URLs:
    DESCRIPTION: SPORTS            https://sports.coral.co.uk/
    DESCRIPTION: GAMING            https://www.coral.co.uk/en/games
    DESCRIPTION: CASINO            https://www.coral.co.uk/en/coralcasino
    DESCRIPTION: LIVE CASINO       https://www.coral.co.uk/en/livecasino
    DESCRIPTION: SLOTS             https://www.coral.co.uk/en/slots
    DESCRIPTION: BINGO             https://bingo.coral.co.uk/en/bingo
    DESCRIPTION: POKER             https://poker.coral.co.uk/en/poker
    DESCRIPTION: OFFERS            https://sports.coral.co.uk/promotions/all
    DESCRIPTION: CONNECT           https://sports.coral.co.uk/retail
    PRECONDITIONS: User can view the header menu links in logged in or logged out status.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_verify_the_all_header_menu_links_functionality_changes_on_hovering_mouse_over_text_on_bottom_navigation___page_opens_in_the_same_window_user_remains_logged_in_and_is_able_to_navigate_back(self):
        """
        DESCRIPTION:  Verify the all Header menu links functionality (changes on hovering, mouse over text on bottom, navigation - page opens in the same window, user remains logged in, and is able to navigate back).
        EXPECTED: When clicking on link user navigated to respective page in the same window and remains logged in.
        """
        # changes_on_hovering_mouse_over_text_on_bottom can not be automated
        if self.site.wait_logged_out(timeout=5):
            self.site.wait_content_state(state_name="homepage")
            self.device.refresh_page()
            header = self.site.header.top_menu.items_as_ordered_dict
            self.assertTrue(header, msg='Header items not displayed on home page')
        self.site.login()
        header = self.site.header.top_menu.items_as_ordered_dict
        self.assertTrue(header, msg='Header items not displayed on home page')
        for event_name, event in list(header.items()):
            header = self.site.header.top_menu.items_as_ordered_dict
            expected_window = self.device.driver.current_window_handle
            if event_name != "SPORTS":
                header[event_name].click()
                self.site.wait_content_state_changed()
            if event_name == "GAMING":
                event_name = "GAMES"
            elif event_name == "OFFERS" and self.brand == 'bma':
                event_name = "PROMOTIONS"
            elif event_name == "CONNECT" or event_name == "THE GRID":
                event_name = "RETAIL"
            elif event_name == "JACKPOTS":
                event_name = "JACKPOT"
            elif event_name == "SAFER GAMBLING":
                event_name = vec.bma.FOOTER_LINK_UNIQUE_WORD[11]

            actual_page_url = self.device.get_current_url()
            self.assertIn(event_name.lower().replace(" ", ""), actual_page_url.lower(),
                          msg=f'header item "{event_name.lower()}" is not present in "{actual_page_url}"')
            if event_name == "SPORTS":
                self.site.wait_content_state(state_name="homepage")
            else:
                self.device.go_back()
            self.assertEqual(self.device.driver.current_window_handle, expected_window, msg=f'user is not on the same window')
            self.assertFalse(self.site.wait_logged_out(timeout=5), msg='user is not logged in')
            self.site.wait_content_state(state_name="homepage")
