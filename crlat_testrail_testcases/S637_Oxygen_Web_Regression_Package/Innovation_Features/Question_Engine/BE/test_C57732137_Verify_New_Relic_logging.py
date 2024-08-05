import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C57732137_Verify_New_Relic_logging(Common):
    """
    TR_ID: C57732137
    NAME: Verify New Relic logging
    DESCRIPTION: This test case verifies New Relic logging
    PRECONDITIONS: Please look for some insights on pages as follow:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS-API+Endpoints
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Symphony+Infrastructure+creds
    PRECONDITIONS: 1. The user is logged on Coral / Labrokes
    PRECONDITIONS: 2. The user is logged in to New Relic ( https://insights.newrelic.com/accounts/1641266/query?query=SELECT%20*%20FROM%20PageAction%20where%20actionName%20%20LIKE%20%27%25correct%25%27%20SINCE%201%20days%20ago&hello=overview )
    PRECONDITIONS: 3. Active quiz already exist
    """
    keep_browser_open = True

    def test_001___open_correct_4_on_coral__ladbrokes__submit_prediction_when_be_returns_400_error(self):
        """
        DESCRIPTION: - Open Correct 4 on Coral / Ladbrokes
        DESCRIPTION: - Submit Prediction when BE returns 400 error
        EXPECTED: Error displayed on XHR
        """
        pass

    def test_002___open_new_relichttpsinsightsnewreliccomaccounts1641266queryqueryselect2020from20pageaction20where20actionname2020like202725correct252720since20120days20agohellooverview(self):
        """
        DESCRIPTION: - Open New Relic
        DESCRIPTION: https://insights.newrelic.com/accounts/1641266/query?query=SELECT%20*%20FROM%20PageAction%20where%20actionName%20%20LIKE%20%27%25correct%25%27%20SINCE%201%20days%20ago&hello=overview
        EXPECTED: New row with 400 error successfully logged
        """
        pass

    def test_003___open_correct_4_on_coral__ladbrokes__submit_prediction_when_be_returns_502_error(self):
        """
        DESCRIPTION: - Open Correct 4 on Coral / Ladbrokes
        DESCRIPTION: - Submit Prediction when BE returns 502 error
        EXPECTED: Error displayed on XHR
        """
        pass

    def test_004___open_new_relichttpsinsightsnewreliccomaccounts1641266queryqueryselect2020from20pageaction20where20actionname2020like202725correct252720since20120days20agohellooverview(self):
        """
        DESCRIPTION: - Open New Relic
        DESCRIPTION: https://insights.newrelic.com/accounts/1641266/query?query=SELECT%20*%20FROM%20PageAction%20where%20actionName%20%20LIKE%20%27%25correct%25%27%20SINCE%201%20days%20ago&hello=overview
        EXPECTED: New row with 502 error successfully logged
        """
        pass

    def test_005___open_correct_4_on_coral__ladbrokes__submit_prediction_when_any_other_issues_appear(self):
        """
        DESCRIPTION: - Open Correct 4 on Coral / Ladbrokes
        DESCRIPTION: - Submit Prediction when any other issues appear
        EXPECTED: Error displayed on XHR
        """
        pass

    def test_006___open_new_relichttpsinsightsnewreliccomaccounts1641266queryqueryselect2020from20pageaction20where20actionname2020like202725correct252720since20120days20agohellooverview(self):
        """
        DESCRIPTION: - Open New Relic
        DESCRIPTION: https://insights.newrelic.com/accounts/1641266/query?query=SELECT%20*%20FROM%20PageAction%20where%20actionName%20%20LIKE%20%27%25correct%25%27%20SINCE%201%20days%20ago&hello=overview
        EXPECTED: New row with any other error successfully logged
        """
        pass

    def test_007___block_call_to_httpsquestion_engine_stg0coralsportsnonprodcloudladbrokescoralcom__open_correct_4_on_coral__ladbrokes(self):
        """
        DESCRIPTION: - Block call to https://question-engine-stg0.coralsports.nonprod.cloud.ladbrokescoral.com
        DESCRIPTION: - Open Correct 4 on Coral / Ladbrokes
        EXPECTED: Error displayed on XHR
        """
        pass

    def test_008___open_new_relichttpsinsightsnewreliccomaccounts1641266queryqueryselect2020from20pageaction20where20actionname20like202725question252720since20120days20agohellooverview(self):
        """
        DESCRIPTION: - Open New Relic
        DESCRIPTION: https://insights.newrelic.com/accounts/1641266/query?query=SELECT%20*%20FROM%20PageAction%20where%20actionName%20LIKE%20%27%25Question%25%27%20SINCE%201%20days%20ago&hello=overview
        EXPECTED: New rows with Question Engine fatal error successfully logged
        """
        pass

    def test_009___block_call_to_httpsquestion_engine_stg0coralsportsnonprodcloudladbrokescoralcomapiv1quizprevioususernamesource_idcorrect4page_number0page_size3__open_correct_4_on_coral__ladbrokes(self):
        """
        DESCRIPTION: - Block call to https://question-engine-stg0.coralsports.nonprod.cloud.ladbrokescoral.com/api/v1/quiz/previous/{username}/?source-id=/correct4&page-number=0&page-size=3
        DESCRIPTION: - Open Correct 4 on Coral / Ladbrokes
        EXPECTED: Error displayed on XHR
        """
        pass

    def test_010___open_new_relichttpsinsightsnewreliccomaccounts1641266queryqueryselect2020from20pageaction20where20actionname20like202725question252720since20120days20agohellooverview(self):
        """
        DESCRIPTION: - Open New Relic
        DESCRIPTION: https://insights.newrelic.com/accounts/1641266/query?query=SELECT%20*%20FROM%20PageAction%20where%20actionName%20LIKE%20%27%25Question%25%27%20SINCE%201%20days%20ago&hello=overview
        EXPECTED: New rows with Question Engine fatal error successfully logged
        """
        pass
