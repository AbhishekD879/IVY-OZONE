import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.build_your_bet
@vtest
class Test_C2303006_BuildYourBet_Verify_count_of_SiteServe_requests_depending_on_number_of_unique_type_ids_received_from_Banach(Common):
    """
    TR_ID: C2303006
    NAME: BuildYourBet_Verify count of SiteServe requests depending on number of unique type ids received from Banach
    DESCRIPTION: This test case verifies how many requests are sent to SiteServe depending on number of unique type ids received from Banach
    PRECONDITIONS: Build Your Bet tab is available on homepage when:
    PRECONDITIONS: 1)BYB is enabled in CMS
    PRECONDITIONS: mobile/tablet/desktop
    PRECONDITIONS: Module Ribbon Tab -> 'Build Your Bet'; 'Visible' = True;
    PRECONDITIONS: Leagues are available when:
    PRECONDITIONS: 1) Banach leagues are mapped in CMS: Your Call > YourCall leagues
    PRECONDITIONS: 2) Banach league is mapped on Banach side
    PRECONDITIONS: 3) SiteServe returns information about leagues, received from Banach
    PRECONDITIONS: Request to Banach to get leagues: https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%
    PRECONDITIONS: Request to SiteServe based on received leagues from Banach: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForType/YYY?translationLang=LL, where:
    PRECONDITIONS: * YYY - is a comma separated list of **Type** ID's received from Banach (leagues);
    PRECONDITIONS: * X.XX - current supported version of OpenBet release
    PRECONDITIONS: * LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_go_to_module_selector_ribbon(self):
        """
        DESCRIPTION: Go to Module Selector Ribbon
        EXPECTED: For mobile/tablet:
        EXPECTED: 'BYB' tab is present
        EXPECTED: For desktop:
        EXPECTED: BYB access point appears on homepage under 'Next Races'
        """
        pass

    def test_002_for_mobiletablettap_on_build_your_bet_tab(self):
        """
        DESCRIPTION: For mobile/tablet:
        DESCRIPTION: Tap on 'Build Your Bet' tab
        EXPECTED: Respective data is loaded
        """
        pass

    def test_003_open_devtools__network_and_view_response_from_banach_httpsbuildyourbet_dev1coralsportsdevcloudladbrokescoralcomapiv1leagues_upcomingdaystz(self):
        """
        DESCRIPTION: Open devtools > Network and view response from Banach (https://buildyourbet-dev1.coralsports.dev.cloud.ladbrokescoral.com/api/v1/leagues-upcoming?days=%&tz=%)
        EXPECTED: * Response contains 'today' and 'upcoming' leagues i.e. OpenBet type Ids
        EXPECTED: * The same leagues/type ids can be found for 'today' and 'upcoming'
        """
        pass

    def test_004_in_network_view_request_to_siteserve_httpsbackoffice_tst2coralcoukopenbet_ssviewerdrilldownxxxclasstosubtypefortypeyyytranslationlangll(self):
        """
        DESCRIPTION: In Network view request to SiteServe (https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubTypeForType/YYY?translationLang=LL)
        EXPECTED: * Request contains unique type ids, received form Banach, i.e. there is no duplicated type ids
        EXPECTED: * One request contains up to 100 type ids
        EXPECTED: * If there are more than 100 type ids, received from Banach, multiple SiteServe requests are sent, each containing up to 100 ids
        """
        pass
