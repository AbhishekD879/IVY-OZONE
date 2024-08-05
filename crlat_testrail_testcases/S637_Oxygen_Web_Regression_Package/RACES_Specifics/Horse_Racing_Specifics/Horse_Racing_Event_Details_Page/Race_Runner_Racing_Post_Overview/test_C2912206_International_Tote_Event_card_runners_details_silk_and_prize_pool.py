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
class Test_C2912206_International_Tote_Event_card_runners_details_silk_and_prize_pool(Common):
    """
    TR_ID: C2912206
    NAME: International Tote Event card: runners details, silk and prize pool
    DESCRIPTION: Test case verifies runners information and silks display on International Tote EDP
    PRECONDITIONS: To see Racing form information find EventToOutcome request on EDP
    PRECONDITIONS: /EventToOutcomeForEvent/{event_id}?simpleFilter=event.suspendAtTime:greaterThan:{date}&racingForm=outcome&racingForm=event&priceHistory=true&externalKeys=event&translationLang=en&prune=event&prune=market
    PRECONDITIONS: where pay attention to the following objects:
    PRECONDITIONS: - event -  contains outcomes names;
    PRECONDITIONS: - racingFormEvent - contains prize value;
    PRECONDITIONS: - racingFormOutcome (for each runner) - contains runner details
    PRECONDITIONS: **Tote pool tab is opened on International Tote event and available pool is selected**
    """
    keep_browser_open = True

    def test_001_verify_prize_pool_value(self):
        """
        DESCRIPTION: Verify Prize Pool value
        EXPECTED: - Prize Pool amount is taken from "prize" key of racingFormEvent object
        """
        pass

    def test_002_verify_runners_summary(self):
        """
        DESCRIPTION: Verify runners summary
        EXPECTED: 1.The following info is displayed in the summary for each runner
        EXPECTED: - Runner number
        EXPECTED: - Runner name
        EXPECTED: - Jokey/Trainer names
        EXPECTED: - Form id
        EXPECTED: 2.Runner name is an outcome name from "event object" of EventToOutcome request.
        EXPECTED: Other info is filled according to racingFormOutcome
        """
        pass

    def test_003_verify_silks(self):
        """
        DESCRIPTION: Verify silks
        EXPECTED: Silks are shown and correct (silk name is from request for racingFormOutcome object from of EventToOutcome request for each runner)
        """
        pass

    def test_004_expand_runner_info_to_see_details(self):
        """
        DESCRIPTION: Expand runner info to see details
        EXPECTED: 1.Details are opened with the following info:
        EXPECTED: - Horse
        EXPECTED: - Jockey
        EXPECTED: - Trainer
        EXPECTED: - Form
        EXPECTED: - Age
        EXPECTED: - Weight
        EXPECTED: - Stall No ("draw" attribute)
        EXPECTED: - Rating
        EXPECTED: 2.Info is filled according to info from racingFormOutcome object from Racing form request
        """
        pass

    def test_005_collapse_the_details(self):
        """
        DESCRIPTION: Collapse the details
        EXPECTED: Details section is collapsed
        """
        pass
