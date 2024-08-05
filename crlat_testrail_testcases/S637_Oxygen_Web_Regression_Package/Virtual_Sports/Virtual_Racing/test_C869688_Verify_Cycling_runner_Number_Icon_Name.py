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
class Test_C869688_Verify_Cycling_runner_Number_Icon_Name(Common):
    """
    TR_ID: C869688
    NAME: Verify Cycling runner Number/Icon/Name
    DESCRIPTION: This test case verifies that Cycling runner number, Cycling runner silk icon and Cycling runner  name correspond to SiteServer response.
    PRECONDITIONS: In order to receive data from the SiteServer use link:
    PRECONDITIONS: 1. To receive a list of event ID's use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/290?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
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

    def test_001_go_to_virtual_cycling_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Cycling' sport page
        EXPECTED: 'Virtual Cycling' sport page is opened
        """
        pass

    def test_002_go_to_win_or_ew_section(self):
        """
        DESCRIPTION: Go to Win or E/W section
        EXPECTED: 
        """
        pass

    def test_003_verify_cycling_runner_number(self):
        """
        DESCRIPTION: Verify Cycling runner Number
        EXPECTED: Cycling runner Number corresponds to the "draw" attribute
        """
        pass

    def test_004_verify_cycling_runner_silk_icons(self):
        """
        DESCRIPTION: Verify Cycling runner Silk icons
        EXPECTED: Cycling runner Silk icons corresponds to the "silkName" attribute
        """
        pass

    def test_005_verifycycling_runnername(self):
        """
        DESCRIPTION: Verify Cycling runner Name
        EXPECTED: Cycling runner Name corresponds to the "name" attribute
        """
        pass
