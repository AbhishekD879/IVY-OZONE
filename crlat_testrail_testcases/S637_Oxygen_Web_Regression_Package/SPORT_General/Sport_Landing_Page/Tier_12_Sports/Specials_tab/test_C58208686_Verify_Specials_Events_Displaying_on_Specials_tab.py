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
class Test_C58208686_Verify_Specials_Events_Displaying_on_Specials_tab(Common):
    """
    TR_ID: C58208686
    NAME: Verify Specials Events Displaying on 'Specials' tab
    DESCRIPTION: This test case verifies data of Specials Events which displayed on Specials tab
    DESCRIPTION: AUTOTEST [C58694710]
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: - Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: - **Specials** Events should be created only with **No Primary** markets
    PRECONDITIONS: - **Special** events should contain **drilldownTagNames = MKTFLAG_SP** for **Market level**
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available
    PRECONDITIONS: 2. **SPECIAL** events are created for the particular Sport:
    PRECONDITIONS: * Events for at least two different Types
    PRECONDITIONS: * Event with only one selection in specific market
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the selected 'Tier 1/2' Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    """
    keep_browser_open = True

    def test_001_check_type_accordions_displaying(self):
        """
        DESCRIPTION: Check Type accordions displaying
        EXPECTED: * Events are shown within Type accordions
        EXPECTED: * First Type accordion is expanded by default and other Type accordions are collapsed by default
        EXPECTED: * Type accordion header title contains <Class> - <Type>
        """
        pass

    def test_002_check_special_event_displaying_when_event_contains_more_than_one_selection_within_market(self):
        """
        DESCRIPTION: Check special event displaying when event contains more than one selection within market
        EXPECTED: Only event name (without price/odds button) and right-side arrow are shown
        """
        pass

    def test_003_check_special_event_displaying_if_event_contains_only_one_selection_within_market(self):
        """
        DESCRIPTION: Check Special event displaying if event contains only one selection within market
        EXPECTED: Selection name and price/odds button is shown
        """
        pass

    def test_004_clicktap_on_eventselection_name(self):
        """
        DESCRIPTION: Click/Tap on 'Event/Selection' name
        EXPECTED: Event details page is opened
        """
        pass
