import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C2912066_Verify_Race_Card_when_race_starts_on_Win_Place_Exacta_Trifecta_tab(Common):
    """
    TR_ID: C2912066
    NAME: Verify Race Card when race starts on Win/Place/Exacta/Trifecta tab
    DESCRIPTION: This test case verifies Race Card when race starts on Win/Place/Exacta/Trifecta tab
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **Request on EDP**: PoolForEvent/ {event_id} ?&translationLang=en
    PRECONDITIONS: International Tote Races with tote pool are available
    PRECONDITIONS: **User is on Int Horse Race EDP and Win/Place/Exacta/Trifecta pool is selected**
    """
    keep_browser_open = True

    def test_001_while_user_is_viewing_the_winplaceexactatrifecta_tab_go_to_ob_office_and_mark_isoff__yes_and_status___suspend_for_event(self):
        """
        DESCRIPTION: While user is viewing the Win/Place/Exacta/Trifecta tab, go to OB office, and mark **isOff = Yes** and **Status - Suspend** for event
        EXPECTED: - Page is greyed out as suspended on app
        EXPECTED: - All check boxes become disabled in real time
        """
        pass

    def test_002_go_back_to_ob_office_and_mark_isoff__no_and_status___active_for_event(self):
        """
        DESCRIPTION: Go back to OB office, and mark **isOff = No** and **Status - Active** for event
        EXPECTED: - Page becomes available on app
        EXPECTED: - All check boxes become active in real time
        """
        pass
