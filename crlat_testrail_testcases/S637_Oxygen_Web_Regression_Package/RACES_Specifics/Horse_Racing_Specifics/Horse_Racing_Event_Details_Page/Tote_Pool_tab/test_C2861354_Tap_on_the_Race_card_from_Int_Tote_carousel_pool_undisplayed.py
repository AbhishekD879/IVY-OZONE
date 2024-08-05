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
class Test_C2861354_Tap_on_the_Race_card_from_Int_Tote_carousel_pool_undisplayed(Common):
    """
    TR_ID: C2861354
    NAME: Tap on the Race card from Int Tote carousel (pool undisplayed)
    DESCRIPTION: Test case verifies the behavior of the tote pool when user taps on the event link and the updates about pool undisplay are not received yet
    PRECONDITIONS: International Tote Races Carousel is present
    PRECONDITIONS: **Instruction on International Tote events mapping**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/How+to+link+International+Tote+events+with+Regular+Horse+Racing+events
    PRECONDITIONS: **To undisplay  pool in OB office:**
    PRECONDITIONS: Betting Setup > Pools > Select pool > Set Displayed - No
    PRECONDITIONS: **CMS configuration**
    PRECONDITIONS: System configuration > Structure: InternationalTotePool is enabled
    PRECONDITIONS: **Request to retrieve events to be shown in the International Tote carousel:**
    PRECONDITIONS: EventToMarketForClass/16288
    PRECONDITIONS: where class - Horse Racing - Intl Thoroughbred Pools
    PRECONDITIONS: **Request from pool types on EDP**
    PRECONDITIONS: PoolForEvent/event_id
    PRECONDITIONS: **User is on Horse racing landing page.**
    """
    keep_browser_open = True

    def test_001_while_user_stays_on_the_hr_landing_page_go_to_ob_office_and_undisplay_the_pool_first_default_pool_for_the_event_to_be_opened(self):
        """
        DESCRIPTION: While user stays on the HR landing page, go to OB office, and undisplay the pool (first default pool for the event to be opened)
        EXPECTED: Pool undisplayed in OB office
        """
        pass

    def test_002_tap_on_the_event_from_int_tote_carousel(self):
        """
        DESCRIPTION: Tap on the event from Int Tote carousel
        EXPECTED: - Event Race card should be opened
        EXPECTED: - Undisplayed pool should not be present
        EXPECTED: - First available pool type should be selected
        """
        pass

    def test_003_verify_url_path(self):
        """
        DESCRIPTION: Verify url path
        EXPECTED: Path contains /{event_id}/totepool/{actual selected pool type}
        """
        pass
