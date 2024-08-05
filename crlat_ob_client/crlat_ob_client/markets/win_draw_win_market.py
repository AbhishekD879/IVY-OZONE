from .base_market import BaseMarketEntity


class WinDrawWinMarket(BaseMarketEntity):

    def __init__(self, **kwargs):
        super(WinDrawWinMarket, self).__init__(**kwargs)
        prices = kwargs.get('prices', {})
        self.home_price = prices.get('odds_home')
        self.draw_price = prices.get('odds_draw')
        self.away_price = prices.get('odds_away')
        self.home_disporder = self.market_disporder
        self.draw_disporder = self.market_disporder
        self.away_disporder = self.market_disporder
        self.market_display_sort_code = 'MR'

    def _generate_params(self):
        return ((f'name_{self.market_template_id}_{self.market_display_sort_code}', self.market_name),
                ('ev_oc_grp_id', self.market_template_id),
                ('ev_oc_grp_id_sort', f'{self.market_template_id}_{self.market_display_sort_code}'),
                (f'name_{self.market_template_id}_{self.market_display_sort_code}_disporder', self.market_disporder),
                (f'hd_home_{self.market_template_id}_{self.market_display_sort_code}', self.home_price),
                (f'hd_home_{self.market_template_id}_{self.market_display_sort_code}_disporder', self.home_disporder),
                (f'hd_draw_{self.market_template_id}_{self.market_display_sort_code}', self.draw_price),
                (f'hd_draw_{self.market_template_id}_{self.market_display_sort_code}_disporder', self.draw_disporder),
                (f'hd_away_{self.market_template_id}_{self.market_display_sort_code}', self.away_price),
                (f'hd_away_{self.market_template_id}_{self.market_display_sort_code}_disporder', self.away_disporder))
