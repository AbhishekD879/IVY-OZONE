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
class Test_C59535361_Verify_the_display_of_Ladbrokes_Legends_panel_CMS_configured(Common):
    """
    TR_ID: C59535361
    NAME: Verify the display of Ladbrokes Legends panel-CMS configured
    DESCRIPTION: Verify that meetings in Ladbrokes Legends panel are positioned as configured in CMS
    PRECONDITIONS: 1: Ladbrokes Legends should have meetings displayed in FE
    PRECONDITIONS: 2: Admin access for CMS
    """
    keep_browser_open = True

    def test_001_launch_ladbrokes_coral_urlfor_mobile_launch_app(self):
        """
        DESCRIPTION: Launch Ladbrokes/ Coral URL
        DESCRIPTION: For Mobile: Launch App
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_002_click_on_horse_racing_from_sports_menufor_mobile__click_on_horse_racing_from_sports_ribbon(self):
        """
        DESCRIPTION: Click on Horse racing from Sports menu
        DESCRIPTION: For Mobile : Click on Horse racing from sports ribbon
        EXPECTED: User should be navigated to Horse racing Landing page
        """
        pass

    def test_003_verify_the_display_of_ladbrokes_legends(self):
        """
        DESCRIPTION: Verify the display of Ladbrokes Legends
        EXPECTED: 
        """
        pass

    def test_004_log_in_to_cms_and_change_the_order_for_ladbrokes_legends(self):
        """
        DESCRIPTION: Log in to CMS and change the order for Ladbrokes Legends
        EXPECTED: 
        """
        pass

    def test_005_verify_in_fe_the_order_displayed_is_as_configured_in_cms(self):
        """
        DESCRIPTION: Verify in FE the order displayed is as configured in CMS
        EXPECTED: User should be able to see the display order as per CMS configuration
        """
        pass
