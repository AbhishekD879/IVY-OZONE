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
class Test_C10474861_BPG_icon_presence_on_Racing_EDP(Common):
    """
    TR_ID: C10474861
    NAME: BPG icon presence on Racing EDP
    DESCRIPTION: Test is used to check BPG icon presence status on Racing EDP depending on GP checkbox set on market level in TI
    PRECONDITIONS: 1. Event with GP price is available (GP available checkbox is selected on market level in TI (isGpAvailable="true" attribute is returned for the market from SiteServer)) is present
    PRECONDITIONS: 2. Event without GP price is available
    PRECONDITIONS: **NOTE: BPG replaced to BOG ( https://jira.egalacoral.com/browse/BMA-49331 ) from Coral 101.2 / Ladbrokes 100.4 versions**
    """
    keep_browser_open = True

    def test_001_open_race_even_details_page_with_gp_price(self):
        """
        DESCRIPTION: Open <Race> Even Details Page with GP price
        EXPECTED: BPG icon is displayed on market header
        """
        pass

    def test_002_open_race_even_details_page_without_gp_price(self):
        """
        DESCRIPTION: Open <Race> Even Details Page without GP price
        EXPECTED: BPG icon is not displayed on market header
        """
        pass
