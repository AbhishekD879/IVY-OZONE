import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.uat
@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870411_Quick_links_at_the_bottom_of_the_pages(Common):
    """
    TR_ID: C44870411
    NAME: Quick links at the bottom of the pages
    DESCRIPTION: Quick links at the bottom of the pages and message above should be displayed on the bottom of each desktop page
    PRECONDITIONS: User loads the Ladbrokes desktop web page and log in
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_001_verify_that_on_the_bottom_of_each_desktop_page_there_is_a_section_that_contains__a_messagenot_found_what_you_are_looking_for_hit_a_quick_link__links_to_other_sports_landing_pagesverify_that_all_the_links_navigate_user_in_the_right_page(self):
        """
        DESCRIPTION: Verify that on the bottom of each desktop page there is a section that contains
        DESCRIPTION: - a message
        DESCRIPTION: NOT FOUND WHAT YOU ARE LOOKING FOR? HIT A QUICK LINK
        DESCRIPTION: - links to other Sports Landing pages
        DESCRIPTION: Verify that all the links navigate user in the right page
        EXPECTED: Quick links at the bottom of the pages and message above should be displayed on the bottom of each desktop page
        EXPECTED: The navigation works fine
        """
        self.site.login()
        self.site.close_all_dialogs()
        actual_message = self.site.home.quick_link_section.message_validation.text
        self.assertEqual(actual_message, vec.bma.QUICK_LINK_MESSAGE,
                         msg=f'Actual message: "{actual_message}" is not same as'
                             f'Expected message: "{vec.bma.QUICK_LINK_MESSAGE}" on HomePage')
        self.__class__.quick_links = self.site.home.quick_link_section.quick_link_items.items_as_ordered_dict
        self.assertTrue(self.quick_links, msg='No quick links present on the page')

        for i in range(len(self.quick_links.items())):
            self.quick_links = self.site.contents.quick_link_section.quick_link_items.items_as_ordered_dict
            q_name, q_item = list(self.quick_links.items())[i]
            if q_name not in [vec.bma.OTF_PAGE_TITLE.upper(), vec.bma.QUICK_LINK_HOMEPAGE,
                              vec.virtuals.VIRTUAL_GREYHOUNDS]:
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
                        self.assertTrue(q_name.startswith(page_title) or page_title in q_name,
                                        msg=f'Actual page title "{page_title}" '
                                            f'is not same as Expected "{q_name}"')
