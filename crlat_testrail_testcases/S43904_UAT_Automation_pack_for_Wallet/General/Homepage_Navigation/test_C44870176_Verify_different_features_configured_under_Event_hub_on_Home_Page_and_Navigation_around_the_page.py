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
class Test_C44870176_Verify_different_features_configured_under_Event_hub_on_Home_Page_and_Navigation_around_the_page(Common):
    """
    TR_ID: C44870176
    NAME: Verify different features configured under Event hub on Home Page and Navigation around the page.
    DESCRIPTION: Verify Event hub features . Verify user is able to place bets from different components.
    DESCRIPTION: -Verify when Event Hub Tab is not there, all the Events and Markets data should also be deleted"
    PRECONDITIONS: User should be logged in
    PRECONDITIONS: User should have configured Event hub in CMS with the following features :
    PRECONDITIONS: 1. Surface bets
    PRECONDITIONS: 2. Quick links
    PRECONDITIONS: 3. Highlights carousel
    PRECONDITIONS: 4. Featured module
    PRECONDITIONS: 5. Events/Races are displayed as configured in CMS
    PRECONDITIONS: 6. Display specific markets (Including racing) with the number of selections provided as per CMS (There Should be a setting to display all the selections)
    PRECONDITIONS: 7. Display specific events (Including racing) with the number of selections provided as per CMS (There Should be a setting to display all the selections)
    """
    keep_browser_open = True

    def test_001_load_app(self):
        """
        DESCRIPTION: Load App
        EXPECTED: App is loaded
        """
        pass

    def test_002_tap_on_the_event_hub_that_has_been_configured_in_cms(self):
        """
        DESCRIPTION: Tap on the Event hub that has been configured in CMS
        EXPECTED: Event Hub Page is loaded
        """
        pass

    def test_003_verify_surface_bets(self):
        """
        DESCRIPTION: Verify Surface bets
        EXPECTED: User should be able to scroll across the surface bets displaying on the Event hub page
        """
        pass

    def test_004_tap_on_any_selection_from_surface_bets(self):
        """
        DESCRIPTION: tap on any selection from surface bets
        EXPECTED: Mobile : quick bet should be invoked (if enabled) or selection added to bet slip
        EXPECTED: Tablet : Selection added to the bet slip
        """
        pass

    def test_005_tap_on_the_event(self):
        """
        DESCRIPTION: tap on the event
        EXPECTED: User should land on the corresponding event landing page.
        """
        pass

    def test_006_click_on_back(self):
        """
        DESCRIPTION: click on back
        EXPECTED: User should navigate to the Event hub page
        """
        pass

    def test_007_repeat_steps_4_6_for_featured_module_highlight_carousal_if_available(self):
        """
        DESCRIPTION: repeat steps 4-6 for featured module, Highlight carousal if available
        EXPECTED: 
        """
        pass

    def test_008_click_on_any_of_the_quick_links_available(self):
        """
        DESCRIPTION: Click on any of the Quick links available
        EXPECTED: user should land on the corresponding page. eg : A quick link for 'Today's Football' would navigate to the page where today's matches are listed under Football.
        """
        pass

    def test_009_add_more_selections_to_the_bet_slip_from_different_components_on_the_event_hub_and_place_bet(self):
        """
        DESCRIPTION: Add more selections to the bet slip from different components on the event hub and place bet.
        EXPECTED: Selections get added to the bet slip and user is able to place bet.
        """
        pass

    def test_010_load_cms_and_disabledelete_the_event_hub(self):
        """
        DESCRIPTION: Load CMS and disable/delete the event hub
        EXPECTED: All the components under the Event hub should be deleted and user should not see the Event hub menu item on Home page
        """
        pass
