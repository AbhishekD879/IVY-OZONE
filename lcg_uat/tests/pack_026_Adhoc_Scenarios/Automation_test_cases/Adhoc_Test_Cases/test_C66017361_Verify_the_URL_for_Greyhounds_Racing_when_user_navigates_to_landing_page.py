import pytest
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

import tests
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.pages.shared import get_driver
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.adhoc24thJan24
@pytest.mark.back_button
@pytest.mark.navigation
@pytest.mark.greyhounds_specific
@pytest.mark.desktop
@vtest
class Test_C66017361_Verify_the_URL_for_Greyhounds_Racing_when_user_navigates_to_landing_page(BaseRacing):
    """
    TR_ID: C66017361
    NAME: Verify the URL for Greyhounds Racing when user navigates to landing page
    DESCRIPTION: Verify the URL for Horse Racing when user navigates to landing page
    """
    keep_browser_open = True
    url_stack = [f'https://{tests.HOSTNAME}/greyhound-racing']
    pointer = 0

    def check_url(self, equals=True):
        current_url = self.device.get_current_url().replace('?automationtest=true', '')
        msg = f'Actual URL is no "{current_url}" is not same as Expected URL : "{self.url_stack[self.pointer]}"' if equals else f'URL is not changed : Current URL is "{current_url}"'
        self.assertEquals(equals, current_url == self.url_stack[self.pointer], msg=msg)

    def reset_url_stack_and_pointer(self, url=f'https://{tests.HOSTNAME}/greyhound-racing'):
        self.__class__.url_stack = [url]
        self.__class__.pointer = 0

    def test_000_preconditions(self):
        """
        PRECONDITIONS: In CMS->Sport Category->Greyhounds Racing->Target Uri->/greyhound-racing
        """
        sports = self.cms_config.get_sport_categories()
        greyhounds_sport = next((sport for sport in sports if sport['imageTitle'].upper() == 'GREYHOUNDS' and not sport['disabled']), None)
        self.assertIsNotNone(greyhounds_sport, 'GREYHOUNDS Sport is not configured in CMS!!!')
        actual_targetUri = greyhounds_sport['targetUri']
        expected_targetUri = '/greyhound-racing'
        self.assertEqual(actual_targetUri, expected_targetUri,
                         f'Actual targetUri is : "{actual_targetUri}" is not same as '
                         f'Expected targetUri : "{expected_targetUri}" in CMS')

    def test_001_launch_the_front_end_application(self):
        """
        DESCRIPTION: Launch the front end application
        EXPECTED: Homepage is loaded successfully
        """
        self.site.go_to_home_page()

    def test_002_navigate_to_greyhounds_racing_landing_page(self):
        """
        DESCRIPTION: Navigate to Greyhounds Racing landing page
        EXPECTED: GR landing page is successfully launched
        EXPECTED: The GR URL is displayed in the below format: 'https://sports.ladbrokes.com/greyhound-racing'
        """
        self.site.open_sport('Greyhounds')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.url_stack[self.pointer], f'Actual URL is no "{current_url}" is not same as '
                                                                    f'Expected URL : "{self.url_stack[self.pointer]}"')

    def test_003_navigate_to_any_other_sub_tabs_like_next_racestomorrowfuturespecials_and_come_back_to_next_racestoday_tab_by_using_browser_back_button(self, back_button='browser'):
        """
        DESCRIPTION: Navigate to any other sub tabs like: Next races/Tomorrow/Future/Specials and come back to 'Next races/Today' tab by using browser back button
        EXPECTED: User successfully navigated to other tabs
        EXPECTED: The HR URL is displayed in below format: 'https://sports.ladbrokes.com/greyhound-racing' once came back to Next races/Today tab by using browser back button
        """
        tabs = self.site.greyhound.tabs_menu.items_as_ordered_dict

        # url checking: for only navigating to one tab and clicking back and then verifying the urls
        for tab_name, tab in list(tabs.items())[1:]:
            tab.click()
            current_tab_name = self.site.greyhound.tabs_menu.current
            self.assertEqual(tab_name, current_tab_name, f'Actual tab is "{current_tab_name}" is not same as '
                                                         f'Expected tab : "{tab_name}"')
            self.check_url(equals=False)
            if back_button == 'browser':
                get_driver().back()
            elif back_button == 'app':
                self.site.back_button.click()
            else:
                breadcrumbs = self.site.greyhound.tab_content.breadcrumbs.items_as_ordered_dict
                greyhounds_breadcrumbs = next((obj for name, obj in breadcrumbs.items() if name.upper() == 'GREYHOUND RACING'))
                greyhounds_breadcrumbs.click()
            self.check_url()

        if back_button == 'breadcrumbs':
            return 'below steps are not applicable for breadcrumbs'

        # urls checking while navigating to back in manner of tab by tab from last to first
        for tab_name, tab in list(tabs.items())[1:]:
            tab.click()
            current_tab_name = self.site.greyhound.tabs_menu.current
            self.assertEqual(tab_name, current_tab_name, f'Actual tab is "{current_tab_name}" is not same as '
                                                         f'Expected tab : "{tab_name}"')
            self.__class__.url_stack.append(self.device.get_current_url())
            self.__class__.pointer = self.pointer + 1

        for _ in range(len(self.url_stack) - 1):
            if back_button == 'browser':
                get_driver().back()
            elif back_button == 'app':
                self.site.back_button.click()
            self.__class__.pointer = self.pointer - 1
            self.check_url()

    def test_004_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button(self, back_button='browser'):
        """
        DESCRIPTION: Navigate to any EDP page and come back by using browser back button
        EXPECTED: User successfully navigated to EDP page
        EXPECTED: The HR URL is displayed in below format: 'https://sports.ladbrokes.com/greyhound-racing' once came back to Next races/Today tab by using browser back button
        """
        events = self.get_next_races_section().items_as_ordered_dict if self.brand == 'bma' else self.site.greyhound.tab_content.accordions_list.items_as_ordered_dict
        event_name, event = next(iter(reversed(events.items())))
        event.scroll_to_we()
        is_virtual = event.is_virtual
        event.header.click() if self.brand == 'ladbrokes' else event.click()
        if is_virtual:
            self.site.wait_content_state('VirtualSports')
        else:
            self.site.wait_content_state('GreyHoundEventDetails')
        self.site.wait_content_state_changed()
        if back_button == 'browser':
            get_driver().back()
        elif back_button == 'app':
            if self.brand == 'ladbrokes' and self.device_type == 'mobile':
                self.site.back_button.click()
            else:
                bypass_exceptions = (NoSuchElementException, StaleElementReferenceException, VoltronException)
                if is_virtual:
                    wait_for_result(lambda: self.site.virtual_sports.back_button_click() is None, bypass_exceptions=bypass_exceptions)
                else:
                    wait_for_result(lambda: self.site.greyhound_event_details.back_button_click() is None, bypass_exceptions=bypass_exceptions)
        else:
            if is_virtual:
                self.navigate_to_page('greyhound-racing')
            else:
                breadcrumbs = self.site.greyhound_event_details.tab_content.breadcrumbs.items_as_ordered_dict
                greyhounds_breadcrumbs = next(
                    (obj for name, obj in breadcrumbs.items() if name.upper() == 'GREYHOUND RACING'))
                greyhounds_breadcrumbs.click()
        self.check_url()

    def test_005_repeat_step_34_by_using_greyhounds_racing_page_back_button(self):
        """
        DESCRIPTION: Repeat step-3,4 by using Greyhounds Racing page back button
        EXPECTED:
        """
        self.reset_url_stack_and_pointer()
        self.test_003_navigate_to_any_other_sub_tabs_like_next_racestomorrowfuturespecials_and_come_back_to_next_racestoday_tab_by_using_browser_back_button(back_button='app')
        self.reset_url_stack_and_pointer()
        self.test_004_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button(back_button='app')

    def test_006_repeat_step_34_by_using_horseracing_breadcrumb(self):
        """
        DESCRIPTION: Repeat step-3,4 by using HorseRacing' breadcrumb
        EXPECTED: The HR URL is displayed in below format: 'https://sports.ladbrokes.com/greyhound-racing/today' for coral and
        EXPECTED: 'https://sports.ladbrokes.com/greyhound-racing/races/next' for lads
        """
        if self.device_type == 'mobile':
            self._logger.info('breadcrumbs is not applicable for mobile')
            return 'breadcrumbs is not applicable for mobile'

        url = f'https://{tests.HOSTNAME}/greyhound-racing/today' if self.brand == 'bma' else f'https://{tests.HOSTNAME}/greyhound-racing/races/next'
        self.reset_url_stack_and_pointer(url=url)
        self.test_003_navigate_to_any_other_sub_tabs_like_next_racestomorrowfuturespecials_and_come_back_to_next_racestoday_tab_by_using_browser_back_button(back_button='breadcrumbs')
        self.reset_url_stack_and_pointer(url=url)
        self.test_004_navigate_to_any_edp_page_and_come_back_by_using_browser_back_button(back_button='breadcrumbs')

    def test_007_navigate_to_homepage_and_again_navigate_to_greyhounds_racing_page_then_refresh_the_page(self):
        """
        DESCRIPTION: Navigate to homepage and again navigate to greyhounds racing page then refresh the page
        EXPECTED: The GR URL is displayed in below format: 'https://sports.ladbrokes.com/greyhounds-racing'
        """
        self.reset_url_stack_and_pointer()
        self.navigate_to_page('/')
        self.site.wait_content_state('Home')
        self.site.open_sport('Greyhounds')
        self.device.refresh_page()
        self.check_url()

    def test_008_duplicate_the_page_and_check_the_other_duplicated_page(self):
        """
        DESCRIPTION: Duplicate the page and check the other duplicated page
        EXPECTED: The GR URL is displayed in below format: 'https://sports.ladbrokes.com/greyhounds-racing'
        """
        # not automating