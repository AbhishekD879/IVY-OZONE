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
class Test_C2745929_Verify_behavior_of_Meeting_time_in_International_Tote_Races_Carousel(Common):
    """
    TR_ID: C2745929
    NAME: Verify behavior of Meeting time in International Tote Races Carousel
    DESCRIPTION: This test case verifies behavior of Meeting time in International Tote Races Carousel
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: System configuration > Structure: InternationalTotePoolRaceCard is enabled
    PRECONDITIONS: ** Check the correctness of the response - https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventForClass/802?simpleFilter=event.startTime:greaterThanOrEqual:2020-06-18T21:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-06-19T21:00:00.000Z&externalKeys=event&translationLang=en&responseFormat=json
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

    def test_001_tap_on_any_of_the_meeting_time_which_is_not_finished_(self):
        """
        DESCRIPTION: Tap on any of the Meeting time (which is not finished )
        EXPECTED: - User should go to the Race card of respective Meeting
        EXPECTED: - Meeting time is selected
        EXPECTED: - 'Tote Pool' Tab should be selected
        EXPECTED: - First default pool should be selected and content is loaded
        """
        pass
