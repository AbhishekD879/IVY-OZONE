package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.google.gson.Gson;
import org.springframework.util.Assert;

public class MultipleNameMarketSelector extends AbstractMultipleMarketSelector {

  private String templateMarketName;

  public MultipleNameMarketSelector(String[] marketNamesToKeep, Gson gson) {
    super(marketNamesToKeep, gson);
    Assert.notEmpty(marketNamesToKeep, "marketNamesToKeep should not be empty.");
    templateMarketName = marketNamesToKeep[0];
  }

  @Override
  protected String selectorName() {
    return templateMarketName;
  }
}
