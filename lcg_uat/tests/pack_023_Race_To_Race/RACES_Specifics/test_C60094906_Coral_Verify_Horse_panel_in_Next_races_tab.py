from time import sleep
import pytest
import re
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.helpers import normalize_name


# @pytest.mark.tst2
# @pytest.mark.stg2  #TC is not applicable for tst2 and stg2
@pytest.mark.crl_prod
@pytest.mark.high
@pytest.mark.races
@pytest.mark.next_races
@pytest.mark.mobile_only
@pytest.mark.horseracing
@vtest
class Test_C60094906_Coral_Verify_Horse_panel_in_Next_races_tab(BaseRacing):
    """
    TR_ID: C60094906
    NAME: Coral: Verify Horse panel in Next races tab
    DESCRIPTION: Verify that when user clicks on Horse panel ( Not on the Prices), User is navigated to full race card( Event details page)
    PRECONDITIONS: 1: Horse racing event should be available in Next races tab
    PRECONDITIONS: 2: Next races tab should be enabled in CMS
    PRECONDITIONS: CMS Configuration
    PRECONDITIONS: 1: System configuration > Structure > Next races toggle
    PRECONDITIONS: 2: System configuration > Structure > Next races
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Next Races" should  be enabled in CMS (CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
        """
        next_races_toggle = self.get_initial_data_system_configuration().get('NextRacesToggle', {})
        if not next_races_toggle:
            next_races_toggle = self.cms_config.get_system_configuration_item('NextRacesToggle')
        if not next_races_toggle.get('nextRacesTabEnabled'):
            raise CmsClientException('Next Races Tab is not enabled for HorseRacing in CMS')

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_ladbrokesclick_on_horse_racing_from_sports_ribbon_or_from_menucoralnavigate_to_home_page(self):
        """
        DESCRIPTION: Navigate to Home page
        DESCRIPTION: Click on Horse racing from sports ribbon or from Menu
        EXPECTED: User should be navigated to Horse racing Landing page
        EXPECTED: User should be able to see Next races tab in home page
        """
        # Covered in step 3

    def test_003_click_on_next_races_tab(self):
        """
        DESCRIPTION: Click on 'Next Races' Tab
        EXPECTED: 1: User should be able to to navigate to Next races tab
        EXPECTED: 2: Horse race events which starts in next 45 mins should be displayed
        EXPECTED: 3: The following should displayed
        EXPECTED: 1:Event Time
        EXPECTED: 2:Meeting name
        EXPECTED: 3:countdown timer
        EXPECTED: 4:'SEE ALL' links in event header
        """
        self.site.home.tabs_menu.click_button(button_name=vec.sb.TABS_NAME_NEXT.upper())
        # used x` because Next race tab is taking time to reflect, other synchronization method is not working
        sleep(2)
        next_races_tab = self.site.home.tabs_menu.current
        self.assertTrue(next_races_tab, msg=f'"{vec.sb.TABS_NAME_NEXT.upper()}" tab is not selected after click')
        self.__class__.meetings = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.meetings, msg='No race sections are found in next races')
        for event in list(self.meetings.values())[0:2]:
            self.assertTrue(event.full_race_card,
                            msg=f'"SEE ALL" link is not found for race: "{event.event_name}"')
            self.assertTrue(event.name.split(" ")[0],
                            msg=f'"Event Time" not found for race: "{event.event_name}"')
            self.assertTrue(event.name.split(" ")[1],
                            msg=f'"Meeting name" not found for race: "{event.event_name}"')
            timer = event.timer.text
            if not timer == '':
                self.assertTrue(timer and re.match(r'\d{2}:\d{2}', timer),
                                msg=f'Countdown timer "{timer}" has incorrect format. Expected format: "XX:XX"')

    def test_004_click_on_horse_panel_not_on_prices(self):
        """
        DESCRIPTION: Click on Horse panel (Not on Prices)
        EXPECTED: 1: User should be able to click anywhere on Horse panel
        EXPECTED: 2: User should be navigated to Full race card (Event details page)
        """
        event = list(self.meetings.values())[0]
        link_url = event.full_race_card.get_link()
        event_id = link_url.split('?origin')[0].split('/')[-1]  # .../123456?origin...
        event_id = int(''.join(re.findall('\d+', event_id)))
        event_ss_info = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)
        ss_event_name = normalize_name(event_ss_info[0]['event']['name'])
        event.full_race_card.click()
        self.site.wait_content_state(state_name='RacingEventDetails')
        ui_event_name = self.site.racing_event_details.event_title
        ui_event_name = ui_event_name.replace('\n', ' ')
        self.assertEqual(ui_event_name, ss_event_name, msg=f'SiteServe event name "{ss_event_name}" != '
                                                           f'UI event name "{ui_event_name}"')
