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
class Test_C1056147_Verify_Racing_Post_Silks_Form_Information_when_silks_are_not_available(Common):
    """
    TR_ID: C1056147
    NAME: Verify Racing Post Silks/Form Information when silks are not available
    DESCRIPTION: This test case verifies how racing post info will be displayed for each event when silks are not available for the event.
    DESCRIPTION: AUTOTEST: [C1952611]
    PRECONDITIONS: update: After BMA-40744 implementation we'll receive needed data from DF api:
    PRECONDITIONS: Racing Data Hub link:
    PRECONDITIONS: Coral DEV : cd-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: Ladbrokes DEV : https://ld-dev1.api.datafabric.dev.aws.ladbrokescoral.com/v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key=LDaa2737afbeb24c3db274d412d00b6d3b
    PRECONDITIONS: URI : /v4/sportsbook-api/categories/{categoryKey}/events/{eventKey}/content?locale=en-GB&api-key={api-key}
    PRECONDITIONS: {categoryKey} : 21 - Horse racing, 19 - Greyhound
    PRECONDITIONS: {eventKey} : OB Event id
    PRECONDITIONS: -------
    PRECONDITIONS: 1. Absolutely no silks should be available for all runners within a single race.
    PRECONDITIONS: **NOTE:** When no silks are available, there is not going to be shown also information about racing outcome.
    PRECONDITIONS: 2. To retrieve racing post silks, form and odds information follow the next steps:
    PRECONDITIONS: Open Develop Tools -> Network->All->Choose event id and look at Response:
    PRECONDITIONS: Find {racingFormOutcome} response and use attributes on outcome level:
    PRECONDITIONS: - **'name'** to see a horse name
    PRECONDITIONS: - **'runnerNumber'** to see a number
    PRECONDITIONS: - **'draw'** to see markets status
    PRECONDITIONS: - **'jockey'** to see a jockey information
    PRECONDITIONS: - **'trainer'** to see trainer name
    PRECONDITIONS: - **'formGuide'** to see a form attribute
    PRECONDITIONS: - **'silkName'** to find out a name of file to download needed silk.
    PRECONDITIONS: Silk can be downloaded using Image URL's.
    PRECONDITIONS: Image URL's:
    PRECONDITIONS: [NOTE! To be changed in OX99. After implementation of BMA-40744 epic: Expected change: work through Aggregation MS (which also uses DF API) and return silk via ID from silks sprite
    PRECONDITIONS: Silks should be loaded from https://aggregation.coral.co.uk/silks/racingpost/17058,243739 by silksIDs]
    PRECONDITIONS: CI-TST2: http://img-tst2.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: CI-STG: http://img-stg2.coral.co.uk/img/racing_post/<silkName>
    PRECONDITIONS: CI-PROD: http://img.coral.co.uk/img/racing_post/<silkName>
    """
    keep_browser_open = True

    def test_001_go_to_event_details_page(self):
        """
        DESCRIPTION: Go to event details page
        EXPECTED: * Event details page is opened
        EXPECTED: * 'Win or E/W' tab is opened by default
        """
        pass

    def test_002_verify_silk_icon(self):
        """
        DESCRIPTION: Verify silk icon
        EXPECTED: * Generic silk images are displayed
        EXPECTED: * Only runner numbers are displayed
        """
        pass

    def test_003_check_event_for_which_runnernumber_attribute_and_silk_are_not_available_for_allsome_runners_within_a_single_race(self):
        """
        DESCRIPTION: Check event for which runnerNumber attribute and silk are not available for all/some runners within a single race
        EXPECTED: Runner numbers are NOT displayed and selection (horse) names without runnerNumber attribute are aligned with the other horse names
        """
        pass
