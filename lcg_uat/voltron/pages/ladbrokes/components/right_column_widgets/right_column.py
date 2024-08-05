from voltron.pages.shared.components.right_column_widgets.favourites_widget_section import FavoritesWidgetSection
from voltron.pages.shared.components.right_column_widgets.in_play_widget import InPlayWidget
from voltron.pages.ladbrokes.components.right_column_widgets.mini_games_widget import LadbrokesMiniGamesWidget
from voltron.pages.shared.components.right_column_widgets.next_races_widget import NextRacesWidget
from voltron.pages.shared.components.right_column_widgets.offers_widget_section import OffersWidgetSection
from voltron.pages.shared.components.right_column_widgets.right_column import RightColumn
from voltron.pages.shared.contents.betslip.betslip_desktop import BetSlipDesktop


class LadbrokesRightColumn(RightColumn):
    widget_attributes = {'widgetAccordion.betslip': BetSlipDesktop,
                         'widgetAccordion.favourites': FavoritesWidgetSection,
                         'widgetAccordion.offers': OffersWidgetSection,
                         'widgetAccordion.mini-games': LadbrokesMiniGamesWidget,
                         'widgetAccordion.in-play': InPlayWidget,
                         'widgetAccordion.next-races': NextRacesWidget}
