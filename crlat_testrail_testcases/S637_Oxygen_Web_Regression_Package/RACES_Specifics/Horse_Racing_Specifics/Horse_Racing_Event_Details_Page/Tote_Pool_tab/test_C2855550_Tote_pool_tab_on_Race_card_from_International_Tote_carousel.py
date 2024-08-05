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
class Test_C2855550_Tote_pool_tab_on_Race_card_from_International_Tote_carousel(Common):
    """
    TR_ID: C2855550
    NAME: Tote pool tab on Race card from International Tote carousel
    DESCRIPTION: Test case verifies that Race card with selected totepool tab is opened when user taps on event from International Tote races carousel
    PRECONDITIONS: International Tote Races Carousel is present
    PRECONDITIONS: **Instruction on Tote events mapping on test environment**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: **Request to retrieve events to be shown in the International Tote carousel:**
    PRECONDITIONS: EventToMarketForClass/16288
    PRECONDITIONS: **Request from pool types on EDP**
    PRECONDITIONS: PoolForEvent/event_id
    PRECONDITIONS: **User is on Horse racing landing page.**
    """
    keep_browser_open = True

    def test_001_tap_on_the_event_from_the_international_tote_carousel(self):
        """
        DESCRIPTION: Tap on the event from the International tote carousel
        EXPECTED: - Event card is opened
        EXPECTED: - Totepool tab is selected
        """
        pass

    def test_002_verify_content_of_totepool_tab(self):
        """
        DESCRIPTION: Verify content of Totepool tab
        EXPECTED: - Supported pool types (from request PoolForEvent) are displayed
        EXPECTED: - The first available pool type (commonly, Win) is selected
        """
        pass

    def test_003_verify_url_path(self):
        """
        DESCRIPTION: Verify url path
        EXPECTED: Path contains /{event_id}/totepool/{pool type}
        """
        pass
