package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.google.gson.Gson;

/** Created by Aliaksei Yarotski on 4/26/18. */
public class PrimaryMarketSelector extends DefaultMarketSelector {

  private static final String MAIN_MARKET = "Main Market";

  public PrimaryMarketSelector(String[] marketNamesToKeep, Gson gson) {
    super(marketNamesToKeep, gson);
  }

  @Override
  protected String selectorName() {
    return MAIN_MARKET;
  }
}
