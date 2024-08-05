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
class Test_C2745933_To_update_Verify_behavior_of_Finished_Races_in_International_Tote_Races_Carousel(Common):
    """
    TR_ID: C2745933
    NAME: [To update] Verify behavior of Finished Races in International Tote Races Carousel
    DESCRIPTION: This test case verifies behavior of Finished Races in International Tote Races Carousel
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: To check whether event **is finished/resulted** use request URL:
    PRECONDITIONS: /EventToOutcomeForEvent/{event_id}?simpleFilter=event.suspendAtTime
    PRECONDITIONS: International Tote Races are available.
    PRECONDITIONS: International Tote Races Carousel is present below UK Races
    PRECONDITIONS: **From OX 106**
    PRECONDITIONS: To get the 'International Tote Carousel' events check modules (modules name can be changed in CMS) in 'FEATURED_STRUCTURE_CHANGED' request from web-socket (wss://featured-sports)
    PRECONDITIONS: Example of event structure:
    PRECONDITIONS: [{
    PRECONDITIONS: data: [{
    PRECONDITIONS: id: "230549330",
    PRECONDITIONS: categoryId: "21",
    PRECONDITIONS: categoryName: "Horse Racing",
    PRECONDITIONS: className: "Horse Racing - Tote",
    PRECONDITIONS: typeName: "Southwell",
    PRECONDITIONS: name: "Southwell",
    PRECONDITIONS: startTime: 1212321345,
    PRECONDITIONS: isResulted: false,
    PRECONDITIONS: localTime: "15:40",
    PRECONDITIONS: externalKeys: {
    PRECONDITIONS: OBEvLinkNonTote: 230658078
    PRECONDITIONS: }
    PRECONDITIONS: }]
    PRECONDITIONS: }]
    PRECONDITIONS: The display order and enable/disable feature of 'International Tote Carousel' module can be set here:
    PRECONDITIONS: CMS/Sports Pages/Sport Categories/Horse Racing
    PRECONDITIONS: ***User is on Horse racing landing page.***
    """
    keep_browser_open = True

    def test_001_tap_on_any_of_the_finished_races_event_with_attributes_isfinishedtrue_and_isresulted__true(self):
        """
        DESCRIPTION: Tap on any of the Finished Races (event with attributes **isFinished='true'** and **isResulted = 'true'**))
        EXPECTED: For Coral:
        EXPECTED: - User should go to the Results Page of that respective Race
        EXPECTED: - 'Results' Tab should be selected
        EXPECTED: - 'By Latest Results' subtab should be selected and content is loaded
        EXPECTED: For Ladbrokes:
        EXPECTED: - User is navigated to the page that displays result info about the race:
        EXPECTED: ![](index.php?/attachments/get/38750)
        """
        pass
