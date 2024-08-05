import pytest
import calendar
from datetime import datetime
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we cannot create events in prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.horseracing
@vtest
class Test_C60094848_Verify_display_of_Day_selector_tabs_Races_available_3_days(Common):
    """
    TR_ID: C60094848
    NAME: Verify display of Day selector tabs-Races available 3 days
    DESCRIPTION: Verify display of Today, Tomorrow and Next day name when races are available for next 3 days
    PRECONDITIONS: 1: Login to TI and schedule races for only Today , Tomorrow and on Day 3
    """
    keep_browser_open = True

    # for getting today name
    current_datetime = datetime.now()
    dayNumber = calendar.weekday(current_datetime.year, current_datetime.month, current_datetime.day)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"]
    if dayNumber == 5:
        day3 = days[0]
    if dayNumber == 6:
        day3 = days[1]
    else:
        day3 = (days[dayNumber + 2])
    days_list = [vec.sb.TABS_NAME_TODAY.upper(),
                 vec.sb.TABS_NAME_TOMORROW.upper(),
                 day3.upper()]

    def verify_selected_tabs(self, tab):
        req_tab = tab.upper() if self.brand == 'bma' else tab.title()
        self.grouping_buttons.items_as_ordered_dict.get(req_tab).click()
        self.site.wait_content_state_changed()
        current_tab = self.grouping_buttons.current
        self.assertEqual(current_tab.upper(), tab.upper(),
                         msg=f'Actual tab: "{current_tab.upper()}" is not same as'
                             f'Expected tab: "{tab.upper()}".')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Add 3 racing events with today, tomorrow and day3 timings:
        EXPECTED: Racing events added
        """
        # for today tab
        self.ob_config.add_UK_racing_event(number_of_runners=1)
        # for tomorrow tab
        tomorrow = self.get_date_time_formatted_string(days=1)
        self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=tomorrow)
        # for Day3 tab
        day3 = self.get_date_time_formatted_string(days=2)
        self.ob_config.add_UK_racing_event(number_of_runners=1, start_time=day3)
        category_id = self.ob_config.horseracing_config.category_id
        self.__class__.cms_horse_tab_name = self.get_sport_title(category_id=category_id)

    def test_001_launch_ladbrokescoral_url_or_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL or App
        EXPECTED: User should be able to launch the app
        """
        # covered in step 2

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        cms_horse_tab_name = self.cms_horse_tab_name if self.device_type == 'mobile' and self.brand == 'ladbrokes' else self.cms_horse_tab_name.upper()
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            all_items = self.site.header.sport_menu.items_as_ordered_dict
        all_items.get(cms_horse_tab_name).click()
        self.site.wait_content_state('horse-racing')

    def test_003_verify_the_display_of_meetings_in_hr_landing_page(self):
        """
        DESCRIPTION: Verify the display of meetings in HR landing page
        EXPECTED: 1: Meetings tab should be selected by default
        EXPECTED: For Coral: Featured tab should be selected by default
        EXPECTED: 2: UK & Irish races should be displayed at by default
        """
        current_tab_name = self.site.horse_racing.tabs_menu.current
        self.assertEqual(current_tab_name, vec.racing.RACING_DEFAULT_TAB_NAME,
                         msg=f'Default tab is "{current_tab_name}" not "{vec.racing.RACING_DEFAULT_TAB_NAME}" tab')

        accordions = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        uk_ire = 'UK And Irish Races' if self.brand == 'bma' and self.device_type == 'desktop' else 'UK AND IRISH RACES'

        uk_and_ire_module = accordions.get(uk_ire)
        self.site.wait_splash_to_hide(timeout=30)
        self.assertTrue(uk_and_ire_module,
                        msg=f'"{uk_ire}" is not found in {accordions.keys()}')

    def test_004_verify_the_day_selector_tabs_displayed_in_the_country_panel(self):
        """
        DESCRIPTION: Verify the Day selector tabs displayed in the Country Panel
        EXPECTED: 1: Today and Tomorrow and Day 3 name should be displayed
        EXPECTED: 2: User should be able to switch between the tabs
        EXPECTED: Example:
        EXPECTED: Today Tomorrow Wednesday
        EXPECTED: Here Wednesday being the third day name
        """
        self.__class__.grouping_buttons = self.site.contents.tab_content.grouping_buttons
        days_tabs = self.grouping_buttons.items_names
        actual_list = [i.upper() for i in days_tabs]
        for i in range(len(self.days_list)):
            self.assertEqual(actual_list[i], self.days_list[i], msg=f'"Actual "{actual_list[i]}" is not same as '
                                                                    f'Expected "{self.days_list[i]}"')
        self.verify_selected_tabs(tab=self.days_list[1])
        self.verify_selected_tabs(tab=self.days_list[2])
        self.verify_selected_tabs(tab=self.days_list[0])
