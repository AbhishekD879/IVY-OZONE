import pytest
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseGreyhound


# @pytest.mark.tst2 # Racing Post Info is not available
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.racing
@pytest.mark.greyhounds
@pytest.mark.event_details
@pytest.mark.other
@pytest.mark.desktop
@vtest
class Test_C64749894_No_data_from_RacingPost(BaseGreyhound):
    """
    TR_ID: C64749894
    NAME: No data from RacingPost
    DESCRIPTION: This testcase verifies when there is
    DESCRIPTION: No data from RacingPost
    PRECONDITIONS: User should have CMS access
    PRECONDITIONS: Greyhounds (GH) Racing Data Hub toggle is turned on: System-configuration > RacingDataHub > isEnabledForGreyhound = true
    PRECONDITIONS: when enabled - Racingpost info should be displayed.
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        racing_datahub_status = self.get_initial_data_system_configuration().get('RacingDataHub')[
            "isEnabledForGreyhound"]
        if not racing_datahub_status:
            self.cms_config.update_system_configuration_structure(config_item='RacingDataHub',
                                                                  field_name='isEnabledForGreyhound',
                                                                  field_value=True)

    def test_001_open_greyhound_event_details_pageverify_racingpost_overview(self):
        """
        DESCRIPTION: Open Greyhound Event Details Page
        DESCRIPTION: Verify RacingPost overview
        EXPECTED: RacingPost overview is NOT displayed
        """
        event_id = self.get_event_details(racing_post_pick=False).event_id
        self.navigate_to_edp(event_id=event_id, sport_name="greyhound-racing")
        self.assertFalse(self.site.greyhound_event_details.tab_content.has_post_info(),
                         msg='Racing Post info is found')
