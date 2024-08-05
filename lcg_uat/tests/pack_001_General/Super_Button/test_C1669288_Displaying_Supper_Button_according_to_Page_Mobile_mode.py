import pytest

from tests.base_test import vtest
from tests.pack_001_General.Super_Button.base_super_button_test import BaseSuperButtonTest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot modify CMS on prod
@pytest.mark.smoke
@pytest.mark.quick_links
@pytest.mark.super_button
@pytest.mark.mobile_only
@pytest.mark.high
@pytest.mark.navigation
@pytest.mark.slow
@pytest.mark.timeout(900)
@vtest
class Test_C1669288_Displaying_Super_Button_according_to_Page(BaseUserAccountTest, BaseSuperButtonTest):
    """
    TR_ID: C1669288
    VOL_ID: C16396576
    NAME: Displaying Super Button according to Page
    PRECONDITIONS: Super Button should be added and enabled in CMS
    PRECONDITIONS:    https://{domain}/quick-links/navigation-points
    PRECONDITIONS: where domain may be:
    PRECONDITIONS:  * coral-cms-dev1.symphony-solutions.eu - Local env
    PRECONDITIONS:  * coral-cms-dev0.symphony-solutions.eu - Develop
    """
    keep_browser_open = True

    def reload_page(self):
        """
        DESCRIPTION: CMS update loads with some delay so need to add small sleep to make test run more stable
        and reload tested page
        :return: None
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

    def get_exact_supper_button_config_index(self):
        """
        DESCRIPTION: CMS update loads with some delay so need to add small sleep to make test run more stable and reload tested page
        :return: index or None if not super button not found in config
        """
        super_button_index = None
        navigation_points_config = self.cms_config.get_initial_data().get('navigationPoints', [])
        for index, config in enumerate(navigation_points_config):
            if self.super_button_name.lower() == config['title'].lower():
                super_button_index = index
                break
        return super_button_index

    def test_000_preconditions(self):
        """
        DESCRIPTION: Super Button creation
        """
        super_button = self.cms_config.add_mobile_super_button()
        self.__class__.super_button_name = super_button.get('title').upper()

        self.__class__.tab_name = self.get_ribbon_tab_name(internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play,
                                                           raise_exceptions=False)
        self.softAssert(self.assertTrue, self.tab_name,
                        msg=f'Tab with internalId "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play}" is not available')

    def test_001_configure_mobile_super_button_in_cms(self, tab_names=['/home/in-play']):
        """
        DESCRIPTION: Configure previously created "Auto Test Super Button" in CMS
        """
        self.cms_config.update_mobile_super_button(name=self.super_button_name, home_tabs=tab_names)

    def test_002_load_oxygen_app_and_verify_super_button_presence(self, tab_names=['/home/in-play']):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button presence
        EXPECTED: Super Button is present on the same Home Tab that was chosen
        EXPECTED: Super Button is present below Module Ribbon Tabs and above of content of the tab
        EXPECTED: Super Button is a yellow button
        """
        tab_menu = self.site.home.module_selection_ribbon.tab_menu
        tab_menu.click_button(self.tab_name)
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertTrue(tabs, msg='No tabs found')
        index = wait_for_result(lambda: self.get_exact_supper_button_config_index() is not None,
                                name=f'Super Button "{self.super_button_name}" to appear in CMS',
                                timeout=30,
                                poll_interval=2)
        if index:
            CmsClientException(f'Super Button "{self.super_button_name}" not present in CMS response')
        if self.tab_name in tabs.keys():
            result = wait_for_result(lambda: self.super_button_name.title() in self.cms_config.get_initial_data()['navigationPoints'][self.get_exact_supper_button_config_index()]['title'] and
                                     self.cms_config.get_initial_data()['navigationPoints'][self.get_exact_supper_button_config_index()]['homeTabs'] == tab_names,
                                     name='Super Button to displayed',
                                     poll_interval=2,
                                     bypass_exceptions=(KeyError, IndexError, TypeError),
                                     timeout=60)
            self.site.header.scroll_to_top()
            self.assertTrue(result, msg=f'Super Button "{self.super_button_name}" is not present in response')
            self.site.home.get_module_content(module_name=self.tab_name)
            self.reload_page()
            current_tab = self.site.home.module_selection_ribbon.tab_menu.current
            self.softAssert(self.assertEqual, current_tab, self.tab_name, msg=f'Current active tab: "{current_tab}", '
                                                                              f'expected: "{self.tab_name}"')

            self.softAssert(self.assertTrue, self.site.home.has_quick_link_section(),
                            msg='Quick Link section is not found on "{self.tab_name}" page')
            self.softAssert(self.assertTrue, self.site.home.quick_link_section.has_button(),
                            msg=f'Mobile Super Button was not found on "{self.tab_name}" page')

    def test_003_deselect_tab_from_show_on_home_tabs_drop_down(self):
        """
        DESCRIPTION: Deselect tab from 'Show on Home Tabs' drop-down
        EXPECTED: Changes are saved successfully
        """
        self.test_001_configure_mobile_super_button_in_cms(tab_names=None)

    def test_004_load_oxygen_app_and_verify_supper_button_presence(self):
        """
        DESCRIPTION: Load Oxygen app and verify Super Button presence
        EXPECTED: Mobile Super Button is NO more displayed on the chosen Home Tab
        """
        tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        if self.tab_name in tabs.keys():
            result = wait_for_result(lambda: self.cms_config.get_initial_data()['navigationPoints'][self.get_exact_supper_button_config_index()]['homeTabs'] is None,
                                     name='Super Button disappear',
                                     poll_interval=2,
                                     bypass_exceptions=(IndexError, KeyError),
                                     timeout=60)
            self.assertTrue(result, msg=f'Super Button "{self.super_button_name}" is still present in response')
            self.reload_page()
            self.site.home.get_module_content(module_name=self.tab_name)
            if self.site.home.has_quick_link_section():
                self.softAssert(self.assertNotEqual, self.site.home.quick_link_section.button.name.upper(),
                                self.super_button_name,
                                msg=f'Mobile Super Button: "{self.super_button_name}" '
                                    f'still displayed on "{self.tab_name}" page')
            else:
                self._logger.warning(f'*** No Super Button displayed on "{self.tab_name}" page')

    def test_005_repeat_steps_1_4_for_featured_home_tab(self):
        """
        DESCRIPTION: Repeat steps 1-4 for Featured home tab
        EXPECTED: Results are the same
        """
        self.__class__.tab_name = self.get_ribbon_tab_name(
            self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)
        self.softAssert(self.assertTrue, self.tab_name,
                        msg=f'Tab with internalId "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured}" is not available')
        self.test_001_configure_mobile_super_button_in_cms(tab_names=['/home/featured'])
        self.reload_page()
        self.test_002_load_oxygen_app_and_verify_super_button_presence(tab_names=['/home/featured'])
        self.test_003_deselect_tab_from_show_on_home_tabs_drop_down()
        self.test_004_load_oxygen_app_and_verify_supper_button_presence()

    def test_006_repeat_steps_1_4_for_next_races_home_tab(self):
        """
        DESCRIPTION: Repeat steps 1-4 for Next Races home tab
        EXPECTED: Results are the same
        """
        self.__class__.tab_name = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races,
            raise_exceptions=False)
        self.softAssert(self.assertTrue, self.tab_name,
                        msg=f'Tab with internalId "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.next_races}" is not available')
        self.test_001_configure_mobile_super_button_in_cms(tab_names=['/home/next-races'])
        self.reload_page()
        self.test_002_load_oxygen_app_and_verify_super_button_presence(tab_names=['/home/next-races'])
        self.test_003_deselect_tab_from_show_on_home_tabs_drop_down()
        self.test_004_load_oxygen_app_and_verify_supper_button_presence()

    def test_007_repeat_steps_1_4_for_live_stream_home_tab(self):
        """
        DESCRIPTION: Repeat steps 1-4 for Live Stream home tab
        EXPECTED: Results are the same
        """
        self.__class__.tab_name = self.get_ribbon_tab_name(
            internal_id=self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream,
            raise_exceptions=False)
        self.softAssert(self.assertTrue, self.tab_name,
                        msg=f'Tab with internalId "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.live_stream}" is not available')
        self.test_001_configure_mobile_super_button_in_cms(tab_names=['/home/live-stream'])
        self.reload_page()
        self.test_002_load_oxygen_app_and_verify_super_button_presence(tab_names=['/home/live-stream'])
        self.test_003_deselect_tab_from_show_on_home_tabs_drop_down()
        self.test_004_load_oxygen_app_and_verify_supper_button_presence()

    def test_008_configure_super_button_for_sport_page(self, category_ids=[16]):
        """
        DESCRIPTION: Select to one of available Sport in 'Show on Sports' drop-down and save changes
        EXPECTED: Changes are saved successfully
        """
        self.cms_config.update_mobile_super_button(name=self.super_button_name, enabled=True,
                                                   category_id=category_ids)
        result = wait_for_result(
            lambda: category_ids == self.cms_config.get_initial_data()['navigationPoints'][self.get_exact_supper_button_config_index()]['categoryId'],
            name='Category ids to change',
            timeout=60)
        self.softAssert(self.assertTrue, result, msg=f'Needed category ids are not present in response')

    def test_009_open_sport_page_and_verify_super_button_presence(self):
        """
        DESCRIPTION: Open Sport page and verify Super Button presence
        EXPECTED: Super Button is present on Sport
        EXPECTED: Super Button is present between <Sport>/<Race> subtabs (e.g. In-Play) and page content
        """
        self.reload_page()
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        self.softAssert(self.assertTrue, self.site.football.has_quick_link_section(),
                        msg='Super Button was not found on "Football" page')
        self.softAssert(self.assertTrue, self.site.football.quick_link_section.has_button(),
                        msg='Mobile Super Button yellow button was not found on "Football" page')

    def test_010_deselect_super_button_for_sport(self):
        """
        DESCRIPTION: Deselect Sport from 'Show on Sports' drop-down
        EXPECTED: Changes are saved successfully
        """
        self.test_008_configure_super_button_for_sport_page(category_ids=None)

    def test_011_open_sport_page_and_verify_super_button_presence(self):
        """
        DESCRIPTION: Open Sport page and verify Super Button presence
        EXPECTED: Mobile Super Button is NO more displayed on the chosen Sport page
        """
        self.reload_page()
        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='Football')
        if self.site.football.has_quick_link_section():
            result = wait_for_result(lambda: self.super_button_name.title() not in self.cms_config.get_initial_data()['navigationPoints'][self.get_exact_supper_button_config_index()]['title'],
                                     name='Super Button disappear',
                                     poll_interval=2,
                                     timeout=60)
            self.softAssert(self.assertTrue, result, msg=f'Super Button "{self.super_button_name}" is still present in '
                                                         f'response on Football page')
            self.reload_page()
            self.softAssert(self.assertNotEqual, self.site.football.quick_link_section.button.name.upper(),
                            self.super_button_name,
                            msg=f'Mobile Super Button: "{self.super_button_name}" still displayed on "Football" page')
        else:
            self._logger.warning('*** No Super Button displayed on "Football" page')

    def test_012_configure_super_button_for_race_page(self):
        """
        DESCRIPTION: Select to one of available Race in 'Show on Sports' drop-down and save changes
        EXPECTED: Changes are saved successfully
        """
        self.cms_config.update_mobile_super_button(name=self.super_button_name, enabled=True, category_id=[21])

    def test_013_open_race_page_and_verify_super_button_presence(self):
        """
        DESCRIPTION: Open Race page and verify Super Button presence
        EXPECTED: Mobile Super Button is present on Sport
        EXPECTED: Mobile Super Button is present between <Sport>/<Race> subtabs (e.g. In-Play) and page content
        """
        self.reload_page()
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        result = wait_for_result(
            lambda: self.super_button_name.title() in self.cms_config.get_initial_data()['navigationPoints'][self.get_exact_supper_button_config_index()]['title'],
            name='Super Button appear on Horseracing page',
            poll_interval=2,
            timeout=60)
        self.softAssert(self.assertTrue, result, msg=f'Super Button "{self.super_button_name}" '
                                                     f'is not present in response on Horseracing page')
        self.softAssert(self.assertTrue, self.site.horse_racing.has_quick_link_section(),
                        msg='Mobile Super Button was not found on "Horse Racing" page')
        self.softAssert(self.assertTrue, self.site.horse_racing.quick_link_section.has_button(),
                        msg='Mobile Super Button yellow button was not found on "Horse Racing" page')

    def test_014_deselect_super_button_for_race(self):
        """
        DESCRIPTION: Deselect Race from 'Show on Sports' drop-down
        EXPECTED: Changes are saved successfully
        """
        self.cms_config.update_mobile_super_button(name=self.super_button_name, category_id=None)

    def test_015_open_race_page_and_verify_super_button_presence(self):
        """
        DESCRIPTION: Open Race page and verify Super Button presence
        EXPECTED: Mobile Super Button is NO more displayed on the chosen Race page
        """
        self.reload_page()
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state(state_name='HorseRacing')
        if self.site.horse_racing.has_quick_link_section():
            result = wait_for_result(lambda: self.super_button_name.title() not in self.cms_config.get_initial_data()['navigationPoints'][self.get_exact_supper_button_config_index()]['title'],
                                     name='Super Button disappear',
                                     poll_interval=2,
                                     timeout=60)
            self.softAssert(self.assertTrue, result,
                            msg=f'Super Button "{self.super_button_name}" is still present in response on Horseracing page')

            self.softAssert(self.assertNotEqual, self.site.horse_racing.quick_link_section.button.name.upper(),
                            self.super_button_name,
                            msg=f'Super Button: "{self.super_button_name}" still displayed on "Horse Racing" page')
        else:
            self._logger.warning('*** No Super Button displayed on "Horse Racing" page')
