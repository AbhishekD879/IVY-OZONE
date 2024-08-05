import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C2389906_Verify_Breadcrumbs_functionality_across_the_application(Common):
    """
    TR_ID: C2389906
    NAME: Verify Breadcrumbs functionality across the application
    DESCRIPTION: This test case verifies Breadcrumbs functionality across the application
    DESCRIPTION: partly covered in AUTOTESTS https://ladbrokescoral.testrail.com/index.php?/suites/view/3779&group_by=cases:section_id&group_id=735049&group_order=asc and [C9698302]
    PRECONDITIONS: Open Oxygen app
    """
    keep_browser_open = True

    def test_001_navigate_to_sports_landing_page_and_verify_breadcrumbs_displaying(self):
        """
        DESCRIPTION: Navigate to Sports Landing page and verify Breadcrumbs displaying
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Landing page: 'Home' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass

    def test_002_choose_some_tab_from_sports_sub_tab_menu(self):
        """
        DESCRIPTION: Choose some tab from Sports Sub Tab menu
        EXPECTED: 'Sub Tab Name' is changed in breadcrumbs trail according to the selected tab (e.g. 'Outrights')
        """
        pass

    def test_003_navigate_to_sports_event_details_page_and_verify_breadcrumbs_displaying(self):
        """
        DESCRIPTION: Navigate to Sports Event Details page and verify Breadcrumbs displaying
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports * Event Details page: 'Home' > 'Sports Name' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass

    def test_004_click_on_sports_name_hyperlink_from_the_breadcrumbs(self):
        """
        DESCRIPTION: Click on 'Sports Name' hyperlink from the breadcrumbs
        EXPECTED: * Default Sports Landing page is loaded
        EXPECTED: * Breadcrumbs are displayed in the next format at the Default * Sports Landing page: 'Home' > 'Sports Name' > 'Sub Tab * * Name' ('Matches' tab is selected by default when navigating to Sports Landing page)
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        pass

    def test_005_click_on_back_button_on_the_sports_header(self):
        """
        DESCRIPTION: Click on 'Back' button on the 'Sports' header
        EXPECTED: * Previously selected page is opened
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        pass

    def test_006_repeat_steps_1_5_for_races_and_verify_breadcrumbs_functionality(self):
        """
        DESCRIPTION: Repeat steps 1-5 for Races and verify Breadcrumbs functionality
        EXPECTED: 
        """
        pass

    def test_007_navigate_to_promotions_page_and_verify_breadcrumbs_displaying_at_the_promotions_page(self):
        """
        DESCRIPTION: Navigate to Promotions page and verify Breadcrumbs displaying at the 'Promotions' page
        EXPECTED: * Breadcrumbs are located below the 'Promotions' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the 'Promotions' page: 'Home' > 'Promotions'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        pass

    def test_008_repeat_the_same_for_player_betsyourcallvirtualslotto_pages(self):
        """
        DESCRIPTION: Repeat the same for 'Player Bets'/'YourCall'/'Virtuals'/'Lotto' pages
        EXPECTED: 
        """
        pass

    def test_009_navigate_to_olympics_landing_page_and_verify_breadcrumbs_functionality(self):
        """
        DESCRIPTION: Navigate to Olympics Landing page and verify Breadcrumbs functionality
        EXPECTED: * Breadcrumbs are located below the 'Olympics' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Olympics Landing page: 'Home' > 'Olympics'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        pass

    def test_010_choose_some_sport_from_the_list_and_verify_breadcrumbs_displaying_at_the_sports_olympics_landing_page(self):
        """
        DESCRIPTION: Choose some Sport from the list and verify Breadcrumbs displaying at the Sports Olympics Landing page
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Sports Olympics Landing page: 'Home' > 'Olympics' > 'Sports Name' > 'Sub Tab Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to the selected page
        """
        pass

    def test_011_navigate_to_olympic_sports_event_details_page_and_verify_breadcrumbs_trail(self):
        """
        DESCRIPTION: Navigate to Olympic Sports Event Details page and verify Breadcrumbs trail
        EXPECTED: * Breadcrumbs are located below the 'Sports' header
        EXPECTED: * Breadcrumbs are displayed in the next format at the Olympic Sports Event Details page: 'Home' > 'Olympics' > 'Olympic Sports Name' > 'Event Name'
        EXPECTED: * Appropriate hyperlink from breadcrumbs is highlighted according to selected page
        EXPECTED: * Items from Breadcrumbs trail are underlined when hovering the mouse over it
        """
        pass
