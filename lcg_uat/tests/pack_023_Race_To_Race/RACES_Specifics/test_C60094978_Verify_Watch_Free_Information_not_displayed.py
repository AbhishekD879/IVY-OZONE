import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not create event in prod
@pytest.mark.low
@pytest.mark.event_details
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.watch_free
@vtest
class Test_C60094978_Verify_Watch_Free_Information_not_displayed(BaseRacing):
    """
    TR_ID: C60094978
    NAME: Verify Watch Free Information-not displayed
    DESCRIPTION: Verify Watch Free Information is no longer displayed in both the brands
    PRECONDITIONS: **Jira tickets: **
    PRECONDITIONS: *   BMA-17787 Live Sim/Watch Free Display Change for Information Pop Up
    PRECONDITIONS: *   BMA-19409 Change the wording in the QL Watch Free Pop Up
    PRECONDITIONS: *   Applicaiton is loaded
    PRECONDITIONS: *   Horse Racing Landing page is opened
    PRECONDITIONS: *   Make sure there is mapped race visualization for tested event
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: **NOTE**: not all UK&IRE races can have LiveSim visuaisation mapped by Quantum Leap. If event is present in this feed then it should have QL LiveSim mapped: http://xmlfeeds-tst2.coral.co.uk/oxi/pub?template=getEvents&class=223
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        cms_horse_tab_name = self.get_sport_title(category_id=21)
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            if not self.brand == 'ladbrokes':
                all_items.get(cms_horse_tab_name.upper()).click()
                self.site.wait_content_state_changed()
            else:
                all_items.get(cms_horse_tab_name).click()
        else:
            all_items = self.site.header.sport_menu.items_as_ordered_dict
            all_items.get(cms_horse_tab_name.upper()).click()
        wait_for_result(lambda: self.site.wait_content_state('Horseracing'), timeout=30)

    def test_003_go_to_the_event_details_page_with_race_visualization_mapping(self):
        """
        DESCRIPTION: Go to the event details page with race visualization mapping
        """
        event_params = self.ob_config.add_UK_racing_event(is_live=True, at_races_stream=True, time_to_start=6)
        self.navigate_to_edp(event_id=event_params.event_id, sport_name='horse-racing')

    def test_004_navigate_to_media_area(self):
        """
        DESCRIPTION: Navigate to media area
        EXPECTED: **For mobile&tablet:**
        EXPECTED: * Twо buttons 'PRE-PARADE' and 'WATCH' are displayed and inActive
        EXPECTED: **For desktop:**
        EXPECTED: * Twо switchers 'PRE-PARADE' and 'WATCH' are displayed and inActive
        """
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                        msg=f'"PRE-PARADE" button is not displayed')
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                        msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not active')

    def test_005_tap_inactive_pre_parade_button_and_verify_that_watch_free_text_is_no_longer_displayed(self):
        """
        DESCRIPTION: Tap inActive 'PRE-PARADE' button and verify that Watch free text is no longer displayed
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   'PRE-PARADE' button becomes Active
        EXPECTED: *   Visualisation video object is shown
        """
        self.horse_racing_edp.watch_free_button.click()
        if not self.device_type == 'mobile':
            self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                            msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not displayed')
        else:
            self.assertTrue(self.horse_racing_edp.watch_free_button.is_selected(),
                            msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not active')
        self.assertEqual(self.horse_racing_edp.watch_free_button.name, vec.sb.DONE.upper(),
                         msg=f'Button "{self.horse_racing_edp.watch_free_button.name}" not '
                             f'changed label to "{vec.sb.DONE.upper()}"')
        stream_button = self.horse_racing_edp.video_stream_button
        self.assertFalse(stream_button.is_selected(expected_result=False),
                         msg=f'"{stream_button.name}" button is active')
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=10)
        self.assertTrue(result, msg='Visualisation video is not shown')
