package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.google.gson.Gson;

/** Created by azayats on 24.05.17. */
public class TemplateNameRawHandicapValueMarketSelector extends AbstractMarketSelector {

  private final String templateMarketName;

  private final double rawHandicapValue;

  public TemplateNameRawHandicapValueMarketSelector(
      String templateMarketName, double rawHandicapValue, Gson gson) {
    super(gson);
    this.templateMarketName = templateMarketName;
    this.rawHandicapValue = rawHandicapValue;
  }

  @Override
  protected boolean acceptMarket(OutputMarket market) {
    return market.getRawHandicapValue() != null
        && templateMarketName.equalsIgnoreCase(market.getTemplateMarketName())
        && Math.abs(rawHandicapValue - market.getRawHandicapValue()) < 0.01;
  }

  @Override
  protected String selectorName() {
    return String.format("%s %2.1f", templateMarketName, rawHandicapValue);
  }
}
