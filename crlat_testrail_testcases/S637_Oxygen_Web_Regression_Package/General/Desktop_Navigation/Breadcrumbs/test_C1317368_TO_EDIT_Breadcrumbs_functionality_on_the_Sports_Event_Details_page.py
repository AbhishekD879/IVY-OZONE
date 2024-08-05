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
class Test_C1317368_TO_EDIT_Breadcrumbs_functionality_on_the_Sports_Event_Details_page(Common):
    """
    TR_ID: C1317368
    NAME: [TO EDIT] Breadcrumbs functionality on the Sports Event Details page
    DESCRIPTION: This test case verifies Breadcrumbs functionality on the Sports Event Details page.
    DESCRIPTION: Need to run the test case on Windows OS (IE, Edge, Chrome, Firefox) and Mac OS (Safari).
    PRECONDITIONS: 1. Oxygen app is loaded
    PRECONDITIONS: 2. Navigate to Sports Landing page -> 'Matches'->'Today' tab
    PRECONDITIONS: 3. Choose any event and navigate to Sports Event Details page
    """
    keep_browser_open = True

    def test_001_verify_breadcrumbs_displaying_on_the_sports_event_details_page(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying on the Sports Event Details page
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Event Details page: 'Home' > 'Sports Name' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass

    def test_002_click_on_sports_name_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Sports Name' hyperlink from the breadcrumbs
        EXPECTED: * Default Sports Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Default Sports Landing page: 'Home' > 'Sports Name' > 'Sub Tab Name' ('Matches' tab is selected by default when navigating to Sports Landing page)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_003_click_on_back_button_on_the_sports_header(self):
        """
        DESCRIPTION: Click on 'Back' button on the 'Sports' header
        EXPECTED: * Previously selected page is opened
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_004_click_on_home_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Home' hyperlink from the breadcrumbs
        EXPECTED: Homepage is loaded
        """
        pass

    def test_005_navigate_to_olympic_sports_event_details_page(self):
        """
        DESCRIPTION: Navigate to Olympic Sports Event Details page
        EXPECTED: Olympic Sports Event Details page is opened
        """
        pass

    def test_006_verify_breadcrumbs_displaying_on_the_sports_event_details_pageto_edit_when_user_is_on_edp_page_via_olympic_sport_navigation_then_olympics_is_not_present_in_the_breadcrumb___this_is_how_it_is_currently_on_coral_prod_so_this_step_probably_should_be_adjusted(self):
        """
        DESCRIPTION: Verify Breadcrumbs displaying on the Sports Event Details page
        DESCRIPTION: **[TO EDIT]** When user is on EDP page via Olympic sport navigation then 'Olympics' is not present in the breadcrumb - this is how it is currently on Coral prod so this step probably should be adjusted.
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Event Details page: 'Home' > 'Olympics' > 'Olympic Sports Name' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass

    def test_007_click_on_sports_name_hyperlink_from_the_breadcrumbsto_edit_see_comment_to_the_previous_step_and_this_one_also_needs_to_be_adjusted(self):
        """
        DESCRIPTION: Click on 'Sports Name' hyperlink from the breadcrumbs
        DESCRIPTION: **[TO EDIT]** See comment to the previous step and this one also needs to be adjusted
        EXPECTED: * Default Olympic Sports Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Default Olympic Sports Landing page: 'Home' > 'Olympics' > 'Sports Name' > 'Sub Tab Name' ('Matches' tab is selected by default when navigating to Olympic Sports Landing page as usual)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        """
        pass

    def test_008_repeat_steps_3_4(self):
        """
        DESCRIPTION: Repeat steps 3-4
        EXPECTED: 
        """
        pass
