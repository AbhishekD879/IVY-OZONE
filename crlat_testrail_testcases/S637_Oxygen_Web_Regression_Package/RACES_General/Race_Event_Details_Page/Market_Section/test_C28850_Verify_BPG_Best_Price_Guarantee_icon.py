import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C28850_Verify_BPG_Best_Price_Guarantee_icon(Common):
    """
    TR_ID: C28850
    NAME: Verify BPG (Best Price Guarantee) icon
    DESCRIPTION: This test case verifies event which has best price guarantee available
    DESCRIPTION: **Jira ticket:**
    DESCRIPTION: BMA-6586 - Racecard Layout Update - Markets and Selections area
    PRECONDITIONS: For verifyfing BPG events special data set up on Site Server is needed.
    PRECONDITIONS: GP tick-box can only be added after SP and LP are ticked.
    PRECONDITIONS: For BPG icon reflection it is needed that attribute **'isGpAvailable'**='true' in the market info in the Site Server response.
    PRECONDITIONS: **NOTE: BPG replaced to BOG ( https://jira.egalacoral.com/browse/BMA-49331 ) from Coral 101.2 / Ladbrokes 100.4 versions**
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_race_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Race> icon from the sports menu ribbon
        EXPECTED: <Race> landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event Details page is opened
        """
        pass

    def test_004_verify_bpg_icon_displaying(self):
        """
        DESCRIPTION: Verify BPG icon displaying
        EXPECTED: *   BPG icon is displayed in the same line as the Each-way terms below <Race> Event markets tab
        EXPECTED: *   BPG icon is displayed for all markets where it is available
        EXPECTED: **Ladbrokes**  BPG icon is absent
        """
        pass

    def test_005_verify_bpg_icon_presence(self):
        """
        DESCRIPTION: Verify BPG icon presence
        EXPECTED: **'isGpAvailable' = 'true**' attribute is prsent on market level in SS response
        """
        pass
