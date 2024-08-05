import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C11482843_Verify_that_Open_API_player_tag_responses_are_logged_in_New_Relic(Common):
    """
    TR_ID: C11482843
    NAME: Verify that Open API player tag responses are logged in New Relic
    DESCRIPTION: This test case verifies ability of business user to access Open API responses with errors analytics using New Relic environment
    DESCRIPTION: Note: Cannot automate as we are not automating NewRelic app
    PRECONDITIONS: 1. Login to New Relic environment at https://insights.newrelic.com (ask your team lead for credentials)
    PRECONDITIONS: ==========
    PRECONDITIONS: - In NRQL query 'appId' attribute defines environment (dev, stage, prod, etc.) on which you're requesting analytics. In order to see needed 'appId' for you environment: Open Oxygen app > Devtools > Console > type "newrelic" > press Enter > in returned values expand 'info' section > applicationID: "xxxxxxxx" (e.g. applicationID: "54469423")
    PRECONDITIONS: - Playtech IMS: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Playtech+IMS
    PRECONDITIONS: - KYC is ON in CMS (System Configuration > Structure > 'KYC' section > "enabled" checkbox is selected)
    """
    keep_browser_open = True

    def test_001_in_new_relic_app__run_nrql_query_select__from_pageaction_where_actionname__getplayertags_and_appid__54469423_since_last_week(self):
        """
        DESCRIPTION: In New Relic app:
        DESCRIPTION: - Run NRQL query: SELECT * FROM PageAction where actionName = 'getPlayerTags' AND appId = '54469423' since last week
        EXPECTED: In received response you should see all player tags within 'playerTags' attribute and all errors (if any returned) in 'getPlayerTagError' attribute
        """
        pass
