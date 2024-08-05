import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.sports
@vtest
class Test_C1319985_Navigation_to_Big_Competition_page(Common):
    """
    TR_ID: C1319985
    NAME: Navigation to Big Competition page
    DESCRIPTION: This test case verifies navigation to Big Competition page via Sports Ribbon and A-Z menu
    PRECONDITIONS: * Competition should be created, set up and enabled in CMS -> Big Competition section
    PRECONDITIONS: * Competition item should be created, enabled and set up correctly in CMS (Menus -> Sport Categories)
    PRECONDITIONS: * 'Show in A-Z' and 'Show in Sports Ribbon' checkboxes are selected for Competition in Sport Categories
    PRECONDITIONS: * Category Id: 0 and SS Category Code: 0 should be set Competition in Sport Categories
    PRECONDITIONS: * To check response correctness open Dev Tools -> select Network tab -> XHR -> set api filter -> select initial-data/{mobile/tablet/desktop} request
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_in_network_tab_verify_initial_datamobiletabletdesktop_response(self):
        """
        DESCRIPTION: In Network tab verify initial-data/{mobile/tablet/desktop} response
        EXPECTED: 'showInHome=true' and 'showInAZ=true' are received for Competition in response within SportCategories structure
        """
        pass

    def test_003_verify_competition_item_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Verify Competition item on Module Selector ribbon
        EXPECTED: Competition item is present Module Selector ribbon
        """
        pass

    def test_004_tap_competition_item_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Tap Competition item on Module Selector ribbon
        EXPECTED: Competition landing page is loaded
        """
        pass

    def test_005_navigate_to_all_sports_page(self):
        """
        DESCRIPTION: Navigate to 'All Sports' page
        EXPECTED: Competition category is shown in 'A-Z' section
        """
        pass

    def test_006_select_competition_category(self):
        """
        DESCRIPTION: Select Competition category
        EXPECTED: Competition landing page is loaded
        """
        pass

    def test_007_verify_navigation_via_direct_url_httpsenvironmentcoralcoukbig_competitioncompetition_namewherecompetition_name___the_same_as_in_cms_within_big_competition_section(self):
        """
        DESCRIPTION: Verify navigation via direct URL: https://<environment>.coral.co.uk/#/big-competition/{competition_name}
        DESCRIPTION: where
        DESCRIPTION: competition_name - the same as in CMS within Big Competition section
        EXPECTED: Competition landing page is loaded
        """
        pass

    def test_008_go_to_cms___menus___sport_categories___competition_item_uncheck_show_in_a_z_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS -> Menus -> Sport Categories -> Competition item, uncheck 'Show in A-Z' checkbox and save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_009_reload_oxygen_app_and_go_to_all_sports_page(self):
        """
        DESCRIPTION: Reload Oxygen app and go to 'All Sports' page
        EXPECTED: * 'showInAZ=false' are received for Competition in response within SportCategories structure
        EXPECTED: * Competition category is NOT shown in 'A-Z' section
        """
        pass

    def test_010_go_to_cms___menus___sport_categories___competition_item_uncheck_show_in_sports_ribbon_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS -> Menus -> Sport Categories -> Competition item, uncheck 'Show in Sports Ribbon' checkbox and save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_011_reload_oxygen_app_and_check_module_selector_ribbon(self):
        """
        DESCRIPTION: Reload Oxygen app and check Module Selector ribbon
        EXPECTED: * 'showInHome=false' are received for Competition in response within SportCategories structure
        EXPECTED: * Competition item is NOT present Module Selector ribbon
        """
        pass

    def test_012_go_to_cms___big_competition___choose_used_competition__uncheck_active_checkbox_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS -> Big Competition -> choose used Competition,  uncheck 'Active' checkbox and save changes
        EXPECTED: Changes are saved
        """
        pass

    def test_013_reload_oxygen_app_and_verify_navigation_via_direct_url_httpsenvironmentcoralcoukbig_competitioncompetition_namewherecompetition_name___the_same_as_in_cms_within_big_competition_section(self):
        """
        DESCRIPTION: Reload Oxygen app and verify navigation via direct URL: https://<environment>.coral.co.uk/#/big-competition/{competition_name}
        DESCRIPTION: where
        DESCRIPTION: competition_name - the same as in CMS within Big Competition section
        EXPECTED: * Competition landing page is NOT loaded
        EXPECTED: * User is navigated to Homepage
        """
        pass
