import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.adhoc_suite
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.sports_specific
@pytest.mark.football_specific
@vtest
class Test_C65949632_Verify_the_displaying_and_virtual_scrolling_behaviour_of_inplay_widget_on_football_SLP(Common):
    """
    TR_ID: C65949632
    NAME: Verify the displaying and virtual scrolling behaviour of inplay widget on football SLP
    DESCRIPTION: This test case is to validate the displaying and virtual scrolling behaviour of inplay widget on football SLP.
    PRECONDITIONS: User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: Football entry points
    PRECONDITIONS: Navigate to     menus>subheadermenus>Football.
    PRECONDITIONS: Click on Football.
    PRECONDITIONS: Make the active check box and in app check box as active.
    PRECONDITIONS: Click on save changes button.
    PRECONDITIONS: Navigate to sport pages>sport categories>football>Genral sport configuration.
    PRECONDITIONS: Enable all the check boxes present out there.
    PRECONDITIONS: Enter all the mandatory fields.
    PRECONDITIONS: Note : Add primary markets there.
    PRECONDITIONS: Scroll down amd make sure to enable all the tabs(matches,,inplay,Specials,Outrights) .
    PRECONDITIONS: Click on save changes button.
    PRECONDITIONS: Navigate to system configuration>structure>Desktopwidgettoggle.
    PRECONDITIONS: Enable inplay under the desktopwidgetstoggle.
    PRECONDITIONS: click on save changes button.
    """
    keep_browser_open = True
    number_of_inplay_events = 0
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load CMS app & Check Football is enabled under Header submenus and In play widget is enabled in the system configuration
        EXPECTED: Football header submenu is enabled in CMS
        EXPECTED: In play widget is enabled in the system configuration
        """
        # ************************** Verification of In Play Widget in CMS **************************************
        inplay_status = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle').get('inPlay')
        if not inplay_status:
            self.cms_config.update_system_configuration_structure(config_item='DesktopWidgetsToggle',
                                                                  field_name='inPlay', field_value=True)
        self._logger.info(f'=====> In Play widget is enabled in the system configuration')
        # ************************** Verification of Football header submenu in CMS **************************************
        header_submenus = self.cms_config.get_header_submenus()
        header_submenus_list = [header_submenu.get('linkTitle').upper() for header_submenu in header_submenus]
        for header_submenu in header_submenus:
            if "FOOTBALL" in header_submenus_list:
                if header_submenu.get('linkTitle').upper() == "FOOTBALL":
                    if header_submenu.get('disabled') is False and header_submenu.get('inApp') is True:
                        self._logger.info('FOOTBALL header sub menu is configured in CMS')
                        break
                    else:
                        self.cms_config.update_header_submenu(header_submenu_id=header_submenu.get('id'), inApp=True,
                                                              disabled=False)
                        break
            else:
                self.cms_config.create_header_submenu(name="Football", target_url='sport/football')
                break
        self._logger.info(f'=====> Football is configured in header sub menu')

    def test_001_lauch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Lauch the Ladbrokes/Coral application.
        EXPECTED: Application should be loaded successfully.By default user is on home page
        """
        # ****************************** Navigating to Home page ************************
        self.site.wait_content_state(state_name="Homepage")
        self._logger.info(f'=====> Launched application and Home page loaded successfully')

    def test_002_desktop_navigate_to_sub_header_menu_and_click_on_footballmobile__navigate_to_sports_ribbon_and_click_on_click_on_football(
            self):
        """
        DESCRIPTION: Desktop: navigate to sub header menu and click on football.
        DESCRIPTION: Mobile : navigate to sports ribbon and click on click on football.
        EXPECTED: User should be navigated to the  Football landing  page.
        EXPECTED: by default user is in matches tab.
        """
        # ************************** Navigating to In Play header submenu **************************************
        actual_header_sub_menus = self.site.header.sport_menu.items_as_ordered_dict
        self.assertTrue(actual_header_sub_menus, msg='Header sub menu is not available')
        actual_header_sub_menus.get('IN-PLAY').click()
        self.site.wait_content_state(state_name='InPlay')
        sports = self.get_inplay_sport_menu_items()
        fooball_sport = None
        for sport_name, sport in sports.items():
            if sport_name.upper() == 'FOOTBALL':
                self.__class__.number_of_inplay_events = sport.counter
                if self.number_of_inplay_events > 0:
                    fooball_sport = sport_name
                break
        if fooball_sport is None:
            raise VoltronException(f'No live events available for Football sport')
        self._logger.info(
            f'=====> Navigated to In Play header submenu page and Verified live events are available for Football sport')
        # ************************** Navigating to Football header submenu **************************************
        actual_header_sub_menus.get('FOOTBALL').click()
        self.site.wait_content_state('football')
        self._logger.info(f'=====> Navigated to Football sport page successfully')
        # ************************** Verifying Matches tab **************************************
        tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        current_tab = self.site.sports_page.tabs_menu.current
        expected_tab = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            category_id=self.ob_config.football_config.category_id)
        if current_tab.upper() != expected_tab.upper():
            tab = next((tab for tab_name, tab in tabs.items() if tab_name.upper() == expected_tab.upper()), None)
            tab.click()
            current_tab = self.site.sports_page.tabs_menu.current
            self.assertEqual(current_tab.upper(), expected_tab.upper(),
                             msg=f'Expected tab name {expected_tab.upper()} but actual is {current_tab.upper()}')
        self._logger.info(f'=====> Navigated to Football Matches tab')

    def test_003_validate_the_inplay_widget_there(self):
        """
        DESCRIPTION: Validate the inplay widget there.
        EXPECTED: In play widget should be displayed under the matches tab.
        """
        # ************************** Verifying In Play Widget **************************************
        sections = self.site.sports_page.in_play_widget.items_as_ordered_dict
        expected_in_play_widget = "IN-PLAY LIVE FOOTBALL"
        actual_in_play_widgets = [section_name.upper() for section_name in sections]
        self.assertIn(expected_in_play_widget, actual_in_play_widgets,
                      msg=f'In Play Widget is available under Matched tab')
        self._logger.info(f'=====> Verified in play widget under matches tab successfully')

    def test_004_click_on_left__and_right_arrow_present_on_the_inplay_widget(self):
        """
        DESCRIPTION: click on left  and right arrow present on the inplay widget
        EXPECTED: Virtual scrolling behaviour should work as expected.
        """
        # ************************** Verifying In Play Widget Left and Right Arrows **************************************
        self.__class__.section = self.site.football.in_play_widget.items_as_ordered_dict.get(
            'In-Play LIVE Football')
        self.assertTrue(self.section, msg='"In-Play" widget not found on football SLP')
        self.__class__.events = self.section.content.items_as_ordered_dict
        self.assertTrue(self.events, msg='events are not displayed')
        if self.number_of_inplay_events > 1:
            event1 = list(self.events.values())[0]
            event1.mouse_over()
            wait_for_haul(2)
            right_arrow = self.section.right_arrow
            self.assertTrue(right_arrow.is_displayed(),
                            msg='Right arrow is not displayed after mouse over on In Play widget')
            click(right_arrow)
            event1.mouse_over()
            wait_for_haul(2)
            left_arrow = self.section.left_arrow
            self.assertTrue(left_arrow.is_displayed(),
                            msg='Left arrow is not displayed after mouse over on In Play widget')
            click(left_arrow)
            self._logger.info(f'=====> In Play events are more than one. Verified Left and Right arrows successfully')
        else:
            self._logger.info(f'=====> In Play events are not more than one. Not verified Left and Right arrows')

    def test_005_click_on_inplay_event_present_out_there(self):
        """
        DESCRIPTION: Click on inplay event present out there.
        EXPECTED: 
        """
        # ************************** Click on In Play Widget event and Verify events details page **************************************
        event_name, event = list(self.events.items())[0]
        event.click()
        page_title = list(self.site.football.breadcrumbs.items_as_ordered_dict.keys())[-1]
        for i in range(5):
            if page_title is None:
                wait_for_haul(3)
                page_title = list(self.site.football.breadcrumbs.items_as_ordered_dict.keys())[-1]
            else:
                break
        self.assertIn(event_name.upper(), page_title.upper(),
                      msg=f'User not navigated to event details page when clicked on In Play widget event')
        self._logger.info(f'=====> Clicked on In Play Widget event and Verified event details page')

    def test_006_navigate_to_other_tabs(self):
        """
        DESCRIPTION: Navigate to other tabs.
        EXPECTED: Inplay widget should not be displayed.
        """
        # ************************** Navigating to the tab(other than Matches tab) **************************************
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state('football')
        tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
        current_tab = self.site.sports_page.tabs_menu.current
        expected_tab = self.get_sport_tab_name(
            self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
            category_id=self.ob_config.football_config.category_id)
        if current_tab.upper() == expected_tab.upper():
            tab = next((tab for tab_name, tab in tabs.items() if tab_name.upper() != expected_tab.upper()), None)
            tab.click()
            current_tab = self.site.sports_page.tabs_menu.current
            self.assertNotEqual(current_tab.upper(), expected_tab.upper(),
                                msg=f'Expected tab {expected_tab.upper()} and actual tab {current_tab.upper()} are same')
        self._logger.info(f'=====> Navigated to tab(other than Matches tab)')
        # ************************** Verifying In Play Widget **************************************
        sections = self.site.sports_page.in_play_widget.items_as_ordered_dict
        expected_in_play_widget = "IN-PLAY LIVE FOOTBALL"
        actual_in_play_widgets = [section_name.upper() for section_name in sections]
        self.assertNotIn(expected_in_play_widget, actual_in_play_widgets,
                         msg=f'In play Widget is available under {current_tab} tab')
        self._logger.info(f'=====> Verified in play widget for other than matches tab')

    def test_007_navigate_back_to_the_home_page(self):
        """
        DESCRIPTION: Navigate back to the home page.
        EXPECTED: User should be navigated back to the home page.
        """
        pass

    def test_008_repeat_3_4_steps(self):
        """
        DESCRIPTION: Repeat 3-4 steps
        EXPECTED: should work as expected
        """
        pass

    def test_009_login_to_the_application(self):
        """
        DESCRIPTION: Login to the application.
        EXPECTED: should work as expected
        """
        self.site.login()
        self.test_002_desktop_navigate_to_sub_header_menu_and_click_on_footballmobile__navigate_to_sports_ribbon_and_click_on_click_on_football()
        self.test_003_validate_the_inplay_widget_there()
        self.test_004_click_on_left__and_right_arrow_present_on_the_inplay_widget()
        self.test_005_click_on_inplay_event_present_out_there()
        self.test_006_navigate_to_other_tabs()
        self._logger.info(f'=====> Verified all the above steps for logged in user')
