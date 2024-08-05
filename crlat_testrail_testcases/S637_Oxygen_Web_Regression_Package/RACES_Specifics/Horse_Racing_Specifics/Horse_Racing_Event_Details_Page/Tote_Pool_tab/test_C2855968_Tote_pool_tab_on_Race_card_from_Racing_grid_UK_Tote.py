import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2855968_Tote_pool_tab_on_Race_card_from_Racing_grid_UK_Tote(Common):
    """
    TR_ID: C2855968
    NAME: Tote pool tab on Race card from Racing grid (UK Tote)
    DESCRIPTION: Test case verifies tote pool tab availability after navigation to Race card from UK & IRE grid
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: Enable_ UK_ Totepools = True
    PRECONDITIONS: UK&IRE events with tote pools are available
    PRECONDITIONS: **Instruction on UK tote pool mapping**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+UK+Tote+event+to+the+Regular+HR+event
    PRECONDITIONS: **Request from pool types on EDP**
    PRECONDITIONS: PoolForEvent/event_id
    PRECONDITIONS: **User is on Horse Racing Landing page**
    """
    keep_browser_open = True

    def test_001_tap_on_the_event_from_uk__ire_having_tote_pool(self):
        """
        DESCRIPTION: Tap on the event from UK & IRE having tote pool
        EXPECTED: - Event Race card is opened
        EXPECTED: - Totepool tab is present on Race card
        """
        pass

    def test_002_tap_on_the_totepool_tab(self):
        """
        DESCRIPTION: Tap on the Totepool tab
        EXPECTED: - Totepool tab is selected
        EXPECTED: - Supported pool types (from request PoolForEvent) are displayed
        """
        pass

    def test_003_verify_url_path(self):
        """
        DESCRIPTION: Verify url path
        EXPECTED: Path contains /{event_id}/totepool/{pool type}
        """
        pass
