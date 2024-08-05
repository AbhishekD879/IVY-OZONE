import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.virtual_sports
@vtest
class Test_C869658_Verify_Speedway_Runner_Number_Icon_Name(Common):
    """
    TR_ID: C869658
    NAME: Verify Speedway Runner Number/Icon/Name
    DESCRIPTION: This test case verifies that Speedway runner number / icon / name correspond to SiteServer response.
    PRECONDITIONS: In order to receive data from the SiteServer use link:
    PRECONDITIONS: 1. To receive a list of event ID's use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/289?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. To see the info about silks, runners, etc. use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXXXXX?racingForm=outcome&translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: XXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_virtual_speedway_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Speedway' sport page
        EXPECTED: 'Virtual Speedway' sport page is opened
        """
        pass

    def test_002_go_to_win_or_ew_section(self):
        """
        DESCRIPTION: Go to Win or E/W section
        EXPECTED: 
        """
        pass

    def test_003_verify_speedway_runner_number(self):
        """
        DESCRIPTION: Verify Speedway Runner Number
        EXPECTED: Speedway Runner Number corresponds to the "draw" attribute
        """
        pass

    def test_004_verify_speedway_runner_icon(self):
        """
        DESCRIPTION: Verify Speedway Runner Icon
        EXPECTED: Speedway Runner Icon corresponds to the "name" attribute
        """
        pass

    def test_005_verifyspeedway_runner_name(self):
        """
        DESCRIPTION: Verify Speedway Runner Name
        EXPECTED: Speedway Runner Name corresponds to the "name" attribute
        """
        pass
