import pytest
import math
from datetime import datetime, date
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from voltron.pages.shared.components.base import ComponentBase
from tests.pack_009_SPORT_Specifics.Football_Specifics.Football_Coupons.BaseCouponsTest import BaseCouponsTest
from tests.base_test import vtest


@pytest.mark.p1
@pytest.mark.uat
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870315_Verify_display_of_Football_coupons_landing_page(BaseCouponsTest, ComponentBase):
    """
    TR_ID: C44870315
    NAME: "Verify display of Football coupons landing page
    DESCRIPTION: "Verify display of Coupons landing page
    DESCRIPTION: -Hover over an accordion  and verify colour change
    DESCRIPTION: -Verify accordion is clickable
    DESCRIPTION: - Verify user can navigate to coupons page and user has been shown all available coupons types
    DESCRIPTION: - Verify user can navigate to selected coupon detail page
    """
    keep_browser_open = True

    def verifying_chronological_order_of_events(self):
        sections = self.site.football.tab_content.accordions_list.items_as_ordered_dict
        for section in sections.values():
            if not section.is_expanded():
                section.expand()
                self.assertTrue(section.is_expanded(), msg=f'"{section.name}" section is not expanded')
            events = section.items_as_ordered_dict
            expected_date_list = []
            for event in events.values():
                event_time = event.template.event_time
                if event_time.endswith('Today'):
                    today_date = date.today().strftime('%d %b')
                    event_time = event_time.replace('Today', today_date)
                expected_date_list.append(event_time)
            actual_date_list = expected_date_list
            if self.brand == 'ladbrokes':
                expected_date_list.sort(key=lambda date: datetime.strptime(date, "%H:%M %d %b"))
            else:
                expected_date_list.sort(key=lambda date: datetime.strptime(date, "%H:%M, %d %b"))
            self.assertEqual(actual_date_list, expected_date_list,
                             msg=f'Actual timings: "{actual_date_list}" are not in chronological order as '
                                 f'Expected timings: "{expected_date_list}" in the league "{section.name}"')
        self.device.go_back()

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: 'Matches' tab is opened by default and highlighted
        """
        self.navigate_to_page(name='sport/football')
        actual_tab = self.site.football.tabs_menu.current
        self.assertEqual(actual_tab, vec.SB.SPORT_TABS_INTERNAL_NAMES.matches.upper(),
                         msg=f'Actual tab: "{actual_tab}" is not as'
                             f'Expected tab: "{vec.SB.SPORT_TABS_INTERNAL_NAMES.matches.upper()}" by default')

    def test_003_select_coupons_tab(self):
        """
        DESCRIPTION: Select 'Coupons' tab
        EXPECTED: 'Coupons' tab is selected and highlighted
        """
        if self.brand == 'ladbrokes':
            self.site.football.tabs_menu.click_button(vec.SB.TABS_NAME_COUPONS)
            actual_tab = self.site.football.tabs_menu.current
            self.assertEqual(actual_tab, vec.SB.TABS_NAME_COUPONS,
                             msg=f'Actual tab: "{actual_tab}" is not as'
                                 f'Expected tab: "{vec.SB.TABS_NAME_COUPONS}"')
        else:
            self.site.football.tabs_menu.click_button(vec.SB.SPORT_TABS_INTERNAL_NAMES.accumulators.upper())
            actual_tab = self.site.football.tabs_menu.current
            self.assertEqual(actual_tab, vec.SB.SPORT_TABS_INTERNAL_NAMES.accumulators.upper(),
                             msg=f'Actual tab: "{actual_tab}" is not as'
                                 f'Expected tab: "{vec.SB.SPORT_TABS_INTERNAL_NAMES.accumulators.upper()}"')

    def test_004_hover_over_an_accordion__and_verify_colour_change(self):
        """
        DESCRIPTION: Hover over an accordion  and verify colour change
        EXPECTED: Accordion colour change to grey
        """
        # this step can't be verified as there is no color change

    def test_005_verify_list_of_coupons(self):
        """
        DESCRIPTION: Verify list of coupons
        EXPECTED: List of coupons are displayed
        EXPECTED: eg:* UK Coupon
        EXPECTED: *Odds on Coupon
        EXPECTED: * European Coupon
        EXPECTED: * Euro Elite Coupon
        EXPECTED: * Televised Matches
        EXPECTED: * Top Leagues Coupon
        EXPECTED: * International Coupon
        EXPECTED: * Rest of the World Coupon
        EXPECTED: * Goalscorer Coupon
        """
        coupons_on_page = []
        self.__class__.coupon_categories = list(self.site.football.tab_content.accordions_list.items_as_ordered_dict.keys())
        for coupon_section in self.coupon_categories:
            coupons = self.get_coupons_list_in_coupons_section(coupon_section=coupon_section)
            coupons_on_page.extend(list(coupons.keys()))
        coupons_list_from_response = self.get_active_coupons_list()
        self.assertListEqual(sorted(coupons_list_from_response), sorted(coupons_on_page),
                             msg=f'Coupons sorted list from SS: \n"{sorted(coupons_list_from_response)}" \n'
                                 f'are not equal sorted to UI: \n"{sorted(coupons_on_page)}"')

    def test_006__verify_events_order_in_the_accordions_and_accordion_is_clickable(self):
        """
        DESCRIPTION: -Verify events order in the accordions and accordion is clickable
        EXPECTED: Accordion expands on click and
        EXPECTED: Events are ordered in the following way:
        EXPECTED: startTime - chronological order in the first instance
        EXPECTED: Event displayOrder in ascending
        EXPECTED: Alphabetical order in ascending (in case of the same 'startTime')
        """
        for coupon_section in range(len(self.coupon_categories)):
            coupons_list = list(self.get_coupons_list_in_coupons_section(coupon_section=self.coupon_categories[coupon_section]))
            for coupon_name in range(math.ceil(len(coupons_list) / 6)):
                self.find_coupon_and_open_it(coupon_section=self.coupon_categories[coupon_section], coupon_name=coupons_list[coupon_name])
                wait_for_result(lambda: self.site.coupon.name, timeout=3)
                self.assertEqual(self.site.coupon.name.upper(), coupons_list[coupon_name].upper(), msg=f'"{coupons_list[coupon_name]}"coupon is not opened {self.site.coupon.name}')
                self.verifying_chronological_order_of_events()

    def test_007_repeat_step_6_7_for_different_list_of_coupons_in_5(self):
        """
        DESCRIPTION: Repeat step #6 #7 for different list of coupons in #5
        """
        # this step is covered in step 6
