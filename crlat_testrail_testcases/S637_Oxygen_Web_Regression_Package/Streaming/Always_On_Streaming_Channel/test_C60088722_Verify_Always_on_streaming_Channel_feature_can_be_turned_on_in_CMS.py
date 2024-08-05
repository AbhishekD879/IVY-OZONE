import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.streaming
@vtest
class Test_C60088722_Verify_Always_on_streaming_Channel_feature_can_be_turned_on_in_CMS(Common):
    """
    TR_ID: C60088722
    NAME: Verify  'Always on streaming Channel' feature  can be  turned on in CMS
    DESCRIPTION: This test case verifies that Always on streaming Channel' feature can be turned ON in CMS for Horse Racing and Greyhounds.
    DESCRIPTION: **Note:** in scope of the BMA-56229 Epic this feature is available only for Greyhounds
    PRECONDITIONS: List of CMS endpoints: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: In CMS: System Configuration > Structure > Racing TV-> Set enabledForSportIds = true for Greyhounds/Horse Racing, enabling each sport by sport id:
    PRECONDITIONS: 19 for Greyhounds
    PRECONDITIONS: 21 for Horse Racing
    PRECONDITIONS: linkShownForSportIds = true for Greyhounds/Horse Racing
    PRECONDITIONS: playerShownForSportIds = true for Greyhounds/Horse Racing
    PRECONDITIONS: 1) Load app
    """
    keep_browser_open = True

    def test_001_desktop_onlyverify_the_ladbrokescoral_tv_button_on_home_screen_above_next_races_modulemobiletablet(self):
        """
        DESCRIPTION: Desktop only:
        DESCRIPTION: Verify the Ladbrokes/Coral TV button on Home Screen above 'Next Races' module
        DESCRIPTION: Mobile/Tablet
        EXPECTED: 'Watch Ladbrokes/Coral TV' button is displayed above 'Next Races' module
        """
        pass

    def test_002_mobiletablet_tap_on_next_races_tab__verify_the_ladbrokescoral_tv_button_on_home_screen_above_next_races_module(self):
        """
        DESCRIPTION: Mobile/Tablet: tap on 'Next Races' tab ->
        DESCRIPTION: Verify the Ladbrokes/Coral TV button on Home Screen above 'Next Races' module
        EXPECTED: 'Watch Ladbrokes/Coral TV' button is displayed above 'Next Races' module
        """
        pass

    def test_003_open_greyhoundshorse_racing_landing_page(self):
        """
        DESCRIPTION: Open Greyhounds/Horse Racing landing page
        EXPECTED: * 'Watch Ladbrokes/Coral TV' button is displayed above the list of next races
        EXPECTED: * For logged in user with balance >0 or placed bet in last 24 hours:
        EXPECTED: Streaming window with play button available for customer to tap in order to start playing the always on streaming channel
        EXPECTED: * For logged out user:
        EXPECTED: placeholder within the Banner area is displayed that explains to customer that by logging in with positive balance or bet placed in last 24 hours they can view live content (text could be configured in CMS > Static Blocks )
        """
        pass

    def test_004_open_live_event_with_racing_tv_streamverify_the_ladbrokescoral_tv_button_is_above_the_selections(self):
        """
        DESCRIPTION: Open Live event with Racing TV stream
        DESCRIPTION: Verify the Ladbrokes/Coral TV button is above the Selections
        EXPECTED: 'Watch Ladbrokes/Coral TV' button is displayed above the Selections
        """
        pass

    def test_005_tap_on_meeting_selector(self):
        """
        DESCRIPTION: Tap on 'Meeting' Selector
        EXPECTED: List of Meetings is shown
        EXPECTED: 'Ladbrokes/Coral TV' link is shown on the top of the list
        """
        pass
