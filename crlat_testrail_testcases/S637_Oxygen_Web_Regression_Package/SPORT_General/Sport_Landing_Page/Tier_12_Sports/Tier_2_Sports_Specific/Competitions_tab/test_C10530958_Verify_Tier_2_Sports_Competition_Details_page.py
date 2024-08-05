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
class Test_C10530958_Verify_Tier_2_Sports_Competition_Details_page(Common):
    """
    TR_ID: C10530958
    NAME: Verify Tier 2 Sports Competition Details page
    DESCRIPTION: This test case verifies Tier 2 Sports Competition details page
    PRECONDITIONS: 1. Make sure that the following events are created in TI for any Tier 2 Sport:
    PRECONDITIONS: - events are within the same competition
    PRECONDITIONS: - events count is at least 4
    PRECONDITIONS: - at least one 'Outright' event
    PRECONDITIONS: 2. Load the app
    PRECONDITIONS: 3. Navigate to the Sport Landing page
    PRECONDITIONS: 3. Click/Tap on 'Competitions' tab
    PRECONDITIONS: 4. Click/Tap on 'See all' link on expanded accordion (Make sure that the Events Limit is configured in CMS and equal '3' by default (System Configuration -> Structure -> SportCompetitionsTab. It's needed for 'See all' link presence)
    PRECONDITIONS: **Configurations:**
    PRECONDITIONS: Please see the following instruction https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-CMSconfigurations to make the all necessary settings in CMS
    PRECONDITIONS: **Note:**
    PRECONDITIONS: - To see what CMS is in use type "devlog" over the opened application or go to URL: https://your_environment/buildInfo.json
    PRECONDITIONS: - CMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Environments+-+to+be+reviewed
    PRECONDITIONS: - To verify queries from Front-end to SiteServe for data availability checking use the following instruction:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+get+data+from+Openbet+Site+Server
    PRECONDITIONS: - To verify queries from CMS to SiteServe for data availability checking use the following instruction: https://confluence.egalacoral.com/display/SPI/Sport+Page+Configs#SportPageConfigs-QueriestoSiteServe(SS)
    """
    keep_browser_open = True

    def test_001_verify_competition_details_page(self):
        """
        DESCRIPTION: Verify Competition details page
        EXPECTED: The following elements are present on the page:
        EXPECTED: * 'Back' button
        EXPECTED: * 'COMPETITIONS' label **Coral**
        EXPECTED: * Competition header with the competition name
        EXPECTED: * 'Matches' and 'Outrights' switchers (displayed only when there are both matches and outrights for selected type in)
        EXPECTED: * 'Matches' switcher is selected by default and all events from the league are shown
        EXPECTED: ![](index.php?/attachments/get/59878983)
        EXPECTED: ![](index.php?/attachments/get/59878982)
        """
        pass

    def test_002_navigate_between_switchers(self):
        """
        DESCRIPTION: Navigate between switchers
        EXPECTED: * User is able to navigate between switchers
        EXPECTED: * Relevant information is shown in each case
        """
        pass

    def test_003_clicktap_the_back_button(self):
        """
        DESCRIPTION: Click/Tap the 'Back' button
        EXPECTED: User is taken to the 'Competitions' tab on Sport Landing page
        """
        pass

    def test_004_clicktap_on_see_all_link_on_expanded_accordion(self):
        """
        DESCRIPTION: Click/Tap on 'See all' link on expanded accordion
        EXPECTED: User is taken to the selected competition details page
        """
        pass

    def test_005_on_matches_switcher_clicktap_on_any_event_card(self):
        """
        DESCRIPTION: On 'Matches' switcher click/tap on any event card
        EXPECTED: Respective event details page opens
        """
        pass

    def test_006_clicktap_back_button_and_clicktap_on_any_outright_event_on_outrights_switcher(self):
        """
        DESCRIPTION: Click/Tap 'Back' button and click/Tap on any outright event on 'Outrights' switcher
        EXPECTED: Respective Outright event details page opens
        """
        pass
