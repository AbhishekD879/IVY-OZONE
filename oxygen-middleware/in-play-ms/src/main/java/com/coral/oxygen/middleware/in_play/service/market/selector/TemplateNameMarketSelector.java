package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.google.gson.Gson;
import java.util.Objects;

/** Created by azayats on 23.05.17. */
public class TemplateNameMarketSelector extends AbstractMultipleMarketSelector {

  private String templateMarketName;

  public TemplateNameMarketSelector(String[] marketTemplateNames, Gson gson) {
    super(marketTemplateNames, gson);
    Objects.requireNonNull(marketTemplateNames, "marketTemplateNames should not be null.");
    templateMarketName = marketTemplateNames[0];
  }

  @Override
  protected String getAcceptMarketName(OutputMarket market) {
    return market.getTemplateMarketName();
  }

  @Override
  protected String selectorName() {
    return templateMarketName;
  }
}
