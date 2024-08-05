import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C16408117_NewRelic_monitoring_for_ACCA_insurance_offer(Common):
    """
    TR_ID: C16408117
    NAME: NewRelic monitoring for ACCA insurance offer
    DESCRIPTION: This test case verifies NewRelic tracking by actionName for ACCA insurance offers:
    DESCRIPTION: AccaInsurance=>InfoIconClick
    DESCRIPTION: AccaInsurance=>MoreClickRedirectSuccess
    DESCRIPTION: AccaInsurance=>MoreClickRedirectFailed
    PRECONDITIONS: -There are events with available ACCA Offers.
    PRECONDITIONS: -For configuration ACCA offers, please, use the following instruction: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=MOB&title=How+to+setup+ACCA+offers
    PRECONDITIONS: -To verify ACCA Offer details please check requests in dev tools requests: BuildBet -> betOfferRef -> [i]-> offerType, where i - the array of returned bets
    PRECONDITIONS: - In order to become eligible for ACCA Insurance offer please use category "Football" and market "Match Result"
    PRECONDITIONS: - Open app and log in
    PRECONDITIONS: - Add selections to Betslip that are applicable for ACCA Insurance
    PRECONDITIONS: - Log in to New Relic https://insights.newrelic.com
    PRECONDITIONS: The list of app ID's:
    PRECONDITIONS: Coral:
    PRECONDITIONS: dev: '54469068',
    PRECONDITIONS: devInvictus: '59103563',
    PRECONDITIONS: devRelease: '59104089',
    PRECONDITIONS: test: '54469319',
    PRECONDITIONS: tst2: '54469319',
    PRECONDITIONS: stg: '54469423',
    PRECONDITIONS: hiddenprod: '54469529',
    PRECONDITIONS: prod: '54469560'
    PRECONDITIONS: Ladbrokes:
    PRECONDITIONS: dev: '282661399',
    PRECONDITIONS: test: '54469068',
    PRECONDITIONS: tst2: '54469068',
    PRECONDITIONS: stg: '54469529',
    PRECONDITIONS: hiddenprod: '282659985',
    PRECONDITIONS: prod: '282660680'
    PRECONDITIONS: Example of query: SELECT * FROM PageAction where appId = '54469068' WHERE actionName = 'AccaInsurance=>InfoIconClick' since last week
    PRECONDITIONS: Design of the ACCA Insurance bet is attached below:
    PRECONDITIONS: ![](index.php?/attachments/get/34241)
    """
    keep_browser_open = True

    def test_001_click_on_the_info_icon_of_the_acca_insurance_bet_in_betslip(self):
        """
        DESCRIPTION: Click on the info Icon of the ACCA Insurance bet in betslip
        EXPECTED: *Signposting pop up of "5 Team Acca Insurance Offer" is displayed
        EXPECTED: *"More" and "OK" buttons are present within popup
        """
        pass

    def test_002_go_to_newrelic___insights_section_and_type_the_next_queryexample_of_query_select__from_pageaction_where_appid__appid_where_actionname__accainsuranceinfoiconclick_since_last_weekwhere_appid___is_an_id_for_specific_environment(self):
        """
        DESCRIPTION: Go to NewRelic -> Insights section and type the next query
        DESCRIPTION: Example of query: SELECT * FROM PageAction where appId = '{appID}' WHERE actionName = 'AccaInsurance=>InfoIconClick' since last week
        DESCRIPTION: where appID - is an id for specific environment
        EXPECTED: * Opening of "5 Team Acca Insurance Offer" pop-up is tracked and saved in NewRelic
        EXPECTED: The next attributes are received:
        EXPECTED: *Timestamp (should be there by default)
        EXPECTED: *Action Name
        EXPECTED: *AppID
        EXPECTED: *App Name
        EXPECTED: *App Version
        EXPECTED: *Device
        EXPECTED: *Token
        EXPECTED: *Username
        EXPECTED: And other attributes are received.
        """
        pass

    def test_003_click_on_the_more_button_in_link_in_the_signposting_pop_up_of_5_team_acca_insurance_offer(self):
        """
        DESCRIPTION: Click on the "More" button in link in the signposting pop up of "5 Team Acca Insurance Offer"
        EXPECTED: The user is redirected to 'Promotions' page
        """
        pass

    def test_004_go_to_newrelic___insights_section_and_type_the_next_queryexample_of_query_select__from_pageaction_where_appid__appid_where_actionname__accainsurancemoreclickredirectsuccess_since_last_week(self):
        """
        DESCRIPTION: Go to NewRelic -> Insights section and type the next query
        DESCRIPTION: Example of query: SELECT * FROM PageAction where appId = '{appID}' WHERE actionName = 'AccaInsurance=>MoreClickRedirectSuccess' since last week
        EXPECTED: * The successful click on "More" button is tracked and saved in NewRelic
        EXPECTED: The next attributes are received:
        EXPECTED: *Timestamp (should be there by default)
        EXPECTED: *Action Name
        EXPECTED: *AppID
        EXPECTED: *App Name
        EXPECTED: *App Version
        EXPECTED: *Device
        EXPECTED: *Token
        EXPECTED: *Username
        EXPECTED: And other attributes are received.
        """
        pass

    def test_005_trigger_a_situation_where_clicking_the_more_button_is_failed_for_example_internet_connection_issue(self):
        """
        DESCRIPTION: Trigger a situation where clicking the "More" button is failed (for example internet connection issue)
        EXPECTED: The click on "More" button is unsuccessful and the user in not navigated to 'Promotions' page
        """
        pass

    def test_006_go_to_newrelic___insights_section_and_type_the_next_queryexample_of_query_select__from_pageaction_where_appid__appid_where_actionname__accainsurancemoreclickredirectfailed_since_last_week(self):
        """
        DESCRIPTION: Go to NewRelic -> Insights section and type the next query
        DESCRIPTION: Example of query: SELECT * FROM PageAction where appId = '{appID}' WHERE actionName = 'AccaInsurance=>MoreClickRedirectFailed' since last week
        EXPECTED: * The unsuccessful click on "More" button is tracked and saved in NewRelic
        EXPECTED: The next attributes are received:
        EXPECTED: *Timestamp (should be there by default)
        EXPECTED: *Action Name
        EXPECTED: *AppID
        EXPECTED: *App Name
        EXPECTED: *App Version
        EXPECTED: *Device
        EXPECTED: *Token
        EXPECTED: *Username
        EXPECTED: And other attributes are received.
        """
        pass
