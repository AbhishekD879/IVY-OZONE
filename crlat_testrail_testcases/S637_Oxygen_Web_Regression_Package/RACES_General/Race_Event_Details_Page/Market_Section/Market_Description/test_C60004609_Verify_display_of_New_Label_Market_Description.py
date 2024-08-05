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
class Test_C60004609_Verify_display_of_New_Label_Market_Description(Common):
    """
    TR_ID: C60004609
    NAME: Verify display of New Label- Market Description
    DESCRIPTION: Verify that New Label is displayed below the Market header along with the description when enabled in CMS
    PRECONDITIONS: 1. Horse racing & Greyhound racing events & markets should be available.
    PRECONDITIONS: 2.Market Descriptions should be configured and enabled in CMS
    """
    keep_browser_open = True

    def test_001_login_to_cms(self):
        """
        DESCRIPTION: Login to CMS
        EXPECTED: User should be logged into CMS
        """
        pass

    def test_002_navigate_to_system_configuration__structure_and_enable_new_label(self):
        """
        DESCRIPTION: Navigate to System Configuration > Structure and enable New Label
        EXPECTED: User should be able to save the changes in CMS
        """
        pass

    def test_003_launch_coral_ladbrokes_urlfor_mobile_launch_the_app(self):
        """
        DESCRIPTION: Launch Coral /Ladbrokes URL
        DESCRIPTION: For Mobile: Launch the app
        EXPECTED: URL should be launched
        EXPECTED: For Mobile: App should be opened
        """
        pass

    def test_004_navigate_to_sports_menuhorse_racingfrom_a_z_all_sports_horse_racing(self):
        """
        DESCRIPTION: Navigate to Sports Menu(Horse Racing)/From A-Z all Sports->Horse Racing
        EXPECTED: User should be navigated Horse racing landing page
        """
        pass

    def test_005_click_on_any_race_which_has_the_market_template_available_for_which_description_is_added_and_new_label_is_configured_in_cms(self):
        """
        DESCRIPTION: Click on any race which has the Market template available for which description is added and New label is configured in CMS
        EXPECTED: User should be navigated to EDP page
        """
        pass

    def test_006_validate_the_description_and_new_label_displayedindexphpattachmentsget120830386indexphpattachmentsget120830387(self):
        """
        DESCRIPTION: Validate the description and New Label displayed![](index.php?/attachments/get/120830386)
        DESCRIPTION: ![](index.php?/attachments/get/120830387)
        EXPECTED: 1: User should be able to view the description below the Market Header
        EXPECTED: 2: New Label should be displayed and CSS should be as mentioned in Zeplin
        """
        pass

    def test_007_navigate_to_grey_hound_racing_and_repeat_5__6_steps(self):
        """
        DESCRIPTION: Navigate to Grey Hound racing and repeat 5 & 6 steps
        EXPECTED: 
        """
        pass

    def test_008_now_disable_the_new_label_configuration_in_cms_and_repeat_4567_stepsvalidate_that_new_label_is_not_displayed(self):
        """
        DESCRIPTION: Now disable the New label configuration in CMS and Repeat 4,5,6,7 Steps
        DESCRIPTION: Validate that New Label is not displayed
        EXPECTED: New Label should not be displayed when disabled in CMS
        """
        pass
