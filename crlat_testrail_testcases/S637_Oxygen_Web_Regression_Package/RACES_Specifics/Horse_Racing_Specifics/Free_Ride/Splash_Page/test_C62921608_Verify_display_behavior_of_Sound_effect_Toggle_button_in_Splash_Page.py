import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C62921608_Verify_display_behavior_of_Sound_effect_Toggle_button_in_Splash_Page(Common):
    """
    TR_ID: C62921608
    NAME: Verify display & behavior of  Sound effect Toggle button in Splash Page
    DESCRIPTION: This test case verifies display & behavior of  Sound effect Toggle button in Splash Page
    PRECONDITIONS: 1: User should have admin access to CMS
    PRECONDITIONS: 2: Free Ride menu should be configured in CMS
    PRECONDITIONS: ***How to Configure Menu Item***
    PRECONDITIONS: Edit CMS Menu --&gt; Create Menu Item
    PRECONDITIONS: Item Label: Free Ride
    PRECONDITIONS: Path: /Free Ride
    PRECONDITIONS: Add sub Menu
    PRECONDITIONS: Item Label: Splash Page
    PRECONDITIONS: Path: /Splash Page
    """
    keep_browser_open = True

    def test_001_login_to_ladbrokes_application_with_eligible_customer_for_free_ride(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer for Free Ride
        EXPECTED: User should be able to login successfully
        """
        pass

    def test_002_verify_display_of_launch_free_ride_banner_in_homepage(self):
        """
        DESCRIPTION: Verify display of 'Launch Free Ride Banner' in Homepage
        EXPECTED: 'Launch Free Ride Banner' should be displayed in Homepage
        """
        pass

    def test_003_click_onlaunch_free_ride_banner(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner'
        EXPECTED: Splash Page should be displayed
        """
        pass

    def test_004_verify_display_ofsound_effect_toggle_button(self):
        """
        DESCRIPTION: Verify display of Sound effect Toggle button
        EXPECTED: Sound effect Toggle button should be displayed as per Zeplin
        """
        pass

    def test_005_verify_onoff_behavior(self):
        """
        DESCRIPTION: Verify ON/OFF behavior
        EXPECTED: User should be able to Turn on and Off the Sound Toggle Button
        """
        pass
