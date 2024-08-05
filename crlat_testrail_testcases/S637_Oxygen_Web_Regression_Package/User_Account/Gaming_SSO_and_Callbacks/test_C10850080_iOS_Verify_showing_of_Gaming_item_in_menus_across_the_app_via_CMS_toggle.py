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
class Test_C10850080_iOS_Verify_showing_of_Gaming_item_in_menus_across_the_app_via_CMS_toggle(Common):
    """
    TR_ID: C10850080
    NAME: [iOS] Verify showing of Gaming item in menus across the app via CMS toggle
    DESCRIPTION: This test case verifies the showing of Gaming item in menus across the app (via CMS toggle)
    DESCRIPTION: Platform:
    DESCRIPTION: * iOS
    DESCRIPTION: **NOTE!** Changes applicable to app versions higher than 5.0.0
    PRECONDITIONS: * CMS toggle: System Configuration > GamingEnabled is ENABLED
    PRECONDITIONS: * Load Oxygen app
    PRECONDITIONS: * User is Logged Out
    PRECONDITIONS: **Note:**
    PRECONDITIONS: Gaming item in all menus should be created with the following data:
    PRECONDITIONS: Title: Gaming
    PRECONDITIONS: Target Uri: https://gaming.coral.co.uk/
    PRECONDITIONS: Tick 'Active' checkbox
    """
    keep_browser_open = True

    def test_001_navigate_to_sports_menu_ribbon(self):
        """
        DESCRIPTION: Navigate to Sports Menu Ribbon
        EXPECTED: Gaming is shown on Sports Menu Ribbon
        """
        pass

    def test_002_repeat_step_1_for_footer_menu_when_the_user_navigated_to_another_page_than_homepage_in_the_app(self):
        """
        DESCRIPTION: Repeat step 1 for Footer Menu when the user navigated to another page than Homepage in the app
        EXPECTED: 
        """
        pass

    def test_003_repeat_step_1_for_a_z_page(self):
        """
        DESCRIPTION: Repeat step 1 for A-Z page
        EXPECTED: 
        """
        pass

    def test_004_repeat_step_1_for_a_z_page__top_sports_section(self):
        """
        DESCRIPTION: Repeat step 1 for A-Z page > Top Sports section
        EXPECTED: 
        """
        pass

    def test_005_repeat_step_1_for_a_z_page__top_games_section(self):
        """
        DESCRIPTION: Repeat step 1 for A-Z page > Top Games section
        EXPECTED: 
        """
        pass

    def test_006_repeat_step_1_for_logged_in_user(self):
        """
        DESCRIPTION: Repeat step 1 for Logged In user
        EXPECTED: 
        """
        pass
