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
class Test_C43885008_Verify_live_updates_on_Surface_Bets_module(Common):
    """
    TR_ID: C43885008
    NAME: Verify  live updates on 'Surface Bets' module
    DESCRIPTION: Test case verifies live updates on 'Surface Bets' module
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Homepage -> 'Featured' tab
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: 1) 'Surface Bets' module should be "Active" in CMS > Sport Pages > Homepage > Surface Bets module
    PRECONDITIONS: 2) You should have active 'Surface Bets' module with active events in CMS > Sport Pages > Homepage > Surface Bets module
    PRECONDITIONS: - Surface Bets module should be configured by EventIDs
    PRECONDITIONS: - Surface Bets module should be configured by SelectionID
    PRECONDITIONS: **Note:**
    PRECONDITIONS: 1) To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: 2) To verify data for created 'Surface Bets' module use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket (featured-sports...) -> response with type: "FEATURED_STRUCTURE_CHANGED" -> modules -> @type: "SurfaceBetModuleData" and choose the appropriate module.
    PRECONDITIONS: ![](index.php?/attachments/get/37874412)
    PRECONDITIONS: - To see what CMS and TI is in use type "devlog" over opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - TI: https://confluence.egalacoral.com/display/SPI/OpenBet+Systems
    PRECONDITIONS: - "Surface Bets" module should be "Active" in CMS > Sport Pages > Homepage > Surface Bets module
    PRECONDITIONS: - You should have an active Surface Bets module with active events in CMS > Sport Pages > Homepage > Surface Bets module
    PRECONDITIONS: - You should be on a home page in application
    """
    keep_browser_open = True

    def test_001___in_ti_tool_increase_the_price_for_one_of_the_selections_of_event_displayed_in_surface_bets_module__verify_live_updates_in_surface_bets_module(self):
        """
        DESCRIPTION: - In TI tool increase the price for one of the selections of event displayed in Surface Bets module
        DESCRIPTION: - Verify live updates in Surface Bets module
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to red for a few seconds
        """
        pass

    def test_002___in_ti_tool_decrease_the_price_for_one_of_the_selections_of_event_displayed_in_surface_bets_module__verify_live_updates_in_surface_bets_module(self):
        """
        DESCRIPTION: - In TI tool decrease the price for one of the selections of event displayed in Surface Bets module
        DESCRIPTION: - Verify live updates in Surface Bets module
        EXPECTED: - Corresponding 'Price/Odds' button immediately displays new price
        EXPECTED: - The outcome button changes its color to blue for a few seconds
        """
        pass
