import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C9770807_Re_establishing_connection_and_receiving_updates_after_OpenBet_request_failed(Common):
    """
    TR_ID: C9770807
    NAME: Re-establishing connection and receiving updates after OpenBet request failed
    DESCRIPTION: This test case verifies re-establishing a connection to Greyhounds and receiving updates after OpenBet request failed in order to receive the latest Greyhounds Next races Events data.
    PRECONDITIONS: 1. "Next Races" tab should be enabled in CMS(CMS -> system-configuration -> structure -> GreyhoundNextRacesToggle-> nextRacesTabEnabled)
    PRECONDITIONS: 2. Load Oxygen app
    PRECONDITIONS: 3. Race events are available for the current day
    PRECONDITIONS: 4. Navigate to Greyhounds "Next races" Tab
    """
    keep_browser_open = True

    def test_001_to_emulate_the_openbet_request_failed_use_network__select_class__block_request_url(self):
        """
        DESCRIPTION: To emulate the OpenBet request failed, use Network > select 'Class' > Block request URL
        EXPECTED: 
        """
        pass

    def test_002_refresh_the_pageverify_next_races_tab(self):
        """
        DESCRIPTION: Refresh the page
        DESCRIPTION: Verify Next races tab
        EXPECTED: "Server is unavailable at the moment, please try again later.
        EXPECTED: If this problem persists, contact our Customer Service Department" and button "Reload" are displayed.
        """
        pass
