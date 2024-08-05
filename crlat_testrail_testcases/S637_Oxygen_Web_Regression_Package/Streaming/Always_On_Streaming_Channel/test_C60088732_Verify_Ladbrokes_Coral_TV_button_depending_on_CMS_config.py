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
class Test_C60088732_Verify_Ladbrokes_Coral_TV_button_depending_on_CMS_config(Common):
    """
    TR_ID: C60088732
    NAME: Verify Ladbrokes/Coral TV button depending on CMS config
    DESCRIPTION: This test case verifies that Ladbrokes/Coral TV button can be turned ON/OFF in CMS for Horse Racing and Greyhounds
    DESCRIPTION: **Note:** in scope of the BMA-56229 Epic this feature is available only for Greyhounds
    PRECONDITIONS: List of CMS endpoints: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: In CMS: System Configuration > Structure > Racing TV-> Set linkShownForSportIds = true for Greyhounds/Horse Racing, enabling each sport by sport id:
    PRECONDITIONS: 19 for Greyhounds
    PRECONDITIONS: 21 for Horse Racing
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

    def test_003__open_greyhoundshorse_racing_landing_page_coralladbrokes_go_to_next_races_tab_ladbrokes(self):
        """
        DESCRIPTION: * Open Greyhounds/Horse Racing landing page (Coral/Ladbrokes)
        DESCRIPTION: * Go to 'Next Races' tab (Ladbrokes)
        EXPECTED: 'Watch Ladbrokes/Coral TV' button is displayed above the list of next races
        """
        pass

    def test_004_open_live_event_with_racing_tv_streamverify_the_ladbrokescoral_tv_button_is_above_the_selections(self):
        """
        DESCRIPTION: Open Live event with Racing TV stream
        DESCRIPTION: Verify the Ladbrokes/Coral TV button is above the Selections
        EXPECTED: 'Watch Ladbrokes/Coral TV' button is displayed above the Selections
        """
        pass
