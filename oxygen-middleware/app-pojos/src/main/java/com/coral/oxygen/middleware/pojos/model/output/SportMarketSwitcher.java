package com.coral.oxygen.middleware.pojos.model.output;

import java.util.List;
import lombok.Data;

@Data
public class SportMarketSwitcher {
  private Sport sport;
  private List<MarketSwitcherSelection> marketSwitcherSelections;
}
