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
class Test_C869686_Verify_Motorsport_Runner_Icon_and_Name(Common):
    """
    TR_ID: C869686
    NAME: Verify Motorsport Runner Icon and Name
    DESCRIPTION: This test case verifies that Motorsport runner number and name correspond to the SiteServer response.
    PRECONDITIONS: In order to receive data from the SiteServer use link:
    PRECONDITIONS: 1. To receive a list of event ID's use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/288?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
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

    def test_001_go_to_virtual_motorsports_sport_page(self):
        """
        DESCRIPTION: Go to 'Virtual Motorsports' sport page
        EXPECTED: "Virtual Motorsports" page is opened
        """
        pass

    def test_002_go_to_win_or_ew_section(self):
        """
        DESCRIPTION: Go to Win or E/W section
        EXPECTED: 
        """
        pass

    def test_003_verify_motosport_runner_icon(self):
        """
        DESCRIPTION: Verify motosport runner icon
        EXPECTED: Motorsport runner icon corresponds to the "silkName" attribute in "racingFormOutcome" section and equals "runner" number
        """
        pass

    def test_004_verifymotorsport_runner_name(self):
        """
        DESCRIPTION: Verify motorsport runner name
        EXPECTED: Motorsports runner corresponds to the "name" attribute
        """
        pass
