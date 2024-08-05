package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.google.gson.Gson;
import java.util.ArrayList;
import java.util.List;

public class DefaultMarketSelector extends AbstractMultipleMarketSelector {

  public DefaultMarketSelector(String[] marketNamesToKeep, Gson gson) {
    super(marketNamesToKeep, gson);
  }

  @Override
  public List<SportSegment> extract(SportSegment sportSegment) {
    List<SportSegment> result = new ArrayList<>(1);
    SportSegment clone = getCloneWithFilteredMarkets(sportSegment);
    clone = updateEventIdsAndCount(clone);
    result.add(clone);
    return result;
  }

  @Override
  protected String selectorName() {
    return null; // default market selector doesn't have name
  }
}
