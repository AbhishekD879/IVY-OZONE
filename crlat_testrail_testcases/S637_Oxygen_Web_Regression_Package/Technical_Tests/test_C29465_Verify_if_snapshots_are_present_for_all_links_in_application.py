import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29465_Verify_if_snapshots_are_present_for_all_links_in_application(Common):
    """
    TR_ID: C29465
    NAME: Verify if snapshots are present for all links in application
    DESCRIPTION: Test case is verifys snapshots presence for all links in application
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-9277: SEO - Microservice implementation (Core functionality)
    DESCRIPTION: BMA-9311: SEO - Microservice implementation (Crawler)
    DESCRIPTION: BMA-9312: SEO - Microservice implementation (Caching pages)
    PRECONDITIONS: Use bm-tst2.coral.co.uk/snapshots-dev/  link for checking of snapshots presence.
    PRECONDITIONS: For example, check presence of snapshots for football page:
    PRECONDITIONS: https://bm-tst2.coral.co.uk/snapshots-dev/**football **
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_openbm_tst2coralcouksnapshots_dev_link(self):
        """
        DESCRIPTION: Open bm-tst2.coral.co.uk/snapshots-dev/ *link*
        EXPECTED: 
        """
        pass

    def test_003_enter_name_of_the_page_for_which_you_want_to_verify_presence_of_snapshot_in_the_end_of_url_from_step_2for_examplehttpsbm_tst2coralcouksnapshots_devpromotionshttpsbm_tst2coralcouksnapshots_devtennisevent4073101httpsbm_tst2coralcouksnapshots_devtennisevent4073101tiebreak_markets(self):
        """
        DESCRIPTION: Enter name of the page for which you want to verify presence of snapshot in the end of url from step 2.
        DESCRIPTION: For example:
        DESCRIPTION: https://bm-tst2.coral.co.uk/snapshots-dev/promotions
        DESCRIPTION: https://bm-tst2.coral.co.uk/snapshots-dev/tennis/event/4073101
        DESCRIPTION: https://bm-tst2.coral.co.uk/snapshots-dev/tennis/event/4073101/tiebreak-markets
        EXPECTED: Snapshot is present
        """
        pass

    def test_004_check_presense_of_snapshots_for_all_links_in_application(self):
        """
        DESCRIPTION: Check presense of snapshots for all links in application
        EXPECTED: Snapshots are present
        """
        pass
