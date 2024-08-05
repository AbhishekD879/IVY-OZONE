import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C58212448_Verify_Specials_are_displayed_on_Matches_Fights_Competitions_Outrights_tabs(Common):
    """
    TR_ID: C58212448
    NAME: Verify Specials are displayed on Matches/Fights, Competitions, Outrights tabs
    DESCRIPTION: This test case verifies Specials are displayed on Matches/Fights, Competitions, Outrights tabs
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: - Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: - **Special** events should contain **drilldownTagNames = MKTFLAG_SP** for **Market level**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. 'Specials', 'Competitions', 'Outrights', 'Fights/Matches' tabs are enabled in CMS for 'Tier 1/2' Sport and data are available
    PRECONDITIONS: 2. **SPECIAL** events are created for the particular Sport (4 different Events):
    PRECONDITIONS: * Matches Event with Primary market with ticked 'Specials' checkbox on market level (there should be 2 Selections created for market)
    PRECONDITIONS: * Outright Event with Outright market with ticked 'Specials' checkbox on market level (there should be 2 Selections created for market)
    PRECONDITIONS: * Matches Event with Primary market with ticked 'Specials' checkbox on market level (there should be only 1 Selection created for market)
    PRECONDITIONS: * Outright Event with Outright market with ticked 'Specials' checkbox on market level (there should be only 1 Selection created for market)
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the selected 'Tier 1/2' Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    """
    keep_browser_open = True

    def test_001_check_specials_events_are_displayed_on_specials_tab(self):
        """
        DESCRIPTION: Check Specials Events are displayed on 'Specials' tab
        EXPECTED: * 4 Events are displayed on Specials tab:
        EXPECTED: * 2 Events with 2 Selections for each event:
        EXPECTED: 'Event Name' and 'right side' arrow are displayed
        EXPECTED: * 2 Events with only 1 Selection for each event:
        EXPECTED: 'Selection Name' and 'Price/Odds' button are displayed
        EXPECTED: ![](index.php?/attachments/get/100880874)
        """
        pass

    def test_002__navigate_to_matchesfights_tab_check_specials_events_are_displayed(self):
        """
        DESCRIPTION: * Navigate to 'Matches'/'Fights' tab.
        DESCRIPTION: * Check Specials Events are displayed.
        EXPECTED: * 2 Events (Matches only) are displayed on Matches/Fights tab:
        EXPECTED: 'Start Date&Time', 'Event Name' and 'Price/Odds' button(s) are displayed
        EXPECTED: ![](index.php?/attachments/get/100880875)
        """
        pass

    def test_003__navigate_to_competitions_tab_check_specials_events_are_displayed(self):
        """
        DESCRIPTION: * Navigate to 'Competitions' tab.
        DESCRIPTION: * Check Specials Events are displayed.
        EXPECTED: * 4 Events are displayed on Specials tab:
        EXPECTED: * 2 Events (Matches):
        EXPECTED: 'Start Date&Time', 'Event Name' and 'Price/Odds' button(s) are displayed
        EXPECTED: * 2 Events (Outrights):
        EXPECTED: 'Event Name' and 'right side' arrow are displayed
        EXPECTED: ![](index.php?/attachments/get/100880876)
        """
        pass

    def test_004__navigate_to_outrights_tab_check_specials_events_are_displayed(self):
        """
        DESCRIPTION: * Navigate to 'Outrights' tab.
        DESCRIPTION: * Check Specials Events are displayed.
        EXPECTED: * 2 Events (Outrights only) are displayed on Matches/Fights tab:
        EXPECTED: 'Event Name' and 'right side' arrow are displayed
        EXPECTED: ![](index.php?/attachments/get/100880877)
        """
        pass
