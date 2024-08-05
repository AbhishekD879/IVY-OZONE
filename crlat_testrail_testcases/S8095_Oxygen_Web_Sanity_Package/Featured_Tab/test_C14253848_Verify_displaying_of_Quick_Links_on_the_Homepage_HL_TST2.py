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
class Test_C14253848_Verify_displaying_of_Quick_Links_on_the_Homepage_HL_TST2(Common):
    """
    TR_ID: C14253848
    NAME: Verify displaying of  'Quick Links' on  the Homepage [HL/ TST2]
    DESCRIPTION: This test case verifies displaying of 'Quick Links' on the Homepage
    DESCRIPTION: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    DESCRIPTION: AUTOTEST [C57995347] on hl and tst2 endpoints
    PRECONDITIONS: 1. Load the application
    PRECONDITIONS: 2. Navigate to the Homepage -> 'Featured' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) Go to CMS -> Sports Pages -> Homepage and configure 1 active 'Quick link' for the Homepage
    PRECONDITIONS: 2) Set 'Active'/'Inactive' flag to 'Active' for the configured 'Quick link' for the Homepage to make it visible on the front end
    PRECONDITIONS: **Note:**
    PRECONDITIONS: To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    """
    keep_browser_open = True

    def test_001_verify_displaying_of_configured_quick_link_on_homepage(self):
        """
        DESCRIPTION: Verify displaying of configured 'Quick Link' on Homepage
        EXPECTED: * 'Quick links' container is displayed on the Homepage
        EXPECTED: * Configured 'Quick link' is displayed on the Homepage
        EXPECTED: * 'Quick link' is stretched to fit the width of the screen
        """
        pass

    def test_002_click_anywhere_on_the_configured_quick_linkverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the configured 'Quick link'.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS.
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass

    def test_003_go_to_cms___sports_pages___homepageconfigure_2nd_quick_link_for_homepage_with_a_long_name_long_enough_in_order_not_to_fit_the_remaining_width_of_the_screen(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> Homepage.
        DESCRIPTION: Configure 2nd Quick link for Homepage with a long name (Long enough in order not to fit the remaining width of the screen).
        EXPECTED: * 'Quick links' container is displayed on the Homepage
        EXPECTED: * Configured 'Quick links' are displayed on the Homepage
        EXPECTED: **[CORAL]**:
        EXPECTED: * 'Quick links' are displayed in the carousel as 2 separate blocks.
        EXPECTED: * 'Quick links' containers have a flexible width
        EXPECTED: * 2nd 'Quick link' is cut off. The only part that can fit the remaining width of the screen is shown
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * 'Quick links' are displayed as a fixed vertical list
        EXPECTED: * 'Quick links' are stretched to fit the width of the screen
        """
        pass

    def test_004_click_anywhere_on_the_newly_configured_quick_linkverify_redirection_to_the_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on the newly configured 'Quick link'.
        DESCRIPTION: Verify redirection to the specific page (URL) configured in CMS.
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass

    def test_005_go_to_cms___system_configuration___structure___sport_quick_links_module_and_set_the_max_number_of_quick_links_to_be_displayed_in_one_time_period_to_6(self):
        """
        DESCRIPTION: Go to CMS -> System Configuration -> Structure -> Sport Quick Links module and set the max number of quick links to be displayed in one Time period to 6
        EXPECTED: 
        """
        pass

    def test_006_go_to_cms___sports_pages___homepage_and_configure_more_quick_links_in_order_to_have_6_active_quick_links_for_the_current_time_period(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> Homepage and configure more 'Quick links' in order to have 6 active 'Quick links' for the current Time period
        EXPECTED: 
        """
        pass

    def test_007_go_to_the_application_homepageverify_that_6_configured_quick_links_are_displayed(self):
        """
        DESCRIPTION: Go to the application Homepage.
        DESCRIPTION: Verify that 6 configured 'Quick links' are displayed.
        EXPECTED: * 'Quick links' container is displayed on the Homepage
        EXPECTED: * Configured 'Quick links' are displayed on the Homepage
        EXPECTED: * 6 'Quick links' are displayed
        EXPECTED: **[CORAL]**:
        EXPECTED: * 'Quick links' are displayed as 6 separate blocks
        EXPECTED: * 'Quick links' containers have a flexible width
        EXPECTED: * 'Quick links' that don't fit the width of the screen are cut off
        EXPECTED: **[LADBROKES]**:
        EXPECTED: * 'Quick links' are displayed as a fixed vertical list
        EXPECTED: * 'Quick links' are stretched to fit the width of the screen
        """
        pass

    def test_008_click_anywhere_on_one_of_the_newly_configured_quick_linksverify_redirection_to_specific_specific_page_url_configured_in_cms(self):
        """
        DESCRIPTION: Click anywhere on one of the newly configured 'Quick links'.
        DESCRIPTION: Verify redirection to specific specific page (URL) configured in CMS.
        EXPECTED: * User is navigated to the specific page (URL) configured in CMS
        EXPECTED: * Page is opened within the application
        """
        pass

    def test_009_select_any_other_tab_on_the_homepage_eg_in_play_coupons_next_races_build_your_bet_etcverify_displaying_of_quick_links_on_other_tabs(self):
        """
        DESCRIPTION: Select any other tab on the Homepage (e.g. In-Play, Coupons, Next races, Build your bet, etc.)
        DESCRIPTION: Verify displaying of 'Quick links' on other tabs.
        EXPECTED: * Configured 'Quick links' are displayed only on the 'Featured' tab
        EXPECTED: * 'Quick links' container is NOT displayed on other 'Homepage' tabs
        EXPECTED: * Configured 'Quick links' are NOT displayed on other 'Homepage' tabs
        """
        pass

    def test_010_go_to_any_sports_page_eg_football_tennis_and_observe_the_quick_links_sectionverify_displaying_of_homepage_configured_quick_links_on_any_sports_landing_page(self):
        """
        DESCRIPTION: Go to any Sports page (e.g. Football, Tennis) and observe the 'Quick links' section.
        DESCRIPTION: Verify displaying of Homepage configured 'Quick links' on any Sports landing page.
        EXPECTED: * Configured 'Quick link' for Homepage is NOT displayed on other Sports pages
        EXPECTED: * Only 'Quick links' that are configured for Sports landing page are shown (if there are some)
        EXPECTED: * 'Quick links' container and links are NOT displayed If no 'Quick links' are configured for Sports pages.
        """
        pass

    def test_011_go_to_cms___sports_pages___homepage___quick_linksset_activeinactive_flag_for_the_configured_quick_link_for_homepage_to_inactive(self):
        """
        DESCRIPTION: Go to CMS -> Sports Pages -> Homepage -> Quick Links.
        DESCRIPTION: Set "Active"/"Inactive" flag for the configured 'Quick link' for Homepage to 'Inactive'
        EXPECTED: 
        """
        pass

    def test_012_go_to_the_appnavigate_to_the_featured_tab_on_the_homepageverify_that_quick_link_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to the app.
        DESCRIPTION: Navigate to the 'Featured' tab on the Homepage.
        DESCRIPTION: Verify that 'Quick link' is no longer displayed.
        EXPECTED: * 'Quick links' container is NOT displayed.
        EXPECTED: * 'Quick link' is no longer displayed.
        """
        pass
