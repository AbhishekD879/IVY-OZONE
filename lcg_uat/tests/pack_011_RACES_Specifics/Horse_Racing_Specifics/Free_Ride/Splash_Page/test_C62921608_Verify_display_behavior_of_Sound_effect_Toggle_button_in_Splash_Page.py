import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
from voltron.environments import constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.horseracing
@pytest.mark.racing
@pytest.mark.races
@pytest.mark.free_ride
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

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User should have admin access to CMS
        PRECONDITIONS: Free Ride menu should be configured in CMS
        """
        self.__class__.username = tests.settings.default_username
        offer_id = self.ob_config.backend.ob.freeride.general_offer.offer_id
        self.ob_config.grant_freeride(offer_id=offer_id, username=self.username)
        self.update_spotlight_events_price(class_id=223)
        self.cms_config.check_update_and_create_freeride_campaign()

    def test_001_login_to_ladbrokes_application_with_eligible_customer_for_free_ride(self):
        """
        DESCRIPTION: Login to Ladbrokes Application with eligible customer for Free Ride
        EXPECTED: User should be able to login successfully
        """
        self.site.login(username=self.username)
        self.site.wait_content_state("Homepage")

    def test_002_verify_display_of_launch_free_ride_banner_in_homepage(self):
        """
        DESCRIPTION: Verify display of 'Launch Free Ride Banner' in Homepage
        EXPECTED: 'Launch Free Ride Banner' should be displayed in Homepage
        """
        self.assertTrue(self.site.home.free_ride_banner(), msg='"Launch Free Ride Banner" is not displayed')

    def test_003_click_onlaunch_free_ride_banner(self):
        """
        DESCRIPTION: Click on 'Launch Free Ride Banner'
        EXPECTED: Splash Page should be displayed
        """
        self.site.home.free_ride_banner().click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_FREE_RIDE, timeout=10,
                                           verify_name=False)
        self.assertTrue(dialog.sound_switch.is_displayed(), msg='"Sound effect Toggle" button is not displayed')
        dialog.sound_switch.click()
        self.assertTrue(dialog.sound_switch.is_displayed(), msg='"Sound effect Toggle" button is not displayed')
        dialog.sound_switch.click()
        self.assertTrue(dialog.sound_switch.is_displayed(), msg='"Sound effect Toggle" button is not displayed')

    def test_004_verify_display_ofsound_effect_toggle_button(self):
        """
        DESCRIPTION: Verify display of Sound effect Toggle button
        EXPECTED: Sound effect Toggle button should be displayed as per Zeplin
        """
        # covered in the step test_003

    def test_005_verify_onoff_behavior(self):
        """
        DESCRIPTION: Verify ON/OFF behavior
        EXPECTED: User should be able to Turn on and Off the Sound Toggle Button
        """
        # covered in the step test_003
