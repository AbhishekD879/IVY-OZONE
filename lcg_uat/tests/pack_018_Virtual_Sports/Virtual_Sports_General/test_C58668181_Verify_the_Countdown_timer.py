import re
from random import choice
import pytest
import tests
from tests.base_test import vtest
from tests.pack_018_Virtual_Sports.BaseVirtualsTest import BaseVirtualsTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from crlat_siteserve_client.constants import ATTRIBUTES
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.siteserve_client import SiteServeRequests
import voltron.environments.constants as vec


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.medium
@pytest.mark.virtual_sports
@pytest.mark.navigation
@pytest.mark.desktop
@pytest.mark.reg157_fix
@vtest
class Test_C58668181_Verify_the_Countdown_timer(BaseVirtualsTest):
    """
    TR_ID: C58668181
    NAME: Verify the Countdown timer
    DESCRIPTION: This test case verifies the view of Countdown timer.
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment.
    PRECONDITIONS: 2. Go to 'Virtual Sports'.
    """
    keep_browser_open = True
    next_events = vec.virtuals.VIRTUAL_HUB_NEXT_EVENTS

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get list of active virtual sport categories
        DESCRIPTION: Open Coral/Ladbrokes test environment.
        DESCRIPTION: Go to 'Virtual Sports'.
        """
        virtuals_cms_class_ids = self.cms_virtual_sports_class_ids()
        ss_req = SiteServeRequests(env=tests.settings.backend_env,
                                   brand=self.brand,
                                   category_id=self.ob_config.virtuals_config.category_id)
        sports_list = ss_req.ss_class(query_builder=self.ss_query_builder.
                                      add_filter(simple_filter(LEVELS.CLASS,
                                                               ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS,
                                                               str(self.ob_config.virtuals_config.category_id))))
        if not sports_list:
            raise SiteServeException('There are no active virtual sports')
        event = None
        sports_list_with_active_events = []
        for sport_class in sports_list:
            class_id = sport_class['class']['id']
            events = self.get_active_event_for_class(class_id=class_id, raise_exceptions=False)
            if not events:
                continue
            event = choice(events)
            ss_class_id = event['event']['classId']
            if ss_class_id in virtuals_cms_class_ids:
                sports_list_with_active_events.append(ss_class_id)
            else:
                continue
        if not event:
            raise SiteServeException('There are no available virtual event with Forecast tab')
        sports_name_ids = {}
        for ss_all_class_id in sports_list_with_active_events:
            for item in self.virtual_carousel_menu_items:
                for tracks in item.get('tracks', None):
                    if tracks.get('classId', None) == ss_all_class_id:
                        sports_name_ids.update({item['title']: ss_all_class_id})

        # Take all sports class IDs related to Virtual category
        self.__class__.expected_sports = list(sports_name_ids.keys())

        self.site.open_sport(self.get_sport_title(category_id=self.ob_config.virtuals_config.category_id),
                             content_state='VirtualSports')

    def test_001_observe_event_which_will_start_after_30plus_seconds(self):
        """
        DESCRIPTION: Observe event which will start after 30+ seconds.
        EXPECTED: The Countdown timer is displayed with:
        EXPECTED: - Timer inside circle is counting down
        EXPECTED: - Circle is grey
        EXPECTED: ![](index.php?/attachments/get/105735340)
        virtual sports hub is configured to a new page and from virtual sports hub we navigate to virtual sports page.
        """
        virtual_hub_home_page = self.cms_config.get_system_configuration_structure().get('VirtualHubHomePage')
        if virtual_hub_home_page.get('enabled'):
            hubs_section = next(
                (section for section_name, section in self.site.virtual_sports_hub.items_as_ordered_dict.items() if
                 section_name.upper() != self.next_events.upper()), None)
            section_sports = list(hubs_section.items_as_ordered_dict.values())[0]
            section_sports.click()
        for sport_name in self.expected_sports:
            virtual_sports_list = self.site.virtual_sports
            open_tab = virtual_sports_list.sport_carousel.open_tab(sport_name)
            self.assertTrue(open_tab, msg=f'Tab "{sport_name}" is not opened')
            sports_tabs = virtual_sports_list.sport_carousel.items_as_ordered_dict
            self.assertTrue(sports_tabs, msg="Virtual Carousel is empty")
            sport_tab = sports_tabs.get(sport_name)
            self.assertTrue(sport_tab, msg=f'Sport tab "{sport_name}" does not exist')
            event_off_times_list = virtual_sports_list.tab_content.event_off_times_list
            self.assertTrue(event_off_times_list.is_displayed(),
                            msg=f'Event selector ribbon is not displayed for "{sport_name}"')

            has_timer = virtual_sports_list.tab_content.has_timer(timeout=7)
            self.assertTrue(has_timer, msg="No timer found")
            sport_time = virtual_sports_list.tab_content.sport_event_timer
            time_format_match = re.match('\d+:\d+|^LIVE$', sport_time) is not None
            self.assertTrue(time_format_match, msg=f'Displayed "{sport_time}" instead of Timer or Live label '
                                                   f'for "{sport_name}"')

    def test_002_observe_event_which_will_start_in_0_29_seconds(self):
        """
        DESCRIPTION: Observe event which will start in 0-29 seconds.
        EXPECTED: The Countdown timer is displayed with:
        EXPECTED: - Timer inside circle is counting down
        EXPECTED: - Circle turns blue
        EXPECTED: ![](index.php?/attachments/get/105735354)
        """
        # LIVE or timer with navigating verified on step 1
        pass

    def test_003_observe_event_which_already_started(self):
        """
        DESCRIPTION: Observe event which already started.
        EXPECTED: The Countdown timer is displayed with:
        EXPECTED: - The "LIVE" string is displayed inside instead of Timer
        EXPECTED: - Circle is blue
        EXPECTED: ![](index.php?/attachments/get/105735356)
        """
        # LIVE or timer with navigating verified on step 1
        pass

    def test_004_observe_event_which_will_start_after_60_minutes(self):
        """
        DESCRIPTION: Observe event which will start after 60 minutes.
        EXPECTED: The Countdown timer is displayed with:
        EXPECTED: - Timer inside circle is counting down
        EXPECTED: - Circle is grey
        EXPECTED: - The time is displayed with +60 value in the left part of the timer (e.g., "61:06").
        """
        # LIVE or timer with navigating verified on step 1
        pass
