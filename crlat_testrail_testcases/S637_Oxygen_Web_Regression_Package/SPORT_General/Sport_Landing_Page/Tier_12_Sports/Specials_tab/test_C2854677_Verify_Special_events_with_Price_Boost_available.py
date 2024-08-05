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
class Test_C2854677_Verify_Special_events_with_Price_Boost_available(Common):
    """
    TR_ID: C2854677
    NAME: Verify Special events with Price Boost available
    DESCRIPTION: This test case verifies how Special event with 'Price Boost' flag is displayed on 'Specials' tab
    DESCRIPTION: **Will be available from 102.0 Coral and 102.0 Ladbrokes**
    PRECONDITIONS: **CMS Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **OB Configurations:**
    PRECONDITIONS: **Special** events should contain the following settings:
    PRECONDITIONS: - |Not Primary market| should be created
    PRECONDITIONS: - Set the **drilldownTagNames = MKTFLAG_SP** for |Not Primary market| on market level ('Specials' flag to be ticked on market level in TI)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available on SS
    PRECONDITIONS: 2. 'Special' event is created with:
    PRECONDITIONS: - 'Price Boost' flag ticked on Market level in TI
    PRECONDITIONS: - Selection name should contain 'Was price' in brackets e.g. |Antalyaspor, Altinordu and Krylia Sovetov All To Win (Was 12/1)|
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    """
    keep_browser_open = True

    def test_001_verify_special_event_with_rice_boost_displaying(self):
        """
        DESCRIPTION: Verify 'Special' event with 'Rice Boost' displaying
        EXPECTED: Event contains:
        EXPECTED: * Selection name
        EXPECTED: * Event start date and time
        EXPECTED: * 'Price/odds' button
        EXPECTED: * 'Was price' part
        """
        pass

    def test_002_verify_selection_name(self):
        """
        DESCRIPTION: Verify selection name
        EXPECTED: * Selection name corresponds to 'name' attribute on 'outcome' level
        EXPECTED: * Selection name doesn't contain 'Was price' part
        """
        pass

    def test_003_verify_start_date_and_time(self):
        """
        DESCRIPTION: Verify start date and time
        EXPECTED: Event start date and time corresponds to event 'startTime' attribute
        """
        pass

    def test_004_verify_priceodds_button(self):
        """
        DESCRIPTION: Verify 'Price/odds' button
        EXPECTED: Value on 'Price/odds' button corresponds to 'priceNum'/'priceDen' attributes for fractional and 'priceDec' attribute for decimal
        """
        pass

    def test_005_verify_was_price(self):
        """
        DESCRIPTION: Verify 'Was price'
        EXPECTED: * 'Was price' is displayed below 'Price/odds' button in strikethrough text
        EXPECTED: * Corresponds to 'Was price' part from selection name e.g. Was 12/1
        """
        pass

    def test_006_tapclick_on_special_event_with_rice_boost(self):
        """
        DESCRIPTION: Tap/click on 'Special' event with 'Rice Boost'
        EXPECTED: Corresponding event details page is opened
        """
        pass
