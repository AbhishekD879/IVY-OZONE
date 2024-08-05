import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod  #Cannot change cms settings in production sites
# @pytest.mark.lad_hl  #Cannot change cms settings in production sites
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@vtest
class Test_C59899927_Verify_Next_Races_Runners_Number_CMS_configuration(BaseRacing):
    """
    TR_ID: C59899927
    NAME: Verify 'Next Races' Runners Number CMS configuration
    DESCRIPTION: This test case verifies Selections/runners number configuration in CMS within Next Races tab.
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS (CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: Below you may find a call from CMS with 'numberOfEvents' and Number of Selections values.
    PRECONDITIONS: Network->mobile-cms/desktop-cms ->systemConfiguration.GreyhoundNextRaces
    PRECONDITIONS: Request URL: https://cms-hl.ladbrokes.com/cms/api/ladbrokes/initial-data/mobile
    PRECONDITIONS: ![](index.php?/attachments/get/118934774)
    """
    keep_browser_open = True
    first_field_value = 3
    second_field_value = 1

    @classmethod
    def custom_tearDown(cls, **kwargs):
        cms_config = cls.get_cms_config()
        cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                         field_name='numberOfEvents',
                                                         field_value="12")

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        for i in range(4):
            self.ob_config.add_virtual_greyhound_racing_event(number_of_runners=1)

    def test_002_tap_system_configuration_section(self):
        """
        DESCRIPTION: Tap 'System-configuration' section
        EXPECTED: 'System-configuration' section is opened
        """
        # Covered in step 5

    def test_003_go_to_greyhoundnextraces_section(self):
        """
        DESCRIPTION: Go to 'GreyhoundNextRaces' section
        EXPECTED: GreyhoundNextRaces section expanded
        """
        # Covered in step 5

    def test_004_in_numberofevents_for_greyhoundenter_some_number___press_submit(self):
        """
        DESCRIPTION: In '**numberOfEvents**' (for Greyhound)enter some number -> Press 'Submit'
        EXPECTED: Changes are saved in CMS
        """
        # Covered in step 5

    def test_005_in_number_of_selections_for_greyhoundenter_some_number___press_submit8_option_should_be_set_by_default(
            self):
        """
        DESCRIPTION: In '**Number of Selections**' (for Greyhound)enter some number -> Press 'Submit'
        DESCRIPTION: ('8' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        greyhound_next_races_toggle = \
            self.cms_config.get_initial_data(device_type=self.device_type)['systemConfiguration'][
                'GreyhoundNextRacesToggle']['nextRacesTabEnabled']
        if not greyhound_next_races_toggle:
            self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRacesToggle',
                                                                  field_name='nextRacesTabEnabled', field_value=True)
        self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                              field_name='numberOfEvents',
                                                              field_value=str(self.first_field_value))

    def test_006_load_application(self):
        """
        DESCRIPTION: Load application
        EXPECTED:
        """
        self.site.wait_content_state('HomePage')

    def test_007_tap_greyhound_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Greyhound> icon from the Sports Menu Ribbon
        EXPECTED: - <Greyhound> landing page is opened
        EXPECTED: - 'Next Races' tab is available
        """
        self.navigate_to_page(name='greyhound-racing')
        self.site.wait_content_state('Greyhoundracing')
        tabs = self.site.greyhound.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.racing.NEXT_RACES.upper(), tabs,
                      msg='"Next Races" tab is not present in tabs list')

    @retry(stop=stop_after_attempt(4), wait=wait_fixed(wait=20),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_008_open_next_races_tabverify__selectionsrunners_number(self, first=True):
        """
        DESCRIPTION: Open 'Next Races' tab.
        DESCRIPTION: Verify  Selections/runners number
        EXPECTED: -Appropriate number of selections (which was set in CMS) is displayed within Next Races module/carousel
        EXPECTED: - If number of selections is less than was set in CMS -> display the remaining selections
        EXPECTED: - 'Unnamed Favourite' runner shouldn't be shown on the 'Next Races' module
        EXPECTED: ![](index.php?/attachments/get/118934773)
        """
        next_races_tab = self.site.greyhound.tabs_menu.click_button(
            button_name=vec.racing.RACING_NEXT_RACES_NAME)
        self.assertTrue(next_races_tab,
                        msg=f'"{vec.racing.RACING_NEXT_RACES_NAME}" tab is not selected after click')

        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_content_state_changed()

        sections = self.get_sections('greyhound-racing')
        self.assertTrue(sections, msg='No race sections are found in next races')
        actual_event_list = len(sections)
        if first:
            self.assertGreaterEqual(self.first_field_value, actual_event_list,
                                    msg=f'Actual Events length : "{actual_event_list}" is not less or equal '
                                        f'as expected events: "{self.first_field_value}"')
        else:
            self.assertGreaterEqual(self.second_field_value, actual_event_list,
                                    msg=f'Actual Events length : "{actual_event_list}" is not less or equal '
                                        f'as expected events: "{self.first_field_value}"')

    def test_009_go_to_cms___in_number_of_selections_enter_some_other_number___press_submit1_option_should_be_set_by_default(
            self):
        """
        DESCRIPTION: Go to CMS -> In '**Number of Selections**' enter some other number -> Press 'Submit'
        DESCRIPTION: ('1' option should be set by default)
        EXPECTED: Changes are saved in CMS
        """
        self.cms_config.update_system_configuration_structure(config_item='GreyhoundNextRaces',
                                                              field_name='numberOfEvents',
                                                              field_value=str(self.second_field_value))

    def test_010_repeat_steps_5_7(self):
        """
        DESCRIPTION: Repeat steps #5-7
        EXPECTED:
        """
        self.navigate_to_page('/')
        self.test_005_in_number_of_selections_for_greyhoundenter_some_number___press_submit8_option_should_be_set_by_default()
        self.test_007_tap_greyhound_icon_from_the_sports_menu_ribbon()
