import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.environments import constants as vec
from time import sleep


# @pytest.mark.tst2  # Very often absence of bog, promotions, raceForm, etc.
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.races
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@vtest
class Test_C60094971_Verify_the_display_of_BOG_Pop_up(BaseRacing):
    """
    TR_ID: C60094971
    NAME: Verify the display of BOG Pop-up
    DESCRIPTION: This test case verify BOG help text in pop up when click on BOG signpost
    PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
    PRECONDITIONS: 2. BOG Signposting, Pop-up configured with Header, Pop-up text and Link in CMS (CMS > Promotions > Promotions)
    PRECONDITIONS: 3. Events with market configured to show BOG flag available (Market should have 'GP Available' 'SP Available' and 'LP Available' checkmarks)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. BOG has been enabled in CMS(Sysytem config)
        """
        bog_toggle_status = self.cms_config.get_initial_data(device_type=self.device_type)['systemConfiguration']['BogToggle']['bogToggle']
        if not bog_toggle_status:
            self.cms_config.update_system_configuration_structure(config_item='BogToggle', field_name='bogToggle',
                                                                  field_value=True)
            bog_toggle = self.cms_config.get_system_configuration_structure()['BogToggle']['bogToggle']
            self.assertTrue(bog_toggle, msg='"Bog toggle" is not enabled in CMS')
        self.assertTrue(bog_toggle_status, msg='"Bog toggle" is not enabled in CMS')

    def test_001_launch_ladbrokescoral_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/Coral URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: Ladbrokes/Coral URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state(state_name='Homepage')

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        self.navigate_to_page('horse-racing')
        self.site.wait_content_state('horse-racing')

    def test_003_click_on_bog_sign_post(self):
        """
        DESCRIPTION: Click on BOG sign post
        EXPECTED: User should be displayed Pop-up with OK button
        """
        sections = self.site.horse_racing.tab_content.accordions_list.items_as_ordered_dict
        self.site.wait_splash_to_hide(timeout=60)
        self.assertTrue(sections, msg='Failed to display any section')
        found_bog = False
        for section_name, section in sections.items():
            if section_name in vec.racing.COUNTRY_SKIP_LIST or self.next_races_title in section_name:
                continue
            else:
                meetings = section.items_as_ordered_dict
                self.assertTrue(meetings, msg='Failed to display any meeting')
                for meeting_name, meeting in meetings.items():
                    events = meeting.items_as_ordered_dict
                    self.assertTrue(events, msg='Failed to display any event')
                    for event_name, event in events.items():
                        if 'race-on' in event.get_attribute('class'):
                            event.click()
                            markets_tab = self.site.racing_event_details.tab_content.event_markets_list.market_tabs_list.open_tab(vec.racing.RACING_EDP_MARKET_TABS.win_or_ew)
                            self.assertTrue(markets_tab, msg='No market tabs found on EDP')
                            sections = self.site.racing_event_details.tab_content.event_markets_list.items_as_ordered_dict
                            self.assertTrue(sections, msg='No sections found')
                            section = list(sections.values())[0]
                            if section.section_header.is_bpg_icon_present():
                                self.assertTrue(section.section_header.is_bpg_icon_present(), msg='BPG icon is not shown')
                                section.section_header.bog_icon.click()
                                sleep(2)
                                bog_dialog = self.site.wait_for_dialog(dialog_name=vec.Dialogs.DIALOG_MANAGER_BEST_ODDS_GUARANTEED, timeout=60)
                                self.assertTrue(bog_dialog,
                                                msg=f'"{vec.dialogs.DIALOG_MANAGER_BEST_ODDS_GUARANTEED}" dialog is not displayed')
                                self.assertTrue(bog_dialog.ok_button.is_displayed(), msg='"ok button" is not displayed')
                                bog_dialog.ok_button.click()
                                self.site.wait_splash_to_hide(timeout=45)
                                self.assertFalse(bog_dialog.is_displayed(expected_result=False),
                                                 msg=f'"{vec.dialogs.DIALOG_MANAGER_BEST_ODDS_GUARANTEED}" dialog is displayed')
                                found_bog = True
                            break
                    if found_bog is True:
                        break
                    else:
                        continue
                if found_bog is True:
                    break
                else:
                    continue
        if found_bog is None:
            self._logger("'No events found with BOG ")
            exit()
        self.site.wait_content_state_changed()

    def test_004_click_on_ok_button(self):
        """
        DESCRIPTION: Click on OK button
        EXPECTED: Pop-up should be closed
        """
        # covered in step3
