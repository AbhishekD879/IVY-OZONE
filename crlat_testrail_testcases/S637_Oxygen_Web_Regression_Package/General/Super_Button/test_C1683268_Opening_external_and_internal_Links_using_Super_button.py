import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.navigation
@vtest
class Test_C1683268_Opening_external_and_internal_Links_using_Super_button(Common):
    """
    TR_ID: C1683268
    NAME: Opening external and internal Links using Super button
    DESCRIPTION: This test case verifies that tapping on Super button can open internal/external links set in CMS
    PRECONDITIONS: Two Super buttons should be added and enabled in CMS
    PRECONDITIONS: https://{domain}/sports-pages/homepage
    PRECONDITIONS: where domain may be
    PRECONDITIONS: coral-cms-dev1.symphony-solutions.eu - Local env
    PRECONDITIONS: coral-cms-dev0.symphony-solutions.eu - Develop
    """
    keep_browser_open = True

    def test_001_load_cms_and_log_in(self):
        """
        DESCRIPTION: Load CMS and log in
        EXPECTED: * CMS is loaded
        EXPECTED: * Content manager is logged in
        """
        pass

    def test_002_go_to_sports_pages__super_button__open_existing_super_button(self):
        """
        DESCRIPTION: Go to Sports Pages > Super Button > open existing Super button
        EXPECTED: Super button details page is opened
        """
        pass

    def test_003_go_to_destination_url_option_set_the_internal_link_eg_big_competitionworld_cupfeatured_and_save_changes(self):
        """
        DESCRIPTION: Go to 'Destination URL' option, set the internal link (e.g. /big-competition/world-cup/featured) and save changes
        EXPECTED: * 'Destination URL' option is set with internal link
        EXPECTED: * Changes is saved successfully
        """
        pass

    def test_004_load_oxygen_app_go_to_super_button_and_tap_on_it(self):
        """
        DESCRIPTION: Load Oxygen app, go to Super button and tap on it
        EXPECTED: User navigates to URL set on step #3 in existing browser tab
        """
        pass

    def test_005_go_to_cms_set_external_link_in_destination_url_option_eg_httpresponsiblegamblingcoralcouk_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set external link in 'Destination URL' option (e.g http://responsiblegambling.coral.co.uk) and save changes
        EXPECTED: * 'Destination URL' option is set with external link
        EXPECTED: * Changes is saved successfully
        """
        pass

    def test_006_repeat_step_4(self):
        """
        DESCRIPTION: Repeat step #4
        EXPECTED: User navigates to URL set on step #5 in a new browser tab
        """
        pass

    def test_007_go_to_cms_set_not_existing_link_in_destination_url_option_eg_test_and_save_changes(self):
        """
        DESCRIPTION: Go to CMS, set not existing link in 'Destination URL' option (e.g. /test) and save changes
        EXPECTED: * 'Destination URL' option is set with not existing link
        EXPECTED: * Changes is saved successfully
        """
        pass

    def test_008_load_oxygen_app_go_to_super_button_and_tap_on_it(self):
        """
        DESCRIPTION: Load Oxygen app, go to Super button and tap on it
        EXPECTED: * User navigates on Homepage
        EXPECTED: * App is NOT crashed, no errors appear
        """
        pass
