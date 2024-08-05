import pytest
import re
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.tst2
# @pytest.mark.stg2  #TC is not applicable for tst2 and stg2
@pytest.mark.prod
@pytest.mark.low
@pytest.mark.races
@pytest.mark.next_races
@pytest.mark.mobile_only
@pytest.mark.horseracing
@pytest.mark.reg165_fix
@vtest
class Test_C60094907_Verify_adding_selection_to_Bet_slip_from_Next_races_tab(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C60094907
    NAME: Verify adding selection to Bet slip from Next races tab
    DESCRIPTION: Verify that User is able to add selections to Bet slip from races displayed in the Next races tab
    PRECONDITIONS: 1: Horse racing event should be available in Next races tab
    PRECONDITIONS: 2: Next races tab should be enabled in CMS
    PRECONDITIONS: CMS Configuration
    PRECONDITIONS: 1: System configuration > Structure > Next races toggle
    PRECONDITIONS: 2: System configuration > Structure > Next races
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: "Next Races" should be enabled in CMS (CMS -> system-configuration -> structure -> NextRacesToggle-> nextRacesTabEnabled=true)
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
        if self.brand == 'ladbrokes':
            self.navigate_to_page('horse-racing')
            self.site.wait_content_state('Horseracing')
        else:
            self.site.wait_content_state('homepage')

    def test_002_ladbrokesclick_on_horse_racing_from_sports_ribbon_or_from_menucoralnavigate_to_home_page(self):
        """
        DESCRIPTION: Ladbrokes:
        DESCRIPTION: Click on Horse racing from sports ribbon or from Menu
        DESCRIPTION: Coral:
        DESCRIPTION: Navigate to Home page
        EXPECTED: Ladbrokes:
        EXPECTED: Click on Horse racing from sports ribbon or from Menu
        EXPECTED: Coral:
        EXPECTED: Navigate to Home page
        """
        # Covered in step 1

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
        expected_module = vec.racing.NEXT_RACES.upper()
        if self.brand == 'ladbrokes':
            next_races_tab = self.site.horse_racing.tabs_menu.click_button(
                button_name=expected_module)
        else:
            self.site.home.tabs_menu.click_button(button_name=vec.sb.TABS_NAME_NEXT.upper())
            sleep(2)
            next_races_tab = self.site.home.tabs_menu.current
        self.assertTrue(next_races_tab,
                        msg=f'"{vec.sb.TABS_NAME_NEXT.upper()}" tab is not selected after cliuck')
        if self.brand == 'ladbrokes':
            self.__class__.sections = self.get_sections('horse-racing')
        else:
            self.__class__.sections = self.site.home.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No race sections are found in next races')
        for race_name, race in list(self.sections.items())[:2]:
            self.assertTrue(race.name.split(" ")[0],
                            msg=f'"Event Time" not found for race: "{race_name}"')
            self.assertTrue(race.name.split(" ")[1],
                            msg=f'"Meeting name" not found for race: "{race_name}"')
            self.site.wait_content_state_changed()
            if self.brand == 'ladbrokes':
                if race.header.has_timer():
                    timer = race.header.timer.text.lower().split("in")[1]
                    self.assertTrue(timer and re.match(r'\d{2}:\d{2}', timer),
                                    msg=f'Countdown timer "{timer}"'
                                        f' has incorrect format. Expected format: "XX:XX"')
                self.assertTrue(race.header.has_view_full_race_card(),
                                msg=f'"More" link is not found for race: "{race_name}"')
            else:
                if race.has_timer():
                    timer = race.timer.text
                    self.assertTrue(timer and re.match(r'\d{2}:\d{2}', timer),
                                    msg=f'Countdown timer "{timer}" has incorrect format. Expected format: "XX:XX"')
                self.assertTrue(race.has_view_full_race_card(),
                                msg=f'"More" link is not found for race: "{race_name}"')

    def test_004_click_on_any_selection_odd_price(self):
        """
        DESCRIPTION: Click on any Selection Odd (Price)
        EXPECTED: 1: User should be able to add the selection to Bet slip
        EXPECTED: 2: If it is the first selection user made, Quick Bet should be displayed else the counter displayed at the Bet slip should be increased by one
        """
        first_event = list(self.sections.values())[0]
        selection1 = list(first_event.runners.items_as_ordered_dict.values())[0]
        selection2 = list(first_event.runners.items_as_ordered_dict.values())[1]

        for index in range(2):
            betslip_counter = self.site.header.bet_slip_counter.counter_value
            if not betslip_counter == '0':
                sleep(5)
                selection2.bet_button.click()
                self.site.wait_content_state_changed()
                self.verify_betslip_counter_change(expected_value="2")
            else:
                selection1.bet_button.click()
                self.site.wait_content_state_changed()
                self.assertTrue(self.site.wait_for_quick_bet_panel(expected_result=True),
                                msg='Quick Bet is not present')
                self.site.quick_bet_panel.header.close_button.click()
                self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False),
                                 msg='Quick Bet is not closed')
