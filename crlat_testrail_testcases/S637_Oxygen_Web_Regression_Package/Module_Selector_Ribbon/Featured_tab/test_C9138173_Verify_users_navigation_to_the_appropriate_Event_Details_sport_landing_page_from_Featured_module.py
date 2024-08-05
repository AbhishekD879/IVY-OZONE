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
class Test_C9138173_Verify_users_navigation_to_the_appropriate_Event_Details_sport_landing_page_from_Featured_module(Common):
    """
    TR_ID: C9138173
    NAME: Verify user's navigation to the appropriate Event Details/sport landing page from Featured module
    DESCRIPTION: This test case verifies user's navigation to the appropriate Event Details/sport landing page from Featured module
    PRECONDITIONS: Featured modules by Type id/Race type id are created and displayed in application
    PRECONDITIONS: Featured tab is opened in app
    PRECONDITIONS: Note: Virtual HR/GH events are supported in featured module created by RaceTypeID so this case should check them as well.
    """
    keep_browser_open = True

    def test_001_select_module_created_by_sport_type_idtap_link_for_selected_event_with_number_of_markets_available(self):
        """
        DESCRIPTION: Select module created by Sport type id.
        DESCRIPTION: Tap link for selected event with number of markets available
        EXPECTED: user is navigated to the selected event details page
        """
        pass

    def test_002_select_module_created_by_race_type_iddesktop_tap_view_full_race_card_link_under_the_selected_race_eventmobile_tap_more_link_on_the_selected_race_event(self):
        """
        DESCRIPTION: Select module created by Race type ID.
        DESCRIPTION: Desktop: Tap 'View full race card' link under the selected race event
        DESCRIPTION: Mobile: Tap 'More' link on the selected race event
        EXPECTED: user is navigated to the selected event details page
        """
        pass

    def test_003_select_module_with_configured_link_to_sport_landing_pagetap_the_link(self):
        """
        DESCRIPTION: Select module with configured link to Sport landing page.
        DESCRIPTION: Tap the link
        EXPECTED: user is navigated to the configured sport landing page
        """
        pass

    def test_004_select_module_with_the_link_that_should_navigate_user_to_any_other_configured_in_cms_pagetap_the_link(self):
        """
        DESCRIPTION: Select module with the link that should navigate user to any other configured in CMS page.
        DESCRIPTION: Tap the link.
        EXPECTED: User is navigated to the page configure in CMS for the module
        """
        pass
