import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C64055800_GALAXY_S9_Verify_PriceOdds_for_2_Way_Market(Common):
    """
    TR_ID: C64055800
    NAME: [GALAXY S9] Verify PriceOdds for 2-Way Market
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001___________preconditions__________create_event__________featured_module_by_sports_type_id_is_created_in_cms(self):
        """
        DESCRIPTION: *          Preconditions
        DESCRIPTION: *          Create event
        DESCRIPTION: *          Featured Module by <Sports> Type ID is created in CMS
        EXPECTED: *
        """
        pass

    def test_002___________load_oxygen_application(self):
        """
        DESCRIPTION: *          Load Oxygen application
        EXPECTED: *          Homepage is opened
        """
        pass

    def test_003___________access_featured_module(self):
        """
        DESCRIPTION: *          Access featured module
        EXPECTED: *          Featured module is displayed
        """
        pass

    def test_004___________verify_data_of_priceodds_for_verified_event(self):
        """
        DESCRIPTION: *          Verify data of Price/Odds for verified event
        EXPECTED: *          'Price/Odds' corresponds to the **priceNum/priceDen **if **eventStatusCode="A"**
        """
        pass

    def test_005___________verify_order_of_priceodds_buttons_for_2_way_market(self):
        """
        DESCRIPTION: *          Verify order of Price/Odds buttons for 2-Way Market
        EXPECTED: *          Price/Odds are in **Win/Win** order according to **Primary Market**, where:
        EXPECTED: *          *   outcomeMeaningMinorCode="H" is a Home Win
        EXPECTED: *          *   outcomeMeaningMinorCode="A" is a Away Win
        """
        pass

    def test_006___________click_on_priceodds_button_to_add_selection_to_the_betslip_from_the_module(self):
        """
        DESCRIPTION: *          Click on Price/Odds button to add selection to the Betslip from the module
        EXPECTED: *          Selection is added to the Betslip
        """
        pass
