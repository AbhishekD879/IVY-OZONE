import pytest
import tests
from tests.base_test import vtest
from collections import OrderedDict
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_haul

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.sports_specific
@pytest.mark.rugby_union_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C65969080_Verify_the_display_of_details_in_the_Rugby_Union_Competitions_tab(BaseBetSlipTest):
    """
    TR_ID: C65969080
    NAME: Verify the display of details in the Rugby Union Competitions tab
    DESCRIPTION: This test case needs to verify details displayed in the Competitions tab for Rugby Union sport.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: Competitions  tab can be configured from CMS-&gt;
    PRECONDITIONS: Sports menu-&gt; Sports Category-&gt; Rugby Union-&gt; Competitions tab-&gt; Enable/Disable.
    PRECONDITIONS: Time filters should be enabled in the Sports Categories -&gt; Rugby Union -&gt; Competitions Tab -&gt; Add time filters and save.
    PRECONDITIONS: Note: In mobile when no events are available Rugby Union sport is not displayed in A-Z sports menu and on clicking Rugby Union  from Sports ribbon user is navigated back to the sports homepage.
    """
    keep_browser_open = True
    sport_name = vec.sb.RUGBYUNION
    home_breadcrumb = 'Home'
    all_sports_page = 'az-sports'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Sports menu-&gt; Sports Category-&gt; Rugby Union-&gt; Competitions tab-&gt; Enable/Disable.
        PRECONDITIONS: Time filters should be enabled in the Sports Categories -&gt; Rugby Union -&gt; Competitions Tab -&gt; Add time filters and save.
        """
        # getting table tennis competitions tab data
        competitions_tab_data = self.cms_config.get_sports_tab_data(sport_id=self.ob_config.rugby_union_config.category_id,
                                                                    tab_name="competitions")
        if not competitions_tab_data.get('enabled') or not competitions_tab_data.get('filters')['time']['enabled']:
            # Making competitions tab enable and enabling time filter for competitions tab in cms for table tennis.
            self.cms_config.update_sports_event_filters(tab_name='competitions', sport_id=self.ob_config.rugby_union_config.category_id,
                                                        enabled=True,
                                                        timefilter_enabled=True,
                                                        event_filters_values=[1, 3, 6, 12, 24, 48])

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application
        EXPECTED: Home page should be loaded successfully
        """
        self.site.login()
        self._logger.info(f'=====> Launched application and Home page loaded successfully')

    def test_002_click_on_rugby_union_sport(self):
        """
        DESCRIPTION: Click on Rugby Union sport.
        EXPECTED: User should be able to navigate Rugby Union landing page.
        """
        self.navigate_to_page(name=self.all_sports_page)
        a_z_menu = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
        self.assertTrue(a_z_menu, msg='A-Z menu is not present')
        Rugby_union = a_z_menu.get('Rugby Union')
        self.assertTrue(Rugby_union, msg='golf sport is not present in a-z sports')
        Rugby_union.click()
        self.site.wait_content_state(state_name='Rugby Union')
        self._logger.info(f'=====> Navigated to Golf sport page successfully')

    def test_003_verify_competitions_tab(self):
        """
        DESCRIPTION: Verify Competitions tab
        EXPECTED: Competitions need to loaded successfully.
        """
        current_tab = self.site.sports_page.tabs_menu.current
        if current_tab.upper() != vec.SB.TABS_NAME_COMPETITIONS.upper():
            self.site.sports_page.tabs_menu.click_button(vec.SB.TABS_NAME_COMPETITIONS.upper())

    def test_004_verify_the_functionality_of_time_filters_by_selecting_the_time_filter(self):
        """
        DESCRIPTION: Verify the functionality of time filters by selecting the time filter.
        EXPECTED: Events should be fetched as per the time filter selected
        """
        filters = self.site.sports_page.tab_content.timeline_filters.items_as_ordered_dict
        self.assertTrue(filters, msg='filters are not displayed')
        # waiting for to load competitions tab data
        wait_for_haul(5)
        for i in filters.keys():
            filter = filters.get(i)
            filter.click()
            selected_filter = list(self.site.competition_league.tab_content.timeline_filters.selected_filters.keys())[0]
            self.assertEqual(i, selected_filter, msg=f'selected time filter {i} is not selected')
            accordion_lists = self.site.sports_page.tab_content.competitions_categories_list.items_as_ordered_dict
            if accordion_lists:
                self.assertTrue(accordion_lists,
                                msg=f'no accordions are found under competitions tab for time filter {"1h"} for table tennis')
            else:
                self._logger.info(f'no accordions are found under time filter {i}')

    def test_005_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordion's are collapsable and expandable
        EXPECTED: Accordion's should be collapsable and expandable
        """
        self.device.refresh_page()
        accordions = list(self.site.sports_page.tab_content.competitions_categories_list.items_as_ordered_dict.items())
        self.assertTrue(accordions, msg='No accordions found on page')
        for accordion_name, accordion in accordions[0:3]:
            self.assertTrue(accordion.is_expanded(), msg=f'accordion {accordion_name} is not expanded by default')
        for accordion_name, accordion in accordions[0:7]:
            if not accordion.is_expanded():
                accordion.expand()
                self.assertTrue(accordion.is_expanded(),
                                msg=f'Accordion {accordion_name} is not expanded after expansion')

    def test_006_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated to the respective page on click
        """
        if self.device_type != 'mobile':
            page = self.site.sports_page
            breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in page.breadcrumbs.items_as_ordered_dict)

            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

            self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index("Competitions"), 2,
                             msg=f'" matches " item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs["Competitions"].link.css_property_value('font-weight')) == 700,
                msg='"competitions" hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_007_verify_by_clicking_on_backward_chevron_beside_sports_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sports header
        EXPECTED: Desktop
        EXPECTED: User should be redirected to home page
        EXPECTED: User should be navigate to sport navigation  page
        EXPECTED: Mobile
        EXPECTED: User should be redirected to sport navigation  page
        """
        if self.device_type == "mobile" and tests.settings.brand == "ladbrokes":
            back_button = self.site.header.back_button
            back_button.click()
        else:
            self.site.sports_page.back_button_click()
        self.navigate_to_page('sport/rugby-union')

    def test_008_verify_bet_placement_for_single_multiplecomplex(self):
        """
        DESCRIPTION: Verify bet placement for single, multiple,complex
        EXPECTED: Bet placement should be successful
        """
        self.test_003_verify_competitions_tab()
        accordions = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg="Accordions are not displayed on Rugby union landing page")
        for accordion_name, accordion in accordions.items():
            accordion.collapse()
        competition_selection = []
        # Single Bet
        for accordion_name, accordion in accordions.items():
            accordion.expand()
            accordion_items = accordion.items_as_ordered_dict
            for _, item in accordion_items.items():
                bet_buttons = item.template.items_as_ordered_dict
                for _, button in bet_buttons.items():
                    event_selection = button._we.get_attribute("id").replace("bet-", "")
                    if event_selection != "na":
                        competition_selection.append(event_selection)
                        break
                break
            accordion.collapse()

        if len(competition_selection) > 1:
            # Single Bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=competition_selection[0])
            self.place_single_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()

        if len(competition_selection) > 2:
            # Multiple bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=[competition_selection[0], competition_selection[1]])
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        if len(competition_selection) >= 4:
            # Complex bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=[competition_selection[0],
                                                             competition_selection[1],
                                                             competition_selection[2],
                                                             competition_selection[3]])
            self.place_multiple_bet(number_of_stakes=2)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
