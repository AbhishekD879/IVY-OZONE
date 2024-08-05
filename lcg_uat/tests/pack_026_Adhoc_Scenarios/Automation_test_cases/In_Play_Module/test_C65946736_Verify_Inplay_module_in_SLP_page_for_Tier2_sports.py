import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.adhoc_suite
@vtest
# This TestCase Covers C65946734
class Test_C65946736_Verify_Inplay_module_in_SLP_page_for_Tier2_sports(Common):
    """
    TR_ID: C65946736
    NAME: Verify Inplay module in SLP page for Tier2 
sports.
    DESCRIPTION: This test case verifies Inplay module in SLP page for Tier2 sports.
    PRECONDITIONS: 1. Verify with Login/logout user.
    PRECONDITIONS: 2. Navigate to CMS-> sport pages-> sports category-> select any Tier2 sport-> active/inactive.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    expected_tier_2_sports = ['TABLE TENNIS', 'CRICKET', 'ESPORTS', 'BASEBALL', 'DARTS', 'SNOOKER', 'VOLLEYBALL',
                              'ICE HOCKEY', 'HANDBALL']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Load CMS app & Check In Play module is enabled under Header submenus
        EXPECTED: In Play header submenu is enabled in CMS
        """
        # ************************** Verification of In Play Widget in CMS **************************************
        inplay_status = self.get_initial_data_system_configuration().get('DesktopWidgetsToggle').get('inPlay')
        if not inplay_status:
            self.cms_config.update_system_configuration_structure(config_item='DesktopWidgetsToggle',
                                                                  field_name='inPlay', field_value=True)
        # ************************** Verification of In Play header submenu in CMS **************************************
        header_submenus = self.cms_config.get_header_submenus()
        header_submenus_list = [header_submenu.get('linkTitle').upper() for header_submenu in header_submenus]
        for header_submenu in header_submenus:
            if "IN-PLAY" in header_submenus_list:
                if header_submenu.get('linkTitle') == "In-Play":
                    if header_submenu.get('disabled') is False and header_submenu.get('inApp') is True:
                        self._logger.info('In Play header sub menu is configured in CMS')
                        break
                    else:
                        self.cms_config.update_header_submenu(header_submenu_id=header_submenu.get('id'), inApp=True, disabled=False)
                        break
            else:
                self.cms_config.create_header_submenu(name="In-Play", target_url='in-play')
                break

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: User should be able to launch the application successfully.
        """
        # ************************** Navigating to In Play header submenu **************************************
        self.site.wait_content_state(state_name='HomePage', timeout=5)
        actual_header_sub_menu = self.site.header.sport_menu.items_as_ordered_dict
        self.assertTrue(actual_header_sub_menu, msg='Header sub menu is not available')
        actual_header_sub_menu.get('IN-PLAY').click()
        self.site.wait_content_state(state_name='InPlay')
        # ************************** Getting In Play Tier 2 Sports **************************************
        sports = self.get_inplay_sport_menu_items()
        self.__class__.tier_2_in_play_sports = [sport_name for sport_name, sport in sports.items() if sport.counter > 0 and sport_name.upper() in self.expected_tier_2_sports]
        self.__class__.tier_2_in_play_sports = self.tier_2_in_play_sports[:2] if len(self.tier_2_in_play_sports) > 2 else self.tier_2_in_play_sports
        if len(self.tier_2_in_play_sports) == 0:
            raise VoltronException(f'Tier 2 sports {self.expected_tier_2_sports} are not having live events')

    def test_002_navigate_to_any_tier2_slp(self):
        """
        DESCRIPTION: Navigate to any Tier2 SLP.
        EXPECTED: User should be able to navigate to any Tier2 SLP.
        """
        # ************************** Navigating to SLP page and Verifying In Play Widget **************************************
        tier_two_sports_category = {'TABLE TENNIS': 59, 'ICE HOCKEY': 22,
                                    'CRICKET': self.ob_config.cricket_config.category_id, 'ESPORTS': 148,
                                    'BASEBALL': self.ob_config.baseball_config.category_id,
                                    'DARTS': self.ob_config.darts_config.category_id,
                                    'SNOOKER': self.ob_config.snooker_config.category_id,
                                    'VOLLEYBALL': self.ob_config.volleyball_config.category_id,
                                    'HANDBALL': self.ob_config.handball_config.category_id, }
        for sport_name in self.tier_2_in_play_sports:
            # self.site.open_sport(name=sport_name)
            self.navigate_to_page(name="sport/"+sport_name.lower().replace(' ', '-'))
            self.site.wait_content_state_changed(timeout=10)
            tabs = self.site.sports_page.tabs_menu.items_as_ordered_dict
            current_tab = self.site.sports_page.tabs_menu.current
            expected_tab = self.get_sport_tab_name(
                        self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,category_id=tier_two_sports_category[sport_name.upper()] )
            if current_tab.upper() != expected_tab:
                tab = next((tab for tab_name, tab in tabs.items() if tab_name.upper() == expected_tab), None)
                tab.click()
                current_tab = self.site.sports_page.tabs_menu.current
                self.assertEqual(current_tab.upper(), expected_tab, msg=f'Expected tab name {expected_tab} but actual is {current_tab.upper()}')
            sections = self.site.sports_page.in_play_widget.items_as_ordered_dict
            expected_in_play_widget = ''.join(f"IN-PLAY LIVE {sport_name.upper()}".split())
            actual_in_play_widgets = [''.join(section_name.upper().split()) for section_name in sections]
            self.assertIn(expected_in_play_widget, actual_in_play_widgets, msg=f'expected in play widget {expected_in_play_widget} is not available in actual widgets {actual_in_play_widgets}')

    def test_003_verify_inplay_module_in_slp_matches_tab(self):
        """
        DESCRIPTION: Verify Inplay module in SLP matches tab.
        EXPECTED: User should be able to see inplay module in SLP matches tab.
        """
        # Covered in test_002_navigate_to_any_tier2_slp

    def test_004_repeat_above_steps_for_all_tire2_sports(self):
        """
        DESCRIPTION: Repeat above steps for all Tire2 sports.
        EXPECTED: 
        """
        # Covered in test_002_navigate_to_any_tier2_slp
