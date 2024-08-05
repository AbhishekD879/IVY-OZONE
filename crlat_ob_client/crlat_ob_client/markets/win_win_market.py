from .base_market import BaseMarketEntity


class WinWinMarket(BaseMarketEntity):

    def __init__(self, **kwargs):
        super(WinWinMarket, self).__init__(**kwargs)
        prices = kwargs.get('prices', {})
        self.home_price = prices.get('odds_home')
        self.away_price = prices.get('odds_away')
        self.home_disporder = self.market_disporder
        self.away_disporder = self.market_disporder
        self.market_display_sort_code = 'HH'

    def _generate_params(self):
        return ((f'name_{self.market_template_id}_{self.market_display_sort_code}', self.market_name),
                ('ev_oc_grp_id', self.market_template_id),
                ('ev_oc_grp_id_sort', f'{self.market_template_id}_{self.market_display_sort_code}'),
                (f'name_{self.market_template_id}_{self.market_display_sort_code}_disporder', self.market_disporder),
                (f'ha_home_{self.market_template_id}_{self.market_display_sort_code}', self.home_price),
                (f'ha_home_{self.market_template_id}_{self.market_display_sort_code}_disporder', self.home_disporder),
                (f'ha_away_{self.market_template_id}_{self.market_display_sort_code}', self.away_price),
                (f'ha_away_{self.market_template_id}_{self.market_display_sort_code}_disporder', self.away_disporder))
