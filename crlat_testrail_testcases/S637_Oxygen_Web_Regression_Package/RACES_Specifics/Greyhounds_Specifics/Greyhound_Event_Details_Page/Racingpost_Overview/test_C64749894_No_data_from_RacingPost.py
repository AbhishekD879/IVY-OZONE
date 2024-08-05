import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C64749894_No_data_from_RacingPost(Common):
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

    def test_001_open_greyhound_event_details_pageverify_racingpost_overview(self):
        """
        DESCRIPTION: Open Greyhound Event Details Page
        DESCRIPTION: Verify RacingPost overview
        EXPECTED: RacingPost overview is NOT displayed
        """
        pass
