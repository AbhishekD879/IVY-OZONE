import pytest
from tests.base_test import vtest
from time import sleep
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound


# @pytest.mark.tst2 # Racing Post Info is not available
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.other
@pytest.mark.desktop
@vtest
class Test_C64749892_Verify_RacingPost_widget_displaying(BaseGreyhound):
    """
    TR_ID: C64749892
    NAME: Verify RacingPost widget displaying
    DESCRIPTION: This testcase Verifies RacingPost
    DESCRIPTION: widget displaying
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have CMS access
        PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
        PRECONDITIONS: when enabled - Racingpost info should be displayed.
        """
        racing_datahub_status = self.get_initial_data_system_configuration().get('RacingDataHub')[
            "isEnabledForGreyhound"]
        if not racing_datahub_status:
            self.cms_config.update_system_configuration_structure(config_item='RacingDataHub',
                                                                  field_name='isEnabledForGreyhound',
                                                                  field_value=True)

    def test_001_load_oxygen_appgo_to_the_greyhounds_landing_pageselect_event_with_racingpost_available_and_go_to_its_details_pageverify_racingpost_widget(self):
        """
        DESCRIPTION: Load Oxygen app
        DESCRIPTION: Go to the Greyhounds landing page
        DESCRIPTION: Select event with RacingPost available and go to its details page
        DESCRIPTION: Verify RacingPost widget
        EXPECTED: Homepage is loaded
        EXPECTED: Greyhounds landing page is opened
        EXPECTED: * Event details page is opened
        EXPECTED: * RacingPost widget is located in Main Column under selections list
        EXPECTED: RacingPost consists of racing post image (as per the Zeplin links) based on the previous performance of the dogs (ratings).
        """
        self.site.wait_content_state('Homepage', timeout=10)
        event_id = self.get_event_details(racing_post_pick=True).event_id
        self.navigate_to_edp(event_id=event_id, sport_name='greyhound-racing', timeout=10)
        self.site.wait_content_state(state_name='GreyHoundEventDetails')
        racing_post_overview = self.site.greyhound_event_details.tab_content.post_info
        self.assertTrue(racing_post_overview, msg='Racing Post widget is not displayed')
        sleep(3)
        self.assertTrue(self.site.greyhound_event_details.tab_content.post_info.has_logo_icon(),
                        msg='Racing Post logo icon is not found')
        racingpost_pick = self.site.greyhound_event_details.tab_content.post_info.items_names
        self.assertTrue(racingpost_pick, msg='Racing Post pick values are not displayed')
