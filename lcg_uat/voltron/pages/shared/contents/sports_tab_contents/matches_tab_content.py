from collections import OrderedDict

from voltron.pages.shared.components.home_page_components.highlight_carousel import HighlightCarousel
from voltron.pages.shared.components.in_play_module import InPlayModule
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.utils.waiters import wait_for_result


class MatchesTabContent(TabContent):
    _verify_spinner = True


