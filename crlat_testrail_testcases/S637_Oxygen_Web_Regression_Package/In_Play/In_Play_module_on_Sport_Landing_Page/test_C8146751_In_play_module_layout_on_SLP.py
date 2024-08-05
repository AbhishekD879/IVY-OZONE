import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C8146751_In_play_module_layout_on_SLP(Common):
    """
    TR_ID: C8146751
    NAME: 'In-play' module layout on SLP
    DESCRIPTION: This test case verifies 'In-play' module layout on <Sport> Landing Page
    PRECONDITIONS: 1) CMS config:
    PRECONDITIONS: * 'In-Play' module is enabled in CMS > System Configuration > Structure > Inplay Module
    PRECONDITIONS: * 'In-Play' module is created in CMS > Sports Pages > Sport Categories > specific sport e.g. Football
    PRECONDITIONS: * 'In-play' module is set to 'Active'
    PRECONDITIONS: * 'Inplay event count' within 'In-play' module is set to any digit e.g. 10
    PRECONDITIONS: 2) In-play events should be present for selected sport e.g. Football
    PRECONDITIONS: Load the app and navigate to <Sport> Landing page under test e.g. Football
    PRECONDITIONS: Open 'Matches' tab
    """
    keep_browser_open = True

    def test_001_verify_in_play_module_layout(self):
        """
        DESCRIPTION: Verify 'In-Play' module layout
        EXPECTED: 'In-Play' module consists of:
        EXPECTED: * In-Play header
        EXPECTED: * Type containers
        EXPECTED: * Event cards
        """
        pass

    def test_002_verify_in_play_module_header(self):
        """
        DESCRIPTION: Verify 'In-Play' module header
        EXPECTED: 'In-Play' module header contains:
        EXPECTED: * 'In-Play' text
        EXPECTED: * 'See all (XX)>' link
        """
        pass

    def test_003_verify_type_containers(self):
        """
        DESCRIPTION: Verify type containers
        EXPECTED: * Events are grouped by TypeID
        EXPECTED: * TypeName is displayed and corresponds to 'typeName' attribute
        EXPECTED: * Home/Draw/Away or 1/2 (depending on 3 or 2 way primary market) displayed
        """
        pass

    def test_004_verify_event_card_elements(self):
        """
        DESCRIPTION: Verify event card elements
        EXPECTED: * Team names/players names
        EXPECTED: * Live/Watch live icons (if available)
        EXPECTED: * Scores (if available)
        EXPECTED: * Match time (if available)
        EXPECTED: * Fav icon (Football only)(Coral only)
        EXPECTED: * Price/odds buttons
        EXPECTED: * 'XX more' link (above Price/odds buttons for Ladbrokes) (below Price/odds buttons for Coral)
        """
        pass
