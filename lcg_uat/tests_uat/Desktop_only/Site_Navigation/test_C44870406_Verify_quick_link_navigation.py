import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870406_Verify_quick_link_navigation(Common):
    """
    TR_ID: C44870406
    NAME: Verify quick link navigation
    DESCRIPTION: Verify user can navigate to relevant pages by clicking on 'Hit a Quick Link'  menu items in the site page bottom
    DESCRIPTION: Verify on the all pages at the bottom
    PRECONDITIONS: Quick Link items are displayed on all pages at the bottom in logged in and logged out status.
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
            DESCRIPTION: Log in, and the quick link items should appear at bottom of the page, then logout.
            EXPECTED: User is logged in and quick link items are displayed, then logged out.
        """
        self.site.login()
        actual_message = self.site.home.quick_link_section.message_validation.text
        self.assertEqual(actual_message, vec.bma.QUICK_LINK_MESSAGE,
                         msg=f'Actual message: "{actual_message}" is not same as'
                             f'Expected message: "{vec.bma.QUICK_LINK_MESSAGE}" on HomePage')
        self.__class__.quick_links = self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict
        self.assertTrue(self.quick_links, msg='No quick links present on the page')
        self.site.logout()

    def test_001_open_httpsbeta_sportscoralcouk_on_chrome_browser(self):
        """
        DESCRIPTION: Open https://beta-sports.coral.co.uk/ on Chrome browser.
        EXPECTED: https://beta-sports.coral.co.uk/ displayed on Chrome browser.
        """
        self.site.wait_content_state(state_name='homepage')

    def test_002_scroll_to_bottom_of_page(self):
        """
        DESCRIPTION: Scroll to bottom of page.
        EXPECTED: Page displays
        EXPECTED: "NOT FOUND WHAT YOU ARE LOOKING FOR? HIT A QUICK LINK"
        EXPECTED: Play 1-2 Free to win £1
        EXPECTED: Homepage
        EXPECTED: In-Play Betting
        EXPECTED: Horse Racing
        EXPECTED: etc
        """
        # This step is covered in step 6

    def test_003_click_on_horse_racing_quick_link(self):
        """
        DESCRIPTION: Click on Horse Racing Quick Link.
        EXPECTED: User directed to Horse Racing landing page.
        """
        # This step is covered in step-6

    def test_004_scroll_to_bottom_of_page(self):
        """
        DESCRIPTION: Scroll to bottom of page.
        EXPECTED: Page displays
        EXPECTED: "NOT FOUND WHAT YOU ARE LOOKING FOR? HIT A QUICK LINK"
        EXPECTED: Play 1-2 Free to win £1
        EXPECTED: Homepage
        EXPECTED: In-Play Betting
        EXPECTED: Horse Racing
        EXPECTED: etc
        """
        # This step is covered in step 6

    def test_005_click_on_horse_promotions_link(self):
        """
        DESCRIPTION: Click on Horse Promotions Link.
        EXPECTED: User directed to Horse Racing landing page.
        """
        # This step is covered in step 6

    def test_006_repeat_the_above_step_for_a_range_of_quick_links_available(self):
        """
        DESCRIPTION: Repeat the above step for a range of quick links available
        EXPECTED: User is directed to those respective quick links and is able to see the respective quick links at the bottom of the page.
        """
        for i in range(len(self.quick_links.items())):
            self.quick_links = self.site.contents.quick_link_section.quick_link_items.items_as_ordered_dict
            q_name, q_item = list(self.quick_links.items())[i]
            if q_name not in [vec.bma.OTF_PAGE_TITLE.upper(), vec.bma.QUICK_LINK_HOMEPAGE, vec.virtuals.VIRTUAL_GREYHOUNDS]:
                q_item.click()
                self.site.wait_content_state_changed()
                actual_message = self.site.contents.quick_link_section.message_validation.text
                self.assertEqual(actual_message, vec.bma.QUICK_LINK_MESSAGE,
                                 msg=f'Actual message: "{actual_message}" is not same as'
                                 f'Expected message: "{vec.bma.QUICK_LINK_MESSAGE}" on "{q_name}" page')
                self.assertTrue(self.quick_links, msg='No quick links present on the page')
                if q_name not in ['Racing Super Series', 'VST', 'vst Lad', 'TestQL']:
                    page_title = self.site.contents.header_line.page_title.title.split()[0]
                    if q_name == 'BYB':
                        self.assertEqual(page_title.upper(), vec.football.FOOTBALL_TITLE.upper(),
                                         msg=f'actual page title: "{q_name}" is not same as'
                                         f'Expected page title: "{vec.football.FOOTBALL_TITLE.upper()}"')
                    else:
                        self.assertTrue(q_name.startswith(page_title) or page_title in q_name, msg=f'Actual page title "{page_title}" '
                                                                                                   f'is not same as Expected "{q_name}"')
