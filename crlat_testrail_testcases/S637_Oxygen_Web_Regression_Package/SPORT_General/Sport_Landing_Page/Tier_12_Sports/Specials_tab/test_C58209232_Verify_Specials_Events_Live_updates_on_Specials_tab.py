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
class Test_C58209232_Verify_Specials_Events_Live_updates_on_Specials_tab(Common):
    """
    TR_ID: C58209232
    NAME: Verify Specials Events Live updates on 'Specials' tab
    DESCRIPTION: This Test Case verifies Specials Events Live updates on 'Specials' tab
    DESCRIPTION: AUTOTEST [C58833982]
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: - Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: - **Special** events should contain the following attributes:
    PRECONDITIONS: **Market level:**
    PRECONDITIONS: * drilldownTagNames = MKTFLAG_SP
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    PRECONDITIONS: **Preconditions:**
    PRECONDITIONS: 1. 'Specials' tab is enabled in CMS for 'Tier 1/2' Sport and data are available
    PRECONDITIONS: 2. **SPECIAL** events of the same Type are created for the particular Sport (2 Events):
    PRECONDITIONS: * Event with 2 selections in specific market
    PRECONDITIONS: * Event with only one selection in specific market
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the selected 'Tier 1/2' Sports Landing Page
    PRECONDITIONS: 3. Choose the 'Specials' tab
    PRECONDITIONS: 4. Make sure created Events are displayed and Price/Odds buttons is displayed for Event with only one selection
    """
    keep_browser_open = True

    def test_001__navigate_to_ti_and_undisplay_event_with_2_selections_navigate_back_to_the_app___specials_tab_do_not_refresh_the_page(self):
        """
        DESCRIPTION: * Navigate to TI and **undisplay** Event with 2 Selections.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Do NOT refresh the page.
        EXPECTED: Event is disappeared from the page
        """
        pass

    def test_002__navigate_to_ti_and_display_undisplayed_in_step1_event_navigate_back_to_the_app___specials_tab_refresh_the_page(self):
        """
        DESCRIPTION: * Navigate to TI and **display** undisplayed (in Step1) Event.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * Event is displayed on the page
        EXPECTED: * Event Name is displayed on Event's card
        """
        pass

    def test_003__navigate_to_ti_and_undisplay_selection_for_event_with_2_selections_navigate_back_to_the_app___specials_tab_do_not_refresh_the_page(self):
        """
        DESCRIPTION: * Navigate to TI and **undisplay** Selection for Event with 2 Selections.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Do NOT refresh the page.
        EXPECTED: * Event is displayed in Type accordion
        EXPECTED: * Selection Name and Price/Odds button is displayed on Event's card
        """
        pass

    def test_004__navigate_to_ti_and_display_undisplayed_in_step3_selection_for_event_with_2_selections_navigate_back_to_the_app___specials_tab_refresh_the_page(self):
        """
        DESCRIPTION: * Navigate to TI and **display** undisplayed (in Step3) Selection for Event with 2 Selections.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * Event is displayed in Type accordion
        EXPECTED: * Event Name is displayed on Event's card
        """
        pass

    def test_005__navigate_to_ti_and_undisplay_selection_for_event_with_only_one_selection_navigate_back_to_the_app___specials_tab_do_not_refresh_the_page(self):
        """
        DESCRIPTION: * Navigate to TI and **undisplay** Selection for Event with only one Selection.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Do NOT refresh the page.
        EXPECTED: Event  is disappeared from Type accordion
        """
        pass

    def test_006__navigate_to_ti_and_display_selection_for_event_with_only_one_selection_navigate_back_to_the_app___specials_tab_refresh_the_page(self):
        """
        DESCRIPTION: * Navigate to TI and **display** Selection for Event with only one Selection.
        DESCRIPTION: * Navigate back to the app -> 'Specials' tab.
        DESCRIPTION: * Refresh the page.
        EXPECTED: * Event is displayed in Type accordion
        EXPECTED: * Selection Name and Price/Odds button is displayed on Event's card
        """
        pass

    def test_007_navigate_to_ti_and_undisplay_all_events_of_the_same_type(self):
        """
        DESCRIPTION: Navigate to TI and **undisplay** all Events of the same Type
        EXPECTED: * Events  are disappeared from Type accordion
        EXPECTED: * Type accordion is disappeared
        """
        pass
