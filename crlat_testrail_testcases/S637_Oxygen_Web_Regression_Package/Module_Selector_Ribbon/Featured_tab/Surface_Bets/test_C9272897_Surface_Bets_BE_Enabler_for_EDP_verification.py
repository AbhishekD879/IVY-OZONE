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
class Test_C9272897_Surface_Bets_BE_Enabler_for_EDP_verification(Common):
    """
    TR_ID: C9272897
    NAME: Surface Bets BE Enabler for EDP verification
    DESCRIPTION: Test Case checks that the correct response is received for the Surface Bet configured for Event Details Page
    PRECONDITIONS: 1. Login to CMS
    PRECONDITIONS: 2. On the Sports Pages > Homepage > Surface Bets module > Create a few Surface Bets with the valid Selection Id and assign it to the few Events
    PRECONDITIONS: 3. Create a few Surface Bets for Home Page and Sport page with valid Selection Id
    PRECONDITIONS: 4. There are some expired Surface Bets for Homepage/Sport Page/EDP
    PRECONDITIONS: 5. In Swagger, perform request to public API:
    PRECONDITIONS: GET /{brand}/edp-surface-bets/{eventId}
    PRECONDITIONS: where {brand} - valid brand, {eventId} - valid event id
    """
    keep_browser_open = True

    def test_001_verify_the_response_is_received_and_contains_the_active_surface_bets_configured_for_the_edp(self):
        """
        DESCRIPTION: Verify the response is received and contains the active Surface Bets configured for the EDP
        EXPECTED: Response of the following format is received:
        EXPECTED: {
        EXPECTED: "@type": "SURFACE_BET",
        EXPECTED: "pageId": "{eventId}",
        EXPECTED: "pageType": "edp",
        EXPECTED: "edpOn": true,
        EXPECTED: "reference": {
        EXPECTED: "relationType": "edp",
        EXPECTED: "refId": "12345",
        EXPECTED: "enabled": true
        EXPECTED: }
        EXPECTED: ...
        EXPECTED: }
        """
        pass

    def test_002_perform_a_request_with_the_second_assigned_event_details_page_and_pass_step_1(self):
        """
        DESCRIPTION: Perform a request with the second assigned Event Details page and pass step 1
        EXPECTED: 
        """
        pass

    def test_003_verify_the_response_contains_data_on_the_surface_bet_from_the_cms(self):
        """
        DESCRIPTION: Verify the response contains data on the Surface Bet from the CMS
        EXPECTED: Response contains data on markets loaded from the CMS:
        EXPECTED: "refId": eventId,
        EXPECTED: "title": "sbTitle"
        EXPECTED: "content": "sbContent"
        EXPECTED: "price": {...}
        """
        pass

    def test_004_verify_the_response_contains_data_on_the_market_selections_event(self):
        """
        DESCRIPTION: Verify the response contains data on the market, selections, event
        EXPECTED: * Response contains data on selections loaded from the OB:
        EXPECTED: {
        EXPECTED: "eventId": "eventId",
        EXPECTED: }
        EXPECTED: * Response contains data on selections loaded from the OB:
        EXPECTED: "outcomes": [
        EXPECTED: {
        EXPECTED: "id": "selectionId",
        EXPECTED: "name": "selectionName",
        EXPECTED: ...
        EXPECTED: }
        EXPECTED: ...]
        EXPECTED: * Response contains data on price loaded from the OB, e.g.:
        EXPECTED: "selectionPrice": [
        EXPECTED: {
        EXPECTED: "priceType": "LP",
        EXPECTED: "priceNum": 1,
        EXPECTED: "priceDen": 10,
        EXPECTED: "priceDec": 1.1
        EXPECTED: }
        EXPECTED: ...]
        """
        pass

    def test_005_in_the_cms_edit_the_valid_surface_bet_for_the_home_page_untick_display_on_edp_checkbox_and_saveverify_this_surface_bets_is_not_present_in_the_response(self):
        """
        DESCRIPTION: In the CMS edit the valid Surface Bet for the Home Page, untick "Display on EDP" checkbox and save.
        DESCRIPTION: Verify this Surface Bets is not present in the response
        EXPECTED: Response doesn't contain Surface Bets those are not configured for the EDP
        """
        pass

    def test_006_in_the_cms_edit_the_valid_surface_bet_for_the_edp_untick_enabled_checkbox_and_saveverify_this_surface_bets_is_not_present_in_the_response(self):
        """
        DESCRIPTION: In the CMS edit the valid Surface Bet for the EDP, untick Enabled checkbox and save.
        DESCRIPTION: Verify this Surface Bets is not present in the response
        EXPECTED: Response doesn't contain disabled Surface Bets
        """
        pass

    def test_007_in_the_cms_edit_the_valid_surface_bet_for_the_edp_set_the_incorrect_selection_id_and_saveverify_this_surface_bets_is_not_present_in_the_response(self):
        """
        DESCRIPTION: In the CMS edit the valid Surface Bet for the EDP, set the incorrect selection Id and save.
        DESCRIPTION: Verify this Surface Bets is not present in the response
        EXPECTED: Response doesn't contain Surface Bets with incorrect selection Id
        """
        pass
