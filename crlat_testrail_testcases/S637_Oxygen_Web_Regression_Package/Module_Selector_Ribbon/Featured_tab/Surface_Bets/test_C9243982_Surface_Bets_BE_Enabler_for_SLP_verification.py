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
class Test_C9243982_Surface_Bets_BE_Enabler_for_SLP_verification(Common):
    """
    TR_ID: C9243982
    NAME: Surface Bets BE Enabler for SLP verification
    DESCRIPTION: Test Case checks that the correct response is received for the Surface Bet configured for Sport Page
    PRECONDITIONS: 1. Login to CMS
    PRECONDITIONS: 2. On the Sports Pages > Sport Page > Surface Bets module > Create a few Surface Bets for the Sport Page with the valid Selection Id
    PRECONDITIONS: 3. Create a few Surface Bets for Home Page and EDP with valid Selection Id
    PRECONDITIONS: 4. There are some expired Surface Bets for Homepage/Sport Page/EDP
    PRECONDITIONS: 5. Open the corresponding Sport page
    """
    keep_browser_open = True

    def test_001_verify_the_ws_response_with_module_surfacebetmodule_is_received_and_contains_the_active_surface_bets_configured_for_the_sport_page(self):
        """
        DESCRIPTION: Verify the WS response with module SurfaceBetModule is received and contains the active Surface Bets configured for the Sport Page
        EXPECTED: Response of the following format is received:
        EXPECTED: {
        EXPECTED: "@type": "SurfaceBetModule"
        EXPECTED: ...
        EXPECTED: {
        EXPECTED: "@type": "SurfaceBetModuleData"
        EXPECTED: },
        EXPECTED: ...
        EXPECTED: {
        EXPECTED: "@type": "SurfaceBetModuleData"
        EXPECTED: }
        EXPECTED: }
        """
        pass

    def test_002_verify_the_response_contains_data_on_the_surface_bet(self):
        """
        DESCRIPTION: Verify the response contains data on the Surface Bet
        EXPECTED: Response contains data on surface bet configuration loaded from the CMS:
        EXPECTED: "sportId": sportCategoryId
        EXPECTED: "title": "sbTitle"
        EXPECTED: "content": "smContent
        EXPECTED: "oldPrice": {...}
        """
        pass

    def test_003_verify_the_response_contains_data_on_the_market_selections_event(self):
        """
        DESCRIPTION: Verify the response contains data on the market, selections, event
        EXPECTED: * Response contains data on markets loaded from the OB:
        EXPECTED: "markets": [
        EXPECTED: {
        EXPECTED: "id": "marketId",
        EXPECTED: "name": "marketName",
        EXPECTED: "isLpAvailable": true,
        EXPECTED: ...
        EXPECTED: }
        EXPECTED: ...]
        EXPECTED: * Response contains data on selections loaded from the OB:
        EXPECTED: "outcomes": [
        EXPECTED: {
        EXPECTED: "id": "selectionId",
        EXPECTED: "name": "selectionName",
        EXPECTED: ...
        EXPECTED: }
        EXPECTED: ...]
        EXPECTED: * Response contains data on prices loaded from the OB, e.g.:
        EXPECTED: "prices": [
        EXPECTED: {
        EXPECTED: "id": "1",
        EXPECTED: "priceType": "LP",
        EXPECTED: "priceNum": 1,
        EXPECTED: "priceDen": 10,
        EXPECTED: "priceDec": 1.1
        EXPECTED: }
        EXPECTED: ...]
        """
        pass

    def test_004_in_the_cms_edit_the_valid_surface_bet_for_the_sport_page_within_the_show_on_sports_untick_the_current_sport_category_and_saveverify_this_surface_bets_is_not_present_in_the_response(self):
        """
        DESCRIPTION: In the CMS edit the valid Surface Bet for the Sport Page, within the Show on Sports untick the current sport category and save.
        DESCRIPTION: Verify this Surface Bets is not present in the response
        EXPECTED: Response doesn't contain Surface Bets those are not configured for the current sport page
        """
        pass

    def test_005_in_the_cms_edit_the_valid_surface_bet_for_the_sport_page_untick_enabled_checkbox_and_saveverify_this_surface_bets_is_not_present_in_the_response(self):
        """
        DESCRIPTION: In the CMS edit the valid Surface Bet for the Sport Page, untick Enabled checkbox and save.
        DESCRIPTION: Verify this Surface Bets is not present in the response
        EXPECTED: Response doesn't contain disabled Surface Bets
        """
        pass

    def test_006_in_the_cms_edit_the_valid_surface_bet_for_the_sport_page_make_it_expired_and_saveverify_this_surface_bets_is_not_present_in_the_response(self):
        """
        DESCRIPTION: In the CMS edit the valid Surface Bet for the Sport Page, make it expired and save.
        DESCRIPTION: Verify this Surface Bets is not present in the response
        EXPECTED: Response doesn't contain expired Surface Bets
        """
        pass

    def test_007_in_the_cms_edit_the_valid_surface_bet_for_the_sport_page_set_the_incorrect_selection_id_and_saveverify_this_surface_bets_is_not_present_in_the_response(self):
        """
        DESCRIPTION: In the CMS edit the valid Surface Bet for the Sport Page, set the incorrect selection Id and save.
        DESCRIPTION: Verify this Surface Bets is not present in the response
        EXPECTED: Response doesn't contain Surface Bets with incorrect selection Id
        """
        pass
