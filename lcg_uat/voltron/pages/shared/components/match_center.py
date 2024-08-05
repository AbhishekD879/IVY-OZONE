from voltron.pages.shared.components.primitives.buttons import FavouritesIcon
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.waiters import wait_for_result


class MatchCenter(ComponentBase):
    """
    Match Center functionality on the displayed Bet Receipt
    """
    _add_all_to_favourites_button = 'xpath=.//*[@data-crlat="favouriteIcon"]'

    def has_add_all_to_favourites_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._add_all_to_favourites_button, context=self._we,
                                                   timeout=0.2) is not None,
            name=f'Label status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def add_all_to_favourites_button(self):
        return FavouritesIcon(selector=self._add_all_to_favourites_button, context=self._we, timeout=2)
