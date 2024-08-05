import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C12561661_Verify_user_navigation_from_Featured_tab_to_CMS_configured_hardcoded_pages_in_application(Common):
    """
    TR_ID: C12561661
    NAME: Verify user navigation from Featured tab to CMS configured/hardcoded pages in application
    DESCRIPTION: This test case verifies user navigation from Featured tab to CMS configured page in application
    PRECONDITIONS: 1. Featured modules by Sport/race type id are configured in CMS
    PRECONDITIONS: 2. For these Featured modules internal links  are configured in 'CMS in Footer link URL field'
    """
    keep_browser_open = True

    def test_001_select_featured_module_by_sport_type_idtap_cms_configurable_link_at_the_bottom_of_the_moduleverify_users_navigation_to_appropriate_page_configured_in_cms_for_selected_module(self):
        """
        DESCRIPTION: Select Featured module by Sport type ID.
        DESCRIPTION: Tap CMS configurable link at the bottom of the module.
        DESCRIPTION: Verify user's navigation to appropriate page configured in CMS for selected module
        EXPECTED: User is navigated to the page configured in CMS for selected module
        """
        pass

    def test_002_select_featured_module_by_sport_type_idtap_hardcoded_link_with_number_of_available_markets_for_selected_event_within_the_moduleverify_that_user_is_navigated_to_selected_event_details_page(self):
        """
        DESCRIPTION: Select Featured module by Sport type ID.
        DESCRIPTION: Tap hardcoded link with number of available markets for selected event within the module.
        DESCRIPTION: Verify that user is navigated to selected event details page
        EXPECTED: User is navigated to selected event details page
        """
        pass

    def test_003_select_featured_module_by_race_type_idtap_cms_configurable_link_at_the_bottom_of_the_moduleverify_users_navigation_to_appropriate_page_configured_in_cms_for_selected_module(self):
        """
        DESCRIPTION: Select Featured module by Race type ID.
        DESCRIPTION: Tap CMS configurable link at the bottom of the module.
        DESCRIPTION: Verify user's navigation to appropriate page configured in CMS for selected module
        EXPECTED: User is navigated to the page configured in CMS for selected module
        """
        pass

    def test_004_select_featured_module_by_race_type_idtap_hardcoded_link_more_with_number_of_available_markets_for_selected_event_within_the_module_headerverify_that_user_is_navigated_to_selected_event_details_page(self):
        """
        DESCRIPTION: Select Featured module by Race type ID.
        DESCRIPTION: Tap hardcoded link 'More' with number of available markets for selected event within the module header.
        DESCRIPTION: Verify that user is navigated to selected event details page
        EXPECTED: User is navigated to selected event details page
        """
        pass
