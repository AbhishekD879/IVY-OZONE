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
class Test_C10875230_Verify_Racing_Post_Silks_Form_Information_on_different_markets(Common):
    """
    TR_ID: C10875230
    NAME: Verify Racing Post Silks/Form Information on different markets
    DESCRIPTION: This test case verifies Racing Post Silks/Form Information on different markets
    PRECONDITIONS: update: After BMA-40744 implementation we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -------
    PRECONDITIONS: Silks should be available for a horse racing event.
    PRECONDITIONS: To retrieve racing post silks, form and odds information follow the next steps: Open Develop Tools -> Network->All->Choose event id and look at Response: Find {racingFormOutcome} response and use attributes on outcome level:
    PRECONDITIONS: 'name' to see a horse name
    PRECONDITIONS: - **'runnerNumber'** to see a number
    PRECONDITIONS: - **'draw'** to see markets status
    PRECONDITIONS: 'jockey' to see a jockey information
    PRECONDITIONS: 'trainer' to see trainer name
    PRECONDITIONS: - **'formGuide'** to see a form attribute
    PRECONDITIONS: 'courseDistanceWinner' to see Course or/and Distance winner badge
    PRECONDITIONS: - **'silkName'** to find out a name of file to download needed silk
    PRECONDITIONS: Silk can be downloaded using Image URL's.
    PRECONDITIONS: [NOTE! To be changed in OX99. After implementation of BMA-40744 epic: Expected change: work through Aggregation MS (which also uses DF API) and return silk via ID from silks sprite
    PRECONDITIONS: Silks should be loaded from https://aggregation.coral.co.uk/silks/racingpost/17058,243739 by silksIDs]
    PRECONDITIONS: Image URL's:
    PRECONDITIONS: CI-TST2: http://img-tst2.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: CI-STG: http://img-stg2.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: CI-PROD: http://img.coral.co.uk/img/racing_post/<silkName>
    """
    keep_browser_open = True

    def test_001_go_to_the_event_details_page(self):
        """
        DESCRIPTION: Go to the event details page
        EXPECTED: Event details page is opened
        EXPECTED: 'Win or E/W' tab is opened by default
        """
        pass

    def test_002_click_on_win_only_market_tab(self):
        """
        DESCRIPTION: Click on 'Win Only' market tab
        EXPECTED: 'Win Only' market tab is opened
        """
        pass

    def test_003_verify_silk_icon(self):
        """
        DESCRIPTION: Verify silk icon
        EXPECTED: Silk icon corresponds to the picture which is got from the Site Server (**'silkName'** attribute)
        EXPECTED: Generic Silks are displayed for missed mappings
        """
        pass

    def test_004_verify_horse_name(self):
        """
        DESCRIPTION: Verify horse name
        EXPECTED: Horse name corresponds to the **'name' **attribute
        """
        pass

    def test_005_verify_runner_number(self):
        """
        DESCRIPTION: Verify runner number
        EXPECTED: Runner number corresponds to the 'runnerNumber' attribute
        EXPECTED: Runner numbers are NOT displayed and selection (horse) names without runnerNumber attribute are aligned with the other horse names
        """
        pass

    def test_006_verify_draw_number(self):
        """
        DESCRIPTION: Verify draw number
        EXPECTED: Draw Number is contained within brackets and corresponds to the 'draw' attribute
        """
        pass

    def test_007_verify_jockeytrainer_information(self):
        """
        DESCRIPTION: Verify jockey/trainer information
        EXPECTED: Jockey information corresponds to the **'jockey'** attribute
        EXPECTED: Trainer information corresponds to the **'trainer' **attribute
        EXPECTED: The information is shown in next format: **Jockey/Trainer**
        """
        pass

    def test_008_verify_form(self):
        """
        DESCRIPTION: Verify form
        EXPECTED: Form corresponds to the **'formGuide' **attribute
        """
        pass

    def test_009_verify_course_orand_distance_winner_badge(self):
        """
        DESCRIPTION: Verify Course or/and Distance winner badge
        EXPECTED: Course or/and Distance winner badge corresponds to courseDistanceWinner attribute:
        EXPECTED: - Course (C)
        EXPECTED: - Distance (D)
        EXPECTED: - Course and Distance (CD)
        """
        pass

    def test_010_repeat_steps_2_9_for_the_following_tabsbetting_wotop_finishplace_insuranceto_finishmore_markets(self):
        """
        DESCRIPTION: Repeat steps #2-9 for the following tabs:
        DESCRIPTION: 'Betting WO'
        DESCRIPTION: 'Top Finish'
        DESCRIPTION: 'Place Insurance'
        DESCRIPTION: 'To Finish'
        DESCRIPTION: 'More Markets'
        EXPECTED: Tab is opened
        EXPECTED: List of corresponding selections is shown
        EXPECTED: All info corresponds to ER's above
        """
        pass
