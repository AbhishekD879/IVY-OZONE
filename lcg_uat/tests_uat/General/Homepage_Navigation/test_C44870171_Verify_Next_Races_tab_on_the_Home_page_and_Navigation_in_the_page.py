import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing


@pytest.mark.prod
@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.mobile_only
@pytest.mark.uat
@pytest.mark.p2
@vtest
class Test_C44870171_Verify_Next_Races_tab_on_the_Home_page_and_Navigation_in_the_page(BaseRacing):
    """
    TR_ID: C44870171
    NAME: Verify Next Races tab on the Home page and Navigation in the page.
    DESCRIPTION: Verify next races tab page on the home page and navigation in the page. Verify New Navigation arrows Next Races Carousel.
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load app
        EXPECTED: App is loaded and user is landed on home page
        """
        self.site.wait_content_state(state_name="Homepage")

    def test_002_select_next_races_tab_on_home_page(self):
        """
        DESCRIPTION: Select NEXT RACES tab on home page
        EXPECTED: Next Races page is loaded and next races are listed in start time order.
        """
        self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get('NEXT RACES').click()
        self.device.driver.implicitly_wait(3)
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertTrue(tabs.get('NEXT RACES').is_selected(),
                        msg='NEXT RACES is not selected after clicking on it')
        self.__class__.hr_events = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        event_time_list = []
        for item in list(self.hr_events.keys()):
            event_time_list.append(item[:5])
        self.assertEqual(event_time_list, sorted(event_time_list),
                         msg='Events are not in start time order')

    def test_003_click_on_more__of_any_meeting_from_the_list(self):
        """
        DESCRIPTION: Click on 'MORE >' of any meeting from the list
        EXPECTED: User should navigate to the corresponding meeting page.
        """
        events = list(self.hr_events.values())
        event_name_expected = events[0].name
        events[0].full_race_card.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
        event_name_actual = self.site.racing_event_details.event_title
        self.assertEqual(event_name_expected.upper(), event_name_actual.upper(),
                         msg=f'Actual event name {event_name_actual} is not as same as'
                             f'Expected event name {event_name_expected}')
