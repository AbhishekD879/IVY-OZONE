import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.homepage_featured
@vtest
class Test_C2552882_Verify_adding_removing_Quick_links_on_any_Sports_Landing_page(Common):
    """
    TR_ID: C2552882
    NAME: Verify adding/removing Quick links on any Sports Landing page
    DESCRIPTION: AUTOTEST: [C9489507]
    DESCRIPTION: This test case verifies adding of Quick links to Homepage and All Sports Landing pages
    PRECONDITIONS: 1. <Sport name1>, <Sport name2> - Select any two Sport types(e.g. Football and Tennis)
    PRECONDITIONS: 2. There should be no active Quick links enabled for <Sport name1>, <Sport name2> landing pages.
    PRECONDITIONS: 3. Go to Oxygen app and navigate to <Sport name1> landing page.
    PRECONDITIONS: [Tab name]- This tab is selected by default aftec accessing Sport Landing Page. Name of the tab depends on the selected Sport. Only Sports with following tabs should contain Quick links module: "Matches", "Events", "Fights"
    PRECONDITIONS: <Sport name1>,<Sport name2> - any sport with following tabs: "Matches", "Events", "Fights" available in oxygen application
    PRECONDITIONS: Ladbrokes Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    PRECONDITIONS: Coral design (now its matching Ladbrokes, i.e. quick links are stacked in a vertical list): https://jira.egalacoral.com/browse/BMA-52016
    PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
    PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
    PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_quick_links_on_sport_name1_landing_page(self):
        """
        DESCRIPTION: Verify displaying of Quick links on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is not displayed on <Sport name1> landing page
        EXPECTED: * No Quick Links are displayed on <Sport name1> landing page
        """
        pass

    def test_002_go_to_cms___sport_pages_sport_name1___quick_links_and_configure_one_quick_link_for_sport_name1_landing_page(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name1> -> Quick Links and configure one Quick Link for <Sport name1> landing page.
        EXPECTED: 
        """
        pass

    def test_003_go_to_oxygen_application_and_navigate_to_sport_name1_landing_pageverify_that_configured_quick_link_is_displayed_on_sport_name1_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen application and navigate to <Sport name1> landing page.
        DESCRIPTION: Verify that configured Quick link is displayed on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name1> landing page
        EXPECTED: * Configured Quick link is displayed on [Tab name] of <Sport name1> landing page
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        pass

    def test_004_go_to_cms___sport_pages_sport_name2___quick_links_and_create_new_quick_link_for_sport_name2_landing_page(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name2> -> Quick Links and create new Quick link for <Sport name2> landing page.
        EXPECTED: 
        """
        pass

    def test_005_go_to_sport_name2_landing_page_in_oxygen_applicationverify_that_quick_link_configured_for_sport_name1_landing_page_is_not_displayed_on_sport_name2_landing_page(self):
        """
        DESCRIPTION: Go to <Sport name2> landing page in oxygen application.
        DESCRIPTION: Verify that quick link configured for <Sport name1> landing page is not displayed on <Sport name2> landing page.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Configured Quick link for <Sport name2> landing page is displayed on [Tab name] of <Sport name2> landing page.
        EXPECTED: * Quick links configured for <Sport name1> landing page is not displayed on [Tab name] of <Sport name1> landing page.
        """
        pass

    def test_006_go_to_home_pageverify_that_quick_links_configured_for_sport_name2_and_sport_name1_landing_pages_are_not_displayed_on_homepage(self):
        """
        DESCRIPTION: Go to Home page.
        DESCRIPTION: Verify that quick links configured for <Sport name2> and <Sport name1> landing pages are not displayed on Homepage.
        EXPECTED: * Quick links configured for <Sport name2> and <Sport name1> landing pages  are not displayed on Homepage.
        """
        pass

    def test_007_go_to_cms___sport_pages_sport_name1___quick_links_and_set_active_inactive_flag_in_configured_quick_link_to_inactive(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name1> -> Quick Links and set "Active/ Inactive" flag in configured quick link to 'Inactive'.
        EXPECTED: 
        """
        pass

    def test_008_go_to_oxygen_app_and_navigate_to_sport_name1_landing_pageverify_that_quick_link_is_no_longer_displayed_on_sport_name1_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to <Sport name1> landing page.
        DESCRIPTION: Verify that Quick link is no longer displayed on <Sport name1> landing page.
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is not displayed on [Tab name] of <Sport name1> landing page
        EXPECTED: * Quick link is no longer displayed on on [Tab name] of <Sport name1> landing page
        """
        pass

    def test_009_go_to_cms___sport_pages_sport_name1___quick_links_and_set_active_inactive_flag_in_configured_quick_link_for_homepage_to_active(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name1> -> Quick Links and set "Active/ Inactive" flag in configured quick link for Homepage to 'Active'.
        EXPECTED: 
        """
        pass

    def test_010_go_to_oxygen_app_and_navigate_to_sport_name1_landing_pageverify_that_quick_link_is_displayed_on_sport_name1_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to <Sport name1> landing page.
        DESCRIPTION: Verify that Quick link is displayed on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is displayed on [Tab name] of <Sport name1> landing page
        EXPECTED: * Configured Quick link is displayed on [Tab name] of <Sport name1> landing page
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        pass

    def test_011_go_to_cms___sport_pages_sport_name1___quick_links_and_delete_previously_created_quick_link_for_sport_name1_landing_page(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages-><Sport name1> -> Quick Links and delete previously created Quick link for <Sport name1> landing page.
        EXPECTED: 
        """
        pass

    def test_012_go_to_oxygen_app_and_navigate_to_sport_name1_landing_pageverify_that_quick_link_is_no_longer_displayed_on_sport_name1_landing_page(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to <Sport name1> landing page.
        DESCRIPTION: Verify that Quick link is no longer displayed on <Sport name1> landing page
        EXPECTED: * [Tab name] is selected by default
        EXPECTED: * Quick links container is not displayed on [Tab name] of <Sport name1> landing page
        EXPECTED: * Quick link is no longer displayed on [Tab name] of <Sport name1> landing page
        """
        pass
