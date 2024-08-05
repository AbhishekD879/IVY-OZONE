import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


# @pytest.mark.tst2
# @pytest.mark.stg2    have an issue in qa2, favourites are not getting added to favoutie matches pages
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.p2
@pytest.mark.crl_uat
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870192_Verify_user_can_add_FB_favourites__Verify_user_can_select_Deselect_favourite_icon_Verify_favourite_icon_count_Verify_user_can_navigate_to_the_favourite_matches_page_and_verify_the_page_links_and_details_(Common):
    """
    TR_ID: C44870192
    NAME: "Verify user can add FB favourites, - Verify user can select/Deselect favourite icon -Verify favourite icon count -Verify user can navigate to the favourite matches page and verify the page links and details  "
    DESCRIPTION: "Verify user can add FB favourites,
    DESCRIPTION: - Verify user can select/Deselect favourite icon
    DESCRIPTION: -Verify favourite icon count
    DESCRIPTION: -Verify user can navigate to the favourite matches page and verify the page links and details
    """
    keep_browser_open = True

    def test_001_load_appsite__log_in(self):
        """
        DESCRIPTION: Load app/site & Log in
        EXPECTED: User is logged in and on the Homepage
        """
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_football(self):
        """
        DESCRIPTION: Navigate to Football
        EXPECTED: User is on the Football page with Matches displayed
        """
        if self.device_type == 'mobile':
            self.site.open_sport(name='FOOTBALL')
            self.site.wait_content_state(state_name='FOOTBALL')
        else:
            self.site.header.sport_menu.items_as_ordered_dict['FOOTBALL'].click()
        self.assertTrue(self.site.sports_page.tabs_menu.items_as_ordered_dict['MATCHES'].is_selected(),
                        msg=f'{vec.sb.TABS_NAME_MATCHES} tab is not selected by default')

    def test_003_add_football_event_to_favourites(self):
        """
        DESCRIPTION: Add Football Event to Favourites
        EXPECTED: Event is displayed on Favourite widget
        """
        counter = self.site.football.header_line.favourites_counter
        comp_name, comp = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.items())[0]
        if comp_name == 'ENHANCED MULTIPLES':
            comp_name, comp = list(self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict.items())[1]
        self.__class__.event_name, event = list(comp.items_as_ordered_dict.items())[0]
        event.favourite_icon.click()
        self.assertTrue(event.favourite_icon.is_selected(), msg=f'favourite icon of event "{event}" is not selected')
        event.click()
        if self.device_type == 'mobile':
            actual_counter = float(self.site.football.header_line.favourites_counter)
            expected_counter = float(counter) + 1
            self.assertEqual(actual_counter, expected_counter,
                             msg=f'Actual favourites counter: "{actual_counter}", is not same as expected favourites counter "{expected_counter}"')
            self.site.football.header_line.go_to_favourites_page.click()
            self.site.wait_content_state(state_name='Favourites')
            expected_url = "https://" + tests.HOSTNAME + "/favourites"
            actual_url = self.device.get_current_url()
            self.assertEqual(actual_url, expected_url,
                             msg=f'current url "{actual_url}" is not as same as'f'expected url "{expected_url}"')
            all_fav_events = self.site.favourites.tab_content.accordions_list.items_as_ordered_dict
        else:
            all_fav_events = self.site.favourites.items_as_ordered_dict
        self.assertTrue(self.event_name in all_fav_events,
                        msg=f'favourite event "{self.event_name}" is not added to favourite page/widget')

    def test_004_verify_the_user_is_able_to_select__deselect_the_favourites(self):
        """
        DESCRIPTION: Verify the user is able to select & deselect the Favourites
        EXPECTED: User is able to select & deselect the Favourites.
        """
        if self.device_type == 'mobile':
            page_title = self.site.favourites.header_line.page_title.title
            self.assertEqual(page_title, vec.sb.FAVOURITE_MATCHES,
                             msg=f'Page title "{page_title}" is not same as expected title "{vec.sb.FAVOURITE_MATCHES}"')
            self.site.favourites.tab_content.accordions_list.items_as_ordered_dict[self.event_name].event_name_we.click()
            wait_for_result(lambda: self.site.sport_event_details, timeout=5)
            self.site.sport_event_details.favourite_icon.click()
            self.assertFalse(self.site.sport_event_details.favourite_icon.is_selected(expected_result=False),
                             msg=f'Favourites icon is still highlighted for event "{self.event_name}"')
            self.device.go_back()
            all_fav_events = self.site.favourites.tab_content.accordions_list.items_as_ordered_dict
            self.assertFalse(self.event_name in all_fav_events, msg=f'favourite event "{self.event_name}" is not deselected')
            self.device.go_back()
            self.device.go_back()
        else:
            self.site.sport_event_details.favourite_icon.click()
            self.assertFalse(self.site.sport_event_details.favourite_icon.is_selected(expected_result=False),
                             msg=f'Favourites icon is still highlighted for event "{self.event_name}"')
            self.device.go_back()
            all_fav_events = self.site.favourites.items_as_ordered_dict
            self.assertFalse(self.event_name in all_fav_events, msg=f'favourite event "{self.event_name}" is not deselected')

    def test_005_go_to_favourite_matchesdesktop_favourites_widgetmobile_star_fav_on_the_header__football_pageand_verify_user_can_navigate_to_the_favourite_matches_page_and_verify_the_page_links_and_details(self):
        """
        DESCRIPTION: Go to Favourite Matches
        DESCRIPTION: Desktop: Favourites Widget
        DESCRIPTION: Mobile: Star (Fav) on the Header > Football page
        DESCRIPTION: and verify user can navigate to the favourite matches page and verify the page links and details
        EXPECTED: All the selected Favourites are displayed and the user is able to navigate to the favourite matches page and verify the page links and details.
        """
        self.test_003_add_football_event_to_favourites()
        if self.device_type != 'mobile':
            self.site.favourites.items_as_ordered_dict[self.event_name].click()
            header_title = wait_for_result(lambda: self.site.sport_event_details.header_line.page_title.title, timeout=10)
            self.assertEqual(self.event_name.upper().replace(" VS ", " V "), header_title, msg=f'not navigated to correct event page "{self.event_name}"')

    def test_006_verify_the_user_is_able_to_deselect_previous_added_event_from_favourite_widget(self):
        """
        DESCRIPTION: Verify the user is able to Deselect previous added Event from Favourite widget
        EXPECTED: Event are deselected from Favourite widget
        """
        self.test_004_verify_the_user_is_able_to_select__deselect_the_favourites()
