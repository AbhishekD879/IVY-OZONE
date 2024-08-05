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
class Test_C58669266_OX1021_Verify_Markets_provided_from_Playtech(Common):
    """
    TR_ID: C58669266
    NAME: (OX102.1) Verify Markets provided from Playtech
    DESCRIPTION: This test case verifies events Markets provided from Playtech
    PRECONDITIONS: Get SiteServer response to verify data:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/x.xx/EventToOutcomeForClass/285?simpleFilter=class.categoryId:equals:39&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: x.xx - current supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: 1. Open Coral/Ladbrokes test environment
    PRECONDITIONS: 2. Go to 'Virtual Sports'
    """
    keep_browser_open = True

    def test_001_select_football_virtual_sports_page(self):
        """
        DESCRIPTION: Select **Football** Virtual sports page
        EXPECTED: Markets should be provided from OB and present on UI:
        EXPECTED: ![](index.php?/attachments/get/105775825)
        EXPECTED: Ladbrokes Tst2:
        EXPECTED: Sport Class - 35073
        EXPECTED: Sport Type - 97500
        EXPECTED: Coral Tst2:
        EXPECTED: Sport Class - 35088
        EXPECTED: Sport Type - 97422
        """
        pass

    def test_002_select_horse_racing_virtual_sports_page(self):
        """
        DESCRIPTION: Select **Horse Racing** Virtual sports page
        EXPECTED: Markets should be provided from OB and present on UI:
        EXPECTED: ![](index.php?/attachments/get/105775829)
        EXPECTED: Ladbrokes Tst2:
        EXPECTED: Sport Class - 35074
        EXPECTED: Sport Type - 97503
        EXPECTED: Coral Tst2:
        EXPECTED: Sport Class - 35087
        EXPECTED: Sport Type - 97421
        """
        pass

    def test_003_select_greyhounds_virtual_sports_page(self):
        """
        DESCRIPTION: Select **Greyhounds** Virtual sports page
        EXPECTED: Markets should be provided from OB and present on UI:
        EXPECTED: ![](index.php?/attachments/get/105775828)
        EXPECTED: Ladbrokes Tst2:
        EXPECTED: Sport Class - 35082
        EXPECTED: Sport Type - 97520
        EXPECTED: Coral Tst2:
        EXPECTED: Sport Class - 35095
        EXPECTED: Sport Type - 97443
        """
        pass

    def test_004_select_basketball_virtual_sports_page(self):
        """
        DESCRIPTION: Select **Basketball** Virtual sports page
        EXPECTED: Markets should be provided from OB and present on UI:
        EXPECTED: ![](index.php?/attachments/get/105775827)
        EXPECTED: Ladbrokes Tst2:
        EXPECTED: Sport Class - 35083
        EXPECTED: Sport Type - 97521
        EXPECTED: Coral Tst2:
        EXPECTED: Sport Class - 35098
        EXPECTED: Sport Type - 102901
        """
        pass
