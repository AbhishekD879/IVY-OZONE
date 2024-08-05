import pytest
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.Common import Common
import voltron.environments.constants as vec
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.popular_bets
@pytest.mark.reg167_fix
@pytest.mark.adhoc_suite
@pytest.mark.football
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C66035681_Verify_the_show_more_and_show_less_in_Popular_Bets(Common):
    """
    TR_ID: C66035681
    NAME: Verify the show more and show less in Popular Bets
    DESCRIPTION: This test case verifies the  show more and show less in Popular Bets
    PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
    """
    keep_browser_open = True

    def get_sport_tab_status(self, tab):
        """
        Check the status of a sport tab.
        Args:
            tab (dict): The tab information.
        Returns:
            bool: True if the tab is enabled and has events; False otherwise.
        Raises:
            ValueError: If check_events or has_events parameters are missing in the tab.
        """
        check_events = tab.get("checkEvents")
        has_events = tab.get("hasEvents")
        enabled = tab.get("enabled")
        if not enabled:
            return False
        if check_events is None or has_events is None:
            raise ValueError(
                f"check_events: {check_events} and has_events: {has_events} are missing in the tab parameters.")
        if check_events and not has_events:
            return False
        return True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Configure Popular bets tab in CMS (CMS>Sports pages>Popular bets)
        """
        all_sub_tabs_for_football = self.cms_config.get_sport_tabs(sport_id=16)
        popular_bets_tab = next(
            (tab for tab in all_sub_tabs_for_football if tab.get("name") == "popularbets"),
            None)
        self.assertTrue(popular_bets_tab, msg="Popular bets tab not found")
        self.__class__.popular_bets_tab_name = next(
            (sub_tab['trendingTabName'].upper() for sub_tab in popular_bets_tab['trendingTabs'] for inner_sub_tab in
             sub_tab['popularTabs']
             if inner_sub_tab['popularTabName'] == 'Popular_tab' and inner_sub_tab['enabled'] and sub_tab[
                 'enabled']), None)
        if not self.popular_bets_tab_name:
            raise CMSException(f' "{self.popular_bets_tab_name}" tab is not enabled in CMS ')
        popular_bets_tab_status = self.get_sport_tab_status(popular_bets_tab)
        self.assertTrue(popular_bets_tab_status, msg="Popular bets tab does not have event")
        self.__class__.tab_name = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.popularbets,
                                                          category_id=16)
        sport_id = self.ob_config.football_config.category_id
        tab_name = vec.sb.TABS_NAME_POPULAR_BETS

        # Retrieve data for the popular bets tab from the CMS
        sports_tab_data = self.cms_config.get_sports_tab_data(sport_id=sport_id, tab_name=tab_name)
        # Extract the default bet count from the retrieved data from CMS
        self.__class__.default_bet_count = sports_tab_data.get('trendingTabs')[0].get('popularTabs')[0].get(
            'numbOfDefaultPopularBets')
        self.__class__.bet_count_after_show_more = sports_tab_data.get('trendingTabs')[0].get('popularTabs')[0].get(
            'numbOfShowMorePopularBets')
        self.__class__.expected_count_after_show_more = self.default_bet_count + self.bet_count_after_show_more
        self.__class__.expected_count_after_second_show_more = self.expected_count_after_show_more + self.bet_count_after_show_more

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the Application
        EXPECTED: Application is launched Successfully
        """
        self.site.login()
        self.site.wait_content_state("HOMEPAGE")

    def test_002_click_on_the_football_sport(self):
        """
        DESCRIPTION: Click on the Football Sport
        EXPECTED: Able to navigate to the Football landing page
        """
        # Open the sports section for football
        self.site.open_sport("football")
        # waiting to load football page content
        self.site.wait_content_state("football")

    def test_003_verify_the_display_of_popular_bets_section(self):
        """
        DESCRIPTION: Verify the display of Popular Bets section
        EXPECTED: User can able to see the Popular Bets section
        """
        # getting available tabs in football page
        tabs = self.site.football.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='No tabs found on Football page')

    def test_004_click_on_popular_bets_section(self):
        """
        DESCRIPTION: Click on Popular Bets section
        EXPECTED: Able to navigate to the Popular Bets section successfully
        """
        # Clicking on popular bets tab in football page
        result = self.site.football.tabs_menu.click_button(self.tab_name)
        self.assertTrue(result, msg=f'"{result}" tab is not opened')
        self.site.football.tab_content.grouping_buttons.click_button(self.popular_bets_tab_name)
        # getting active tab in football page and checking whether it is matching with expected tab
        actual_tab = self.site.football.tabs_menu.current
        self.assertEqual(actual_tab, self.tab_name,
                         msg=f'Expected tab "{self.tab_name}" but found "{actual_tab}"')

    def test_005_click_on_show_more(self):
        """
        DESCRIPTION: Click on "show more"
        EXPECTED: 1. User is displayed with 5 more popular bets in addition to the default list of 10 popular bets.
        EXPECTED: 2. Show more should not be displayed after 20 popular bets in total.
        """
        last_updated = self.site.football.tab_content.has_last_updated
        self.assertTrue(last_updated, "Last updated time format not found")
        #we are storing the last updated time here to check it later in 7th step that time has updated or not
        self.__class__.initial_last_updated_time = self.site.football.tab_content.last_updated

        # Get the initial count of items
        initial_count = len(list(self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup))

        # Checking whether intial count is equal to default bet count
        self.assertEqual(initial_count, self.default_bet_count, "Initial count does not match the count from CMS")

        # Clicking on the "Show more" button
        show_more_button = self.site.football.tab_content.accordions_list.show_more_less
        self.assertTrue(show_more_button, "Show more button not found")
        show_more_button.click()

        # storing the count after clicking show more
        count_after_show_more = len(list(self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup))

        # Check if the count increased by 'bet_count_after_show_more' after clicking "Show more"
        self.assertEqual(count_after_show_more, self.expected_count_after_show_more,
                         "Count did not increase after clicking Show more")

        # Click on the "Show more" button 
        show_more_button.click()

        # Get the count after the again clicking on "Show more"
        count_after_second_show_more = len(list(self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup))

        # Checking if the count increased by 'bet_count_after_show_more' after clicking "Show more"
        self.assertEqual(count_after_second_show_more, self.expected_count_after_second_show_more,
                         "Count did not increase after second click on Show more")

        # Check if the "Show less" button is displayed after reaching the maximum count
        show_less_button = self.site.football.tab_content.accordions_list.show_more_less

        # Checking if there are more than 20 bets are displayed or not
        if count_after_second_show_more > 20:
            raise VoltronException("More than 20 bets are displayed")

        self.assertTrue(show_less_button, "Show less button not found")

    def test_006_click_on_show_less(self):
        """
        DESCRIPTION: Click on "show less"
        EXPECTED: user should be displayed with only 10 popular bets on clicking "Show less" at anypoint of time.
        """
        show_less_button = self.site.football.tab_content.accordions_list.show_more_less
        self.assertTrue(show_less_button, "Show less button not found")
        show_less_button.click()

        # Get the count after clicking "Show less" 
        count_after_show_less = len(list(self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup))

        # Checking if the count is now back to "intial count" (10)
        self.assertEqual(count_after_show_less, self.default_bet_count, "Count is not 10 after clicking Show less")

    def test_007_click_on_show_more_to_display_15_bets_and_wait_for_the_dynamic_update_of_last_updated_time_noof_bets_is_configured_through_cms(self):
        """
        DESCRIPTION: Click on Show more to display 15 bets and wait for the Dynamic update of Last Updated time (No.of bets is configured through CMS)
        EXPECTED: 15 bets should be displayed even after the dynamic update of Last updated time.
        """
        last_updated = self.site.football.tab_content.has_last_updated
        self.assertTrue(last_updated, "last updated time format not found")

        # Clicking on "Show more" button to display 15 bets
        show_more_button = self.site.football.tab_content.accordions_list.show_more_less
        self.assertTrue(show_more_button, "Show more button not found")
        show_more_button.click()

        # Verify that 15 bets are displayed
        bets_count = len(list(self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup))
        self.assertEqual(bets_count, self.expected_count_after_show_more, "Expected 15 bets to be displayed after clicking on 'Show more'")
        # waiting for "last upadated time" to update
        wait_for_haul(20)

        # Geting the updated "last updated time"
        updated_last_updated_time = self.site.football.tab_content.last_updated

        # Verify that the "last updated time" has changed after clicking "Show more" 
        self.assertNotEqual(self.initial_last_updated_time, updated_last_updated_time,
                            "Expected last updated time to change after displaying 15 bets")

        # Verify that 15 bets are still displayed after the dynamic update
        updated_bets_count = len(list(self.site.football.tab_content.accordions_list.items_as_ordered_dict_inc_dup))
        self.assertEqual(updated_bets_count, self.expected_count_after_show_more,
                         "Expected 15 bets to be displayed after dynamic update of last updated time")

    def test_008_notealways_20_bets_need_to_be_displayedcan_cover_this_in_separate_tcs(self):
        """
        DESCRIPTION: Note:Always 20 bets need to be displayed.(Can cover this in separate tcs)
        EXPECTED:
        """
        # covered in test_005_click_on_show_more step
