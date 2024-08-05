import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C29035_Multiples_are_not_available(Common):
    """
    TR_ID: C29035
    NAME: Multiples are not available
    DESCRIPTION: This test case verifies cases situation when Multiples are not available.
    DESCRIPTION: This test case is applied for Mobile and Tablet application.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_verify_the_betslip_without_added_selections_eg_see_betslip_widget_on_tablet_version_or_by_tapping_betslip_bubble_on_mobile(self):
        """
        DESCRIPTION: Verify the Betslip without added selections (e.g. see BetSlip widget on Tablet version or by tapping 'BetSlip' bubble on Mobile)
        EXPECTED: Betslip page does not contain any Multiples
        EXPECTED: Message displayed: "You have no selections in the slip."
        """
        pass

    def test_003_open_any_sport(self):
        """
        DESCRIPTION: Open any sport
        EXPECTED: 
        """
        pass

    def test_004_open_event_details_page(self):
        """
        DESCRIPTION: Open Event Details page
        EXPECTED: 
        """
        pass

    def test_005_add_one_selection_to_the_betslip(self):
        """
        DESCRIPTION: Add one selection to the Betslip
        EXPECTED: 
        """
        pass

    def test_006_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: 'Multiples' section is not available for one added selection
        """
        pass

    def test_007_add_several_selections_from_the_same_market_to_the_betslip(self):
        """
        DESCRIPTION: Add several selections from the same market to the betslip
        EXPECTED: 
        """
        pass

    def test_008_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: 'Multiples' section is not available for added selections
        """
        pass

    def test_009_add_several_selections_from_different_markets_from_the_same_event(self):
        """
        DESCRIPTION: Add several selections from different markets from the same event
        EXPECTED: 
        """
        pass

    def test_010_go_to_betslip(self):
        """
        DESCRIPTION: Go to Betslip
        EXPECTED: 'Multiples' section is not available for added selections
        """
        pass
