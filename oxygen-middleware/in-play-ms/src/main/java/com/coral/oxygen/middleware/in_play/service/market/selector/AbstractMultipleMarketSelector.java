package com.coral.oxygen.middleware.in_play.service.market.selector;

import com.coral.oxygen.middleware.pojos.model.output.OutputMarket;
import com.google.gson.Gson;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

public abstract class AbstractMultipleMarketSelector extends AbstractMarketSelector {

  private final List<String> marketTemplateNamesToKeep;

  public AbstractMultipleMarketSelector(String[] marketNamesToKeep, Gson gson) {
    super(gson);
    this.marketTemplateNamesToKeep =
        Arrays.stream(marketNamesToKeep)
            .map(name -> name.replace("|", "").toLowerCase())
            .collect(Collectors.toList());
  }

  @Override
  protected boolean acceptMarket(OutputMarket market) {
    String marketName = getAcceptMarketName(market);
    if (Objects.nonNull(marketName)) {
      return marketTemplateNamesToKeep.contains(marketName.replace("|", "").toLowerCase());
    }
    return false;
  }

  protected String getAcceptMarketName(OutputMarket market) {
    return market.getName();
  }
}
