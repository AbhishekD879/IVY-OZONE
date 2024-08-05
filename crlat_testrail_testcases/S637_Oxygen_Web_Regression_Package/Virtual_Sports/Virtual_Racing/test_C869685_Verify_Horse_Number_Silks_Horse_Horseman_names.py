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
class Test_C869685_Verify_Horse_Number_Silks_Horse_Horseman_names(Common):
    """
    TR_ID: C869685
    NAME: Verify Horse Number/Silks, Horse/Horseman names
    DESCRIPTION: This test case verifies that Horse number, Horse silk icon, Horse name and Horseman name correspond to SiteServer response.
    PRECONDITIONS: In order to receive data from the SiteServer use link:
    PRECONDITIONS: 1. To receive a list of event ID's use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 2. To see the info about silks, runners etc. use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXXXXXX?racingForm=outcome&translationLang=LL
    PRECONDITIONS: X.XX - current supported version of OpenBet release
    PRECONDITIONS: XXXXXX - event id
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_go_to_win_or_ew_section(self):
        """
        DESCRIPTION: Go to Win or E/W section
        EXPECTED: 
        """
        pass

    def test_002_verify_horse_number(self):
        """
        DESCRIPTION: Verify Horse Number
        EXPECTED: Horse Number corresponds to the "draw" attribute.
        """
        pass

    def test_003_verify_horse_silk_icons(self):
        """
        DESCRIPTION: Verify Horse Silk icons
        EXPECTED: Horse Silk icon corresponds to the "silkName" attribute.
        """
        pass

    def test_004_verifyhorse_name(self):
        """
        DESCRIPTION: Verify Horse Name
        EXPECTED: Horse Name corresponds to the "name" attribute.
        """
        pass

    def test_005_verifyhorseman_name(self):
        """
        DESCRIPTION: Verify Horseman Name
        EXPECTED: Horse Name corresponds to the "jockey" attribute.
        """
        pass
