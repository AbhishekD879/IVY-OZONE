import pytest
from tests.base_test import vtest
from json import JSONDecodeError
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.horseracing
@pytest.mark.adhoc_suite
@pytest.mark.adhoc06thFeb24
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66035621_Verify_that_exponential_calls_are_not_seen_when_user_navigates_in_between_various_tabs_on_the_HR_GH_landing_pages(
    Common):
    """
    TR_ID: C66035621
    NAME: Verify that exponential calls are not seen when user navigates in between various tabs on the HR and GH landing pages
    DESCRIPTION: This test case validates that multiple calls are not triggered when user navigates and switches between tabs which are available on the HR/GH landing page
    PRECONDITIONS: Navigate to the Horse Racing or Greyhounds landing page. Open the Dev tools in the browser -> Select the Network tab.
    PRECONDITIONS: Type tab in the filter.
    """
    enable_bs_performance_log = True
    keep_browser_open = True

    def get_response_url_count(self, url):
        """
        :param url: Required URl
        :return: Count
        """
        perflog = self.device.get_performance_log()
        count = 0
        for log in list(reversed(perflog)):
            try:
                data_dict = log[1]['message']['message']['params']['request']
                request_url = data_dict['url']
                if url in request_url:
                    count += 1
            except (KeyError, JSONDecodeError, TypeError, IndexError):
                continue
        return count

    def test_001_access_the_application_and_navigate_to_the_horse_racing_landing_page(self):
        """
        DESCRIPTION: Access the application and navigate to the Horse Racing Landing page.
        EXPECTED: Observe in the Network tab of the browser there should be only a single call when user navigates to the Horse racing landing page.
        """
        self.site.wait_content_state(state_name='HomePage')
        self.navigate_to_page('horse-racing')
        category = self.ob_config.horseracing_config.category_id
        tabs = self.site.horse_racing.tabs_menu.items_as_ordered_dict
        for tab_name, tab in tabs.items():
            tab.click()
            count = self.get_response_url_count(f'/sport-tabs/{category}')
            self.assertEqual(count, 1, msg='more than one response calls are displayed')
        self.navigate_to_page('/')

    def test_002_switch_between_meetings_next_races_future_amp_specials_tabs_which_are_available_on_the_page(self):
        """
        DESCRIPTION: Switch between Meetings, Next Races, Future &amp; Specials tabs which are available on the page.
        EXPECTED: Multiple calls should not be seen in the Network tab when user switches between various tabs.
        """
        # Covered in above step

    def test_003_repeat_for_gh(self):
        """
        DESCRIPTION: Repeat for GH
        EXPECTED: Validate the NetWork calls information
        """
        self.site.wait_content_state(state_name='HomePage')
        self.navigate_to_page(name='greyhound-racing')
        category = self.ob_config.horseracing_config.category_id
        self.site.wait_content_state('Greyhoundracing', timeout=25)
        tabs = self.site.greyhound.tabs_menu.items_as_ordered_dict
        for tab_name, tab in tabs.items():
            tab.click()
            count = self.get_response_url_count(f'/sport-tabs/{category}')
            self.assertEqual(count, 1, msg='more than one response calls are displayed')