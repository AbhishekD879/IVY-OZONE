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
class Test_C64055793_GALAXY_S9_In_play_module_layout_on_SLP(Common):
    """
    TR_ID: C64055793
    NAME: [GALAXY S9] 'In-play' module layout on SLP
    DESCRIPTION: 
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001__test_000_preconditions(self):
        """
        DESCRIPTION: * test_000_preconditions
        EXPECTED: *
        """
        pass

    def test_002___________verify_in_play_module_layout(self):
        """
        DESCRIPTION: *          Verify 'In-Play' module layout
        EXPECTED: *          'In-Play' module consists of:
        EXPECTED: *          * In-Play header
        EXPECTED: *          * Type containers
        EXPECTED: *          * Event cards
        """
        pass

    def test_003___________verify_in_play_module_header(self):
        """
        DESCRIPTION: *          Verify 'In-Play' module header
        EXPECTED: *          'In-Play' module header contains:
        EXPECTED: *          * 'In-Play' text
        EXPECTED: *          * 'See all (XX)>' link
        """
        pass

    def test_004___________verify_type_containers(self):
        """
        DESCRIPTION: *          Verify type containers
        EXPECTED: *          * Events are grouped by TypeID
        EXPECTED: *          * TypeName is displayed and corresponds to 'typeName' attribute
        EXPECTED: *          * Home/Draw/Away or 1/2 (depending on 3 or 2 way primary market) displayed
        """
        pass

    def test_005___________verify_event_card_elements(self):
        """
        DESCRIPTION: *          Verify event card elements
        EXPECTED: *          * Team names/players names
        EXPECTED: *          * Live/Watch live icons (if available)
        EXPECTED: *          * Scores (if available)
        EXPECTED: *          * Match time (if available)
        EXPECTED: *          * Fav icon (Football only)
        EXPECTED: *          * Price/odds buttons
        EXPECTED: *          * 'XX more' link
        """
        pass
