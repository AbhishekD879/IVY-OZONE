import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.navigation
@vtest
class Test_C2089464_Super_button_Updating(Common):
    """
    TR_ID: C2089464
    NAME: Super button Updating
    DESCRIPTION: This test case verifies Mobile Super button Updating
    PRECONDITIONS: * Mobile Super button can be added and configured in CMS:
    PRECONDITIONS: https://{domain}/sports-pages/homepage
    PRECONDITIONS: where domain may be
    PRECONDITIONS: coral-cms-dev1.symphony-solutions.eu - Local env
    PRECONDITIONS: coral-cms-dev0.symphony-solutions.eu - Develop
    PRECONDITIONS: * To check data open DevTools -> select 'Network' tab -> 'XMR' sorting type -> set 'cms' filter
    """
    keep_browser_open = True

    def test_001_load_cms(self):
        """
        DESCRIPTION: Load CMS
        EXPECTED: CMS is opened
        """
        pass

    def test_002_go_to_sports_pages_gt_super_button_gt_open_existing_super_button(self):
        """
        DESCRIPTION: Go to Sports Pages &gt; Super Button &gt; open existing Super button
        EXPECTED: Super button details page is opened
        """
        pass

    def test_003_change_titleoption_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Change
        DESCRIPTION: * title
        DESCRIPTION: option for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_004_load_oxygen_app_go_to_the_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up
        EXPECTED: * GET {domain}cms/api/{brand}/navigation-points request is sent to get new data from CMS
        EXPECTED: * Title of Super button is updated according to changes.
        """
        pass

    def test_005_change_destination_urloption_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Change
        DESCRIPTION: * destination URL
        DESCRIPTION: option for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_006_load_oxygen_app_go_to_the_page_where_super_button_is_set_up_and_tap_it(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up and tap it
        EXPECTED: * GET {domain}cms/api/{brand}/navigation-points request is sent to get new data from CMS
        EXPECTED: * Destination URL of Super button is updated according to changes without page refresh
        EXPECTED: * User is navigated to new destination URL page
        """
        pass

    def test_007_load_cms_change_short_descriptionoption_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change
        DESCRIPTION: * short description
        DESCRIPTION: option for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_008_load_oxygen_app_go_to_the_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up
        EXPECTED: * GET {domain}cms/api/{brand}/navigation-points request is sent to get new data from CMS
        EXPECTED: * Short Description of Super button is updated according to changes.
        """
        pass

    def test_009_load_cms_change_validity_period_startendoptions_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change
        DESCRIPTION: * validity period start/end
        DESCRIPTION: options for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_010_load_oxygen_app_go_to_the_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up
        EXPECTED: * GET {domain}cms/api/{brand}/navigation-points request is sent to get new data from CMS
        EXPECTED: * Validity period start/end of Super button is updated according to changes.
        """
        pass

    def test_011_load_cms_change_activeinactiveoption_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change
        DESCRIPTION: * active/inactive
        DESCRIPTION: option for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_012_load_oxygen_app_go_to_the_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: Load Oxygen app, go to the page where Super button is set up
        EXPECTED: * GET {domain}cms/api/{brand}/navigation-points request is sent to get new data from CMS
        EXPECTED: * Data for Supoer button is NOT received from CMS if 'inactive' option is set up
        """
        pass

    def test_013_load_cms_change_show_on_home_tabsoption_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change
        DESCRIPTION: * Show on Home Tabs
        DESCRIPTION: option for existing Super button and save changes
        EXPECTED: 
        """
        pass

    def test_014_in_oxygen_navigate_to_home_tabs_where_super_button_is_set_up(self):
        """
        DESCRIPTION: In Oxygen, navigate to Home Tab(s) where Super button is set up
        EXPECTED: * GET {domain}cms/api/{brand}/navigation-points request is sent
        EXPECTED: * Super button is displayed on Home Tab(s)
        """
        pass

    def test_015_load_cms_change_show_on_sportoption_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change
        DESCRIPTION: * Show on Sport
        DESCRIPTION: option for existing Super button and save changes
        EXPECTED: Changes are saved successfully
        """
        pass

    def test_016_in_oxygen_navigate_to_ltsportgt_ltracegt_landing_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: In Oxygen, navigate to &lt;Sport&gt;/ &lt;Race&gt; landing page where Super button is set up
        EXPECTED: * GET {domain}/cms/api/{brand}/navigation-points request is sent
        EXPECTED: * Super button is displayed on &lt;Sport&gt;/ &lt;Race&gt; landing page
        """
        pass

    def test_017_load_cms_change_show_on_big_competitionsoption_for_existing_super_button_and_save_changes(self):
        """
        DESCRIPTION: Load CMS, change
        DESCRIPTION: * Show on Big Competitions
        DESCRIPTION: option for existing Super button and save changes
        EXPECTED: 
        """
        pass

    def test_018_in_oxygen_navigate_to_big_competition_page_where_super_button_is_set_up(self):
        """
        DESCRIPTION: In Oxygen, navigate to Big Competition page where Super button is set up
        EXPECTED: * GET {domain}/cms/api/{brand}/navigation-points request is sent
        EXPECTED: * Super button is displayed on Big Competition landing page
        """
        pass
