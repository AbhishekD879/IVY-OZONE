import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C2635877_No_Enhanced_Multiples(Common):
    """
    TR_ID: C2635877
    NAME: No Enhanced Multiples
    DESCRIPTION: This test case verifies absence of Enhanced Multiples carousel in case there are no Enhanced Multiples
    PRECONDITIONS: No Enhanced Multiples for <Sport>
    """
    keep_browser_open = True

    def test_001_open_sport_landing_page(self):
        """
        DESCRIPTION: Open <Sport> Landing page
        EXPECTED: 
        """
        pass

    def test_002_verify_enhanced_multiples_carousel(self):
        """
        DESCRIPTION: Verify Enhanced Multiples carousel
        EXPECTED: * Enhanced Multiples carousel is NOT displayed at all in case if there are no available Enhanced Multiples events for the <Sport>
        EXPECTED: * There is no empty space, the rest of content it displayed properly
        """
        pass
