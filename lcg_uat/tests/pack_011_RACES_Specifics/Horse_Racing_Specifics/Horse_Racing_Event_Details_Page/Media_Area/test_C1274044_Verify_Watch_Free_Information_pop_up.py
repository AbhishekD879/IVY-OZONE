import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.watch_free
@pytest.mark.desktop
@pytest.mark.races
@pytest.mark.issue('https://jira.egalacoral.com/browse/BMA-46367')
@vtest
class Test_C1274044_Verify_Watch_Free_Information_pop_up(BaseRacing):
    """
    TR_ID: C1274044
    NAME: Verify Watch Free Information pop-up
    DESCRIPTION: This Test Case verified Watch Free Information pop-up message.
    NOTE: This was removed for Ladbrokes - BMA-44862
    PRECONDITIONS: *   Applicaiton is loaded
    PRECONDITIONS: *   Horse Racing Landing page is opened
    PRECONDITIONS: *   Make sure there is mapped race visualization for tested event
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: **NOTE**: not all UK&IRE races can have LiveSim visuaisation mapped by Quantum Leap. If event is present in this feed then it should have QL LiveSim mapped: http://xmlfeeds-tst2.coral.co.uk/oxi/pub?template=getEvents&class=223
    """
    keep_browser_open = True
    maxDiff = None
    dialog = None
    expected_watch_free_text = f'{vec.sb_desktop.WATCH_FREE_CONTENT_TITLE}\n{vec.sb_desktop.WATCH_FREE_CONTENT_P_1}\n' \
                               f'{vec.sb_desktop.WATCH_FREE_CONTENT_P_2}\n{vec.sb_desktop.WATCH_FREE_CONTENT_P_3}\n' \
                               f'{vec.sb_desktop.WATCH_FREE_CONTENT_P_4}\n{vec.sb_desktop.WATCH_FREE_CONTENT_P_5}\n' \
                               f'{vec.sb_desktop.WATCH_FREE_FOOTER}'

    def test_000_go_to_the_event_details_page_with_race_visualization_mapping(self):
        """
        DESCRIPTION: Add racing event with start time more than 5 minutes to UK & IRE types
        EXPECTED: Racing event added
        """
        event_params = self.ob_config.add_UK_racing_event()
        self.__class__.eventID, self.__class__.event_off_time, = event_params.event_id, event_params.event_off_time
        self.__class__.created_event_name = f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}'
        self.__class__.devise_is_mobile = self.device_type == 'mobile'

    def test_001_navigate_to_media_area(self):
        """
        DESCRIPTION: Navigate to media area
        EXPECTED: **For mobile&tablet:"
        EXPECTED: * Twо buttons 'WATCH FREE' and 'LIVE STREAM' are displayed and inActive
        EXPECTED: **For desktop:**
        EXPECTED: * Twо switchers 'WATCH FREE' and 'LIVE STREAM' are displayed and inActive
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertTrue(self.horse_racing_edp.has_watch_free_button(),
                        msg=f'Watch Free button was not found for event "{self.created_event_name}"')
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(expected_result=False),
                         msg='Watch Free button is active')

    def test_002_tap_inactive_watch_free_button(self):
        """
        DESCRIPTION: Tap inActive 'WATCH FREE' button
        EXPECTED: * The area below 'WATCH FREE' button is expanded
        EXPECTED: * 'WATCH FREE' button becomes Active
        EXPECTED: * Visualisation video object is shown
        EXPECTED: **For mobile&tablet:**
        EXPECTED: * An information link labeled "Find out more about Watch Free here" appears under Media Area on the page
        EXPECTED: **For desktop:**
        EXPECTED: * "Find out more about Watch Free" widget is displayed in the 3rd column or below the event card
        """
        self.horse_racing_edp.watch_free_button.click()
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertTrue(result, msg='Visualisation video is shown')
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_selected(),
                        msg='Watch Free button is not active')
        if self.devise_is_mobile:
            self.assertTrue(self.horse_racing_edp.has_watch_free_info_link(),
                            msg='Watch Free info link is not present')
        else:
            sections = self.horse_racing_edp.accordions_list.items_as_ordered_dict
            self.__class__.watch_free_widget = sections.get(vec.sb_desktop.WATCH_FREE_HEADER.title())
            self.assertTrue(self.watch_free_widget, msg=f'Can not find section: "{vec.sb_desktop.WATCH_FREE_HEADER}"')

    def test_003_tap_on_find_out_more_about_watch_free_here_information_link_for_mobile_tablet(self):
        """
        DESCRIPTION: Tap on "Find out more about Watch Free here" information link For mobile&tablet
        EXPECTED: Information pop-up is appears
        """
        if self.devise_is_mobile:
            self.horse_racing_edp.watch_free_info_link.click()
            self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_EVERY_RACE_ANGLE_DAY,
                                                              timeout=15)
            self.assertTrue(self.dialog, msg='Watch Free information pop up was not opened')

    def test_004_check_the_elements_on_information_pop_up_for_mobile_tablet_on_widget_for_desktop(self):
        """
        DESCRIPTION: Check the elements on Information pop-up For mobile&tablet
        DESCRIPTION: Check the elements on "Find out more about Watch Free" widget For desktop
        EXPECTED: **For mobile&tablet:**
        EXPECTED: *   Pop-up is contained a Close ('X') button
        EXPECTED: *   Pop-up header name is “EVERY RACE, EVERY ANGLE, EVERY DAY …”
        EXPECTED: *   Pop-up is contained a an 'OK' button
        EXPECTED: *   Pop-up is included the 'Watch Free' logo
        EXPECTED: *   Pop-up is contained corresponding content
        EXPECTED: **For desktop:**
        EXPECTED: *   Widget is included the 'Watch Free' logo

        """
        if self.devise_is_mobile:
            header_text = self.dialog.name
            self.assertEqual(header_text, vec.dialogs.DIALOG_MANAGER_EVERY_RACE_ANGLE_DAY,
                             msg=f'Watch Free info pop up header "{header_text}" is not the same as expected '
                                 f'"{vec.dialogs.DIALOG_MANAGER_EVERY_RACE_ANGLE_DAY}"')
            self.assertTrue(self.dialog.has_close_button(), msg='Pop up does not have close button')
            self.assertTrue(self.dialog.has_ok_button(), msg='Pop up does not have OK button')
            self.assertTrue(self.dialog.has_watch_free_logo(), msg='Pop up does not have Watch Free logo')
        else:
            self.assertTrue(self.horse_racing_edp.has_watch_free_logo(),
                            msg="Widget does not have Watch Free logo")

    def test_005_check_the_content_on_information_pop_up_for_mobile_tablet_on_widget_for_desktop(self):
        """
        DESCRIPTION: Check the content on Information pop-up For mobile&tablet
        DESCRIPTION: Check the content on "Find out more about Watch Free" widget For desktop
        EXPECTED: The message content must read as follows:
        EXPECTED: “Watch Free brings your favourite races live to your mobile or tablet.
        EXPECTED: This exciting addition really takes you into the heart of the action with four unique camera angles.
        EXPECTED: You’ll get a ‘so real you could be there’ Jockey view where you’re in the saddle, the classic trackside view and views from the 1st Favourite and 2nd Favourite angles respectively.
        EXPECTED: Race commentary is also included to fully complete the ‘live’ race experience.
        EXPECTED: Watch free even displays winning percentages so you can keep up with all the latest race betting.
        EXPECTED: Remember that Watch Free will activate 15 minutes before each race so just make a note of the start time, and click on ‘Watch Free’ in that pre-race window.
        EXPECTED: Enjoy watching your chosen races live – for FREE!”
        """
        if self.devise_is_mobile:
            pop_up_text = self.dialog.text.replace('OK', '').strip()
            self.assertEqual(pop_up_text, self.expected_watch_free_text,
                             msg=f'Actual text from popup \n"{pop_up_text}"\n don\'t match expected \n '
                                 f'"{self.expected_watch_free_text}"')
        else:
            widget_text = self.watch_free_widget.content.text.lower()
            self.assertEqual(widget_text, self.expected_watch_free_text.lower(),
                             msg=f'Actual text from widget \n"{widget_text}" \n don\'t match expected \n '
                                 f'"{self.expected_watch_free_text.lower()}"')

    def test_006_tap_on_close_x_button_on_the_information_pop_up_for_mobile_tablet(self):
        """
        DESCRIPTION: Tap on Close ('X') button on the Information pop-up For mobile&tablet
        EXPECTED: *   The pop-up message is closed
        EXPECTED: *   User is stayed on the same page they clicked the link from
        """
        if self.devise_is_mobile:
            self.dialog.close_dialog()
            self.site.wait_content_state(state_name='RacingEventDetails')

    def test_007_tap_on_find_out_more_about_watch_free_here_information_link_one_more_time_for_mobile_tablet(self):
        """
        DESCRIPTION: Tap on "Find out more about Watch Free here" information link one more time For mobile&tablet
        EXPECTED: Information pop-up is appears
        """
        if self.devise_is_mobile:
            self.test_003_tap_on_find_out_more_about_watch_free_here_information_link_for_mobile_tablet()

    def test_008_tap_on_ok_button_on_the_information_pop_up_for_mobile_tablet(self):
        """
        DESCRIPTION: Tap on 'OK' button on the Information pop-up For mobile&tablet
        EXPECTED: *   The pop-up message is closed
        EXPECTED: *   User is stayed on the same page they clicked the link from
        """
        if self.devise_is_mobile:
            self.dialog.click_ok()
            self.assertTrue(self.dialog.wait_dialog_closed(), msg='Information pop-up is not closed')
            self.site.wait_content_state(state_name='RacingEventDetails')
