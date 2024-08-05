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
class Test_C2727621_Verify_International_Tote_Races_Carousel(Common):
    """
    TR_ID: C2727621
    NAME: Verify International Tote Races Carousel
    DESCRIPTION: This test case verifies International Tote Races Carousel
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: International Tote Races are available.
    PRECONDITIONS: International Tote Races Carousel is present below UK Races
    PRECONDITIONS: To get all available 'Events' on HR Landing page use the link:
    PRECONDITIONS: EventToMarketForEvent/{event-id1},{event-id2}
    PRECONDITIONS: ** Check the correctness of the response - https://ss-aka-ori.ladbrokes.com/openbet-ssviewer/Drilldown/2.31/EventForClass/802?simpleFilter=event.startTime:greaterThanOrEqual:2020-06-18T21:00:00.000Z&simpleFilter=event.startTime:lessThan:2020-06-19T21:00:00.000Z&externalKeys=event&translationLang=en&responseFormat=json
    PRECONDITIONS: **Note:** NOT showing International Tote Races Carousel when NO Tote races are available
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

    def test_001_verify_content_of_international_tote_races_carousel(self):
        """
        DESCRIPTION: Verify content of International Tote Races Carousel
        EXPECTED: International Tote Races Carousel should contain:
        EXPECTED: - Text "TOTE EVENTS" (for Ladbrokes)
        EXPECTED: - Meeting Timing
        EXPECTED: - Meeting Venue should be shown as abbreviation (extracted value **typeName** from response **EventToMarketForEvent**):
        EXPECTED: ** If Meeting Venue is more than 5 characters it should be truncated to 5 characters. e.g. Gulfstream - Gulfs
        EXPECTED: ** If it is equal to or less than 5 characters then show 5 letters or 4 letters in abbreviations. e.g. Vaal - Vaal
        """
        pass

    def test_002_verify_order_of_meetings(self):
        """
        DESCRIPTION: Verify order of Meetings
        EXPECTED: - Events are ordered by Meeting time
        EXPECTED: - Finished Races should shown in Meeting time order on the left side before unfinished ones.
        EXPECTED: - Unfinished Meetings should be shown in order after finished Races.
        EXPECTED: - if Meeting times are same for 2 or more meetings than it should be shown as per OB event ID order
        EXPECTED: **Ladbrokes**: Race Statuses displayed for started or resulted events under Meeting Venue abbreviation:
        EXPECTED: Race Off - event has 'isOff=Yes'
        EXPECTED: Live - event has 'isOff=Yes'and at least one of markets has 'betInRunning=true'
        EXPECTED: Resulted - event has 'isResulted=true' + 'isFinished=true'
        """
        pass

    def test_003_verify_ability_to_swipe_the_carousel_right_to_left_and_vice_versa(self):
        """
        DESCRIPTION: Verify ability to swipe the carousel right to left and vice versa
        EXPECTED: User should be able to move the carousel right to left and vice versa
        """
        pass
