import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.promotions_banners_offers
@vtest
class Test_C363727_To_edit_Offers_reload(Common):
    """
    TR_ID: C363727
    NAME: [To edit] Offers reload
    DESCRIPTION: Test case should be updated according to comment in BMA-48186
    DESCRIPTION: This test case verifies reload of 'Offers' widget content (offers modules and offers) after losing and restoring the connection to the Internet or coming back from sleep mode/background
    PRECONDITIONS: * 'Offers' widget is configured to be shown in CMS->Widgets
    PRECONDITIONS: * At least one Offer module is created in CMS->Offers->Offer Modules
    PRECONDITIONS: * Few offers are created in CMS->Offers->Offers
    PRECONDITIONS: * At least one Offer is added to created Offer module
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: To test sleep mode:
    PRECONDITIONS: * lock mobile/tablet for few minutes (depends on device)
    PRECONDITIONS: * on laptop/workstation click Power -> Sleep
    """
    keep_browser_open = True

    def test_001_load_oxygen_application_on_tablet(self):
        """
        DESCRIPTION: Load Oxygen application on tablet
        EXPECTED: 
        """
        pass

    def test_002_move_device_to_sleep_mode(self):
        """
        DESCRIPTION: Move device to sleep mode
        EXPECTED: 
        """
        pass

    def test_003_in_cms_make_changes_visible_on_oxygen_front_end_eg_add_one_more_offer_to_offer_module(self):
        """
        DESCRIPTION: In CMS make changes visible on Oxygen front end (e.g. add one more offer to offer module)
        EXPECTED: 
        """
        pass

    def test_004_unlock_deviceverify_console_and_network_tabs(self):
        """
        DESCRIPTION: Unlock device
        DESCRIPTION: Verify Console and Network tabs
        EXPECTED: * 'reload components' in displayed Console
        EXPECTED: * 'tablet' request is sent in Network tab
        """
        pass

    def test_005_verify_offer_module(self):
        """
        DESCRIPTION: Verify offer module
        EXPECTED: Сhange from step #3 is displayed on Oxygen front end (e.g. relevant number of navigation dots (increased to 1) are shown in offer module)
        """
        pass

    def test_006_move_app_to_background_for_few_minutes(self):
        """
        DESCRIPTION: Move app to background for few minutes
        EXPECTED: 
        """
        pass

    def test_007_in_cms_make_changes_visible_on_oxygen_frontend_eg_create_one_new_offer_module_and_offer_to_the_module(self):
        """
        DESCRIPTION: In CMS make changes visible on Oxygen frontend (e.g. create one new offer module and offer to the module)
        EXPECTED: 
        """
        pass

    def test_008_move_app_to_foregroundverify_console_and_network_tabs(self):
        """
        DESCRIPTION: Move app to foreground
        DESCRIPTION: Verify console and Network tabs
        EXPECTED: * 'reload components' in console
        EXPECTED: * 'tablet' request is sent in Network tab
        """
        pass

    def test_009_verify_offers_widget_content(self):
        """
        DESCRIPTION: Verify 'Offers' widget content
        EXPECTED: Сhange from step #7 is displayed on Oxygen front end (e.g. new module with offer is displayed)
        """
        pass

    def test_010_make_device_lose_internet_connection_and_wait_few_minutes(self):
        """
        DESCRIPTION: Make device lose internet connection and wait few minutes
        EXPECTED: * Pop up about loosing internet appears
        """
        pass

    def test_011_in_cms_make_changes_visible_on_oxygen_frontend_eg_disable_offers_module_created_in_step_6(self):
        """
        DESCRIPTION: In CMS make changes visible on Oxygen frontend (e.g. disable offers module created in step #6)
        EXPECTED: 
        """
        pass

    def test_012_close_pop_up(self):
        """
        DESCRIPTION: Close pop up
        EXPECTED: 
        """
        pass

    def test_013_restore_internet_connection_it_may_take_some_timeverify_console_and_network_tabs(self):
        """
        DESCRIPTION: Restore internet connection (it may take some time)
        DESCRIPTION: Verify console and Network tabs
        EXPECTED: * 'reload components' in console
        EXPECTED: * 'tablet' request is sent in Network tab
        """
        pass

    def test_014_verify_offers_widget_content(self):
        """
        DESCRIPTION: Verify 'Offers' widget content
        EXPECTED: Сhange from step #11 is displayed on Oxygen front end (e.g. module created in step #6 is not displayed)
        """
        pass

    def test_015_load_oxygen_application_on_desktop(self):
        """
        DESCRIPTION: Load Oxygen application on desktop
        EXPECTED: 
        """
        pass

    def test_016_repeat_steps_2_5_and_10_14(self):
        """
        DESCRIPTION: Repeat steps #2-5 and #10-14
        EXPECTED: Results are the same (except 'desktop' request is sent after 'reload components')
        """
        pass
