import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.desktop_only
@pytest.mark.adhoc_suite
@pytest.mark.in_play
@vtest
class Test_C65946733_Verify_Inplay_and_live_stream_tabs_in_home_page_Inplay_module(Common):
    """
    TR_ID: C65946733
    NAME: Verify Inplay and live stream tabs in home page (Inplay module).
    DESCRIPTION: This testcase verifies Inplay and live stream tabs in home page (Inplay module).
    PRECONDITIONS: Verify with Login/logout user.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    is_in_play_available_in_cms = False

    def test_000_pre_conditions(self):
        header_submenus = self.cms_config.get_header_submenus()
        self.__class__.is_in_play_available_in_cms = next((True for header_details in header_submenus if header_details.get('linkTitle').upper() == 'IN-PLAY'), False)


    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: User should be able to launch the application successfully.
        """
        self.site.go_to_home_page()

    def test_002_verify_inplay_module_in_home_page(self):
        """
        DESCRIPTION: Verify In-play module in home page.
        EXPECTED: User should be able to see the In-play module in home page.
        """
        pass

    def test_003_verify_inplay_and_live_streaming(self):
        """
        DESCRIPTION: Verify "In-play and live streaming".
        EXPECTED: User should be able to see the "In-play and live streaming".
        """
        in_play_live_stream = self.site.home.desktop_modules.inplay_live_stream_module
        self.assertEqual('IN-PLAY AND LIVE STREAM', in_play_live_stream.name,
                         f'Actual Name of module : {in_play_live_stream.name} is not same as '
                         f'Expected Name of Module : {"IN-PLAY AND LIVE STREAM"}')

        tabs = in_play_live_stream.tabs_menu.items_as_ordered_dict
        self.assertTrue(tabs, '"Switchers" is not displayed in "IN-PLAY AND LIVE STREAM" MODULE')
        default_tab = in_play_live_stream.tabs_menu.current
        self.assertEqual(default_tab.upper(), 'IN-PLAY', f'Actual Selected Tab is "{default_tab}" is not same as '
                                                         f'Expected Selected Tab is "IN-PLAY"')
        in_play_tab_name, in_play_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                              tab_name.upper() == 'IN-PLAY'),
                                             [None, None])
        live_stream_name, live_stream_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                                  tab_name.upper() == 'LIVE STREAM'),
                                                 [None, None])
        self.assertIsNotNone(live_stream_name, '"LIVE STREAM" is not displayed inside "IN-PLAY AND LIVE STREAM" MODULE')
        live_stream_tab.click()
        self.assertTrue(live_stream_tab.is_selected(), f'{live_stream_name} is not selected after clicking on it')
        in_play_tab.click()
        self.assertTrue(in_play_tab.is_selected(), f'{in_play_tab} is not selected after clicking on it')

    def test_004_verify_switching_between_live_now_and_upcoming_tabs(self):
        """
        DESCRIPTION: Verify switching between live now and upcoming tabs.
        EXPECTED: User should be able to switch between live now and
        EXPECTED: upcoming tabs by clicking on it.
        """
        if self.is_in_play_available_in_cms:
            all_sub_headers = self.site.header.sport_menu.items_as_ordered_dict
            sub_header_in_play = next((sport for sport_name, sport in all_sub_headers.items() if
                                       sport_name.upper() == 'IN-PLAY'),
                                      None)
            self.assertIsNotNone(sub_header_in_play, 'IN-PLAY is not displayed in sub header...')
            sub_header_in_play.click()
        else:
            self.navigate_to_page('in-play')
        tabs = self.site.inplay.tab_content.grouping_buttons.items_as_ordered_dict
        live_now_tab_name, live_now_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                                tab_name.upper() == 'LIVE NOW'),
                                               [None, None])
        self.assertIsNotNone(live_now_tab_name, '"LIVE NOW" is not present')
        upcoming_tab_name, upcoming_tab = next(([tab_name, tab] for tab_name, tab in tabs.items() if
                                                tab_name.upper() == 'UPCOMING'),
                                               [None, None])
        self.assertIsNotNone(upcoming_tab_name, '"UPCOMING" is not present')
        self.assertTrue(live_now_tab.is_selected(), f'"{live_now_tab_name}" is not active by default')
        upcoming_tab.click()
        self.assertTrue(upcoming_tab.is_selected(), f'"{upcoming_tab_name}" is not active after clicking on it')
        live_now_tab.click()
        self.assertTrue(live_now_tab.is_selected(), f'"{live_now_tab_name}" is not active after clicking on it')

        self.site.back_button.click()

    def test_005_login_and_repeat_the_above_steps(self):
        """
        DESCRIPTION: Login to application and repeat above steps
        """
        self.site.login()
        self.test_003_verify_inplay_and_live_streaming()
        self.test_004_verify_switching_between_live_now_and_upcoming_tabs()
