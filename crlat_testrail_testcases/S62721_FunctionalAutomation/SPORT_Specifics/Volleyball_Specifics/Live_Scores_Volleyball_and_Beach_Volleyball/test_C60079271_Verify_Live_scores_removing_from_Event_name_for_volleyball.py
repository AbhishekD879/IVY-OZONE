import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C60079271_Verify_Live_scores_removing_from_Event_name_for_volleyball(Common):
    """
    TR_ID: C60079271
    NAME: Verify Live scores removing from Event name for volleyball
    DESCRIPTION: This test case verifies BIP scores in Event Name are replaced to ''v''  for Volleyball events on Front End
    PRECONDITIONS: 1. In order to get events with Scorers use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Commentary/X.XX/CommentaryForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. EN, Ukr)
    PRECONDITIONS: 2. OB tool:
    PRECONDITIONS: https://confluence.egalacoral.com/display/MOB/Open+Bet+Systems
    PRECONDITIONS: 3. Go to OB and create Volleyball live event with name:
    PRECONDITIONS: |Team A Name| (SetsA) PointsInCurrentSetA-PointsInCurrentSetB (SetsB) |Team B Name
    """
    keep_browser_open = True

    def test_001_go_to_oxygen_and_check_event_name_displaying_on_pages_in_play_pagetabwidget__all_sports_filter_and__volleyball_sports_filter(self):
        """
        DESCRIPTION: Go to Oxygen and check event name displaying on pages:
        DESCRIPTION: * In Play page/tab/widget ( all sports filter and  volleyball sports filter)
        EXPECTED: Event name should be:
        EXPECTED: Volero Zurich Women v CS Volei Alba Blaj Women (BG)
        EXPECTED: ''(2) 12-5 (0)'' should be replaced on ''v'' on Event Details Page
        """
        pass

    def test_002__live_stream_pagewidget__if_live_stream_is_available_for_event(self):
        """
        DESCRIPTION: * Live Stream page/widget ( if live stream is available for event)
        EXPECTED: vent name should be:
        EXPECTED: Volero Zurich Women v CS Volei Alba Blaj Women (BG)
        EXPECTED: ''(2) 12-5 (0)'' should be replaced on ''v''
        """
        pass

    def test_003__betslip_sliderwidget_adding_via_deep_link_too(self):
        """
        DESCRIPTION: * Betslip slider/widget (adding via deep link too)
        EXPECTED: vent name should be:
        EXPECTED: Volero Zurich Women v CS Volei Alba Blaj Women (BG)
        EXPECTED: ''(2) 12-5 (0)'' should be replaced on ''v''
        """
        pass

    def test_004__cash_out(self):
        """
        DESCRIPTION: * Cash Out
        EXPECTED: vent name should be:
        EXPECTED: Volero Zurich Women v CS Volei Alba Blaj Women (BG)
        EXPECTED: ''(2) 12-5 (0)'' should be replaced on ''v''
        """
        pass

    def test_005__bet_historyopen_bets(self):
        """
        DESCRIPTION: * Bet History/Open bets
        EXPECTED: vent name should be:
        EXPECTED: Volero Zurich Women v CS Volei Alba Blaj Women (BG)
        EXPECTED: ''(2) 12-5 (0)'' should be replaced on ''v''
        """
        pass

    def test_006__featured__created_by_type_id_selection_id(self):
        """
        DESCRIPTION: * Featured ( created by type id, selection id)
        EXPECTED: vent name should be:
        EXPECTED: Volero Zurich Women v CS Volei Alba Blaj Women (BG)
        EXPECTED: ''(2) 12-5 (0)'' should be replaced on ''v''
        """
        pass
