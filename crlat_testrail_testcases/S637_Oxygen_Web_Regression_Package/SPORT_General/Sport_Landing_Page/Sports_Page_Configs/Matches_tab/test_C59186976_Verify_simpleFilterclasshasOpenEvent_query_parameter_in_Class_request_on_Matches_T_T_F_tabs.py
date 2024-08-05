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
class Test_C59186976_Verify_simpleFilterclasshasOpenEvent_query_parameter_in_Class_request_on_Matches_T_T_F_tabs(Common):
    """
    TR_ID: C59186976
    NAME: Verify  simpleFilter=class.hasOpenEvent query parameter in Class request on 'Matches, 'T'/'T'/'F' tabs
    DESCRIPTION: This test case verifies simpleFilter=class.hasOpenEvent query parameter in Class request on 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs for different Sports(Tier 1, Tier 2)
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Choose one Football event, one more event from Tier 1 (Tennis, Basketball), one event from Tier 2 and Tier 2 sport Outright(e.g. Golf, Cycling, Hurling, Motorbikes).
    PRECONDITIONS: Example of Class request:
    PRECONDITIONS: "https://tst2-backoffice-lcm.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/Class?translationLang=en&responseFormat=json&simpleFilter=class.categoryId:equals:16&simpleFilter=class.isActive&simpleFilter=class.siteChannels:contains:M&simpleFilter=class.hasOpenEvent"
    PRECONDITIONS: - Sport page configurations can be found here: https://confluence.egalacoral.com/pages/viewpage.action?spaceKey=SPI&title=Sport+Page+Configs
    PRECONDITIONS: - What is considered as Class that contains Event that is open for betting:
    PRECONDITIONS: The item contains (or is, or belongs to) a displayed Event on which betting is either currently offered, or has been offered in the last few minutes, or is expected to be offered in the next few minutes. Settled events will not be included; temporarily suspended events will be.
    PRECONDITIONS: Notes:
    PRECONDITIONS: Does not currently take into account the details of the Markets and Outcomes within the Event.
    PRECONDITIONS: NOTE: 'Matches' tab can have another names e.g. 'Events','Fights' etc(depends on Sport you choose)
    """
    keep_browser_open = True

    def test_001_navigate_to_football_landing_page__gtmatchesmobile_todaytomorrowfuturedesktop(self):
        """
        DESCRIPTION: Navigate to Football Landing page -&gt;'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop)
        EXPECTED: 
        """
        pass

    def test_002_check_class_request_on_matchesmobile_todaytomorrowfuturedesktop_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(self):
        """
        DESCRIPTION: Check Class request on 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: * Class request to SS has query parameter:
        EXPECTED: simpleFilter=class.hasOpenEvent
        EXPECTED: * Only Classes that contain an Events that are open for betting are received in response of Class request
        """
        pass

    def test_003_navigate_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_any_other_sport_landing_page_with_tier_1_sport_configurationeg_tennis_basketball(self):
        """
        DESCRIPTION: Navigate to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on any other Sport Landing page with Tier 1 Sport configuration(e.g. Tennis, Basketball)
        EXPECTED: 
        """
        pass

    def test_004_check_class_request_on_matchesmobile_todaytomorrowfuturedesktop_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(self):
        """
        DESCRIPTION: Check Class request on 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: * Class request to SS has query parameter:
        EXPECTED: simpleFilter=class.hasOpenEvent
        EXPECTED: * Only Classes that contain an Events that are open for betting are received in response of Class request
        """
        pass

    def test_005_navigate_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_any_sport_landing_page_with_tier_2_sport_configurationeg_ice_hokey_volleyball_etc(self):
        """
        DESCRIPTION: Navigate to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on any Sport Landing page with Tier 2 Sport Configuration(e.g. Ice Hokey, Volleyball etc.)
        EXPECTED: 
        """
        pass

    def test_006_check_class_request_on_matchesmobile_todaytomorrowfuturedesktop_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(self):
        """
        DESCRIPTION: Check Class request on 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: * Class request to SS has query parameter:
        EXPECTED: simpleFilter=class.hasOpenEvent
        EXPECTED: * Only Classes that contain an Events that are open for betting are received in response of Class request
        """
        pass

    def test_007_navigate_to_matchesmobile_todaytomorrowfuturedesktop_tabs_on_any_sport_landing_page_with_tier_2_sport_outright_configurationeg_golf_cycling_hurling_motorbikes_etc(self):
        """
        DESCRIPTION: Navigate to 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) tabs on any Sport Landing page with Tier 2 Sport Outright Configuration(e.g. Golf, Cycling, Hurling, Motorbikes etc.)
        EXPECTED: 
        """
        pass

    def test_008_check_class_request_on_matchesmobile_todaytomorrowfuturedesktop_and_verify_simplefilterclasshasopenevent_query_parameter_is_present_in_the_request(self):
        """
        DESCRIPTION: Check Class request on 'Matches'(Mobile), 'Today'/'Tomorrow'/'Future'(Desktop) and verify simpleFilter=class.hasOpenEvent query parameter is present in the request.
        EXPECTED: * Class request to SS has query parameter:
        EXPECTED: simpleFilter=class.hasOpenEvent
        EXPECTED: * Only Classes that contain an Events that are open for betting are received in response of Class request
        """
        pass
