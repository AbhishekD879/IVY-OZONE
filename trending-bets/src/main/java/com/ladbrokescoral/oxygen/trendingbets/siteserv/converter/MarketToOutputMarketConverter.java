package com.ladbrokescoral.oxygen.trendingbets.siteserv.converter;

import com.egalacoral.spark.siteserver.model.Market;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputMarket;
import org.springframework.stereotype.Component;

@Component
public class MarketToOutputMarketConverter extends BaseConverter<Market, OutputMarket> {

  @Override
  protected OutputMarket populateResult(Market market, OutputMarket outputMarket) {
    outputMarket.setId(market.getId());
    outputMarket.setName(market.getName());
    outputMarket.setMarketStatusCode(market.getMarketStatusCode());
    outputMarket.setIsActive(market.getIsActive());
    outputMarket.setIsDisplayed(market.getIsDisplayed());
    outputMarket.setIsLpAvailable(market.getIsLpAvailable());
    outputMarket.setIsSpAvailable((market.getIsSpAvailable()));
    outputMarket.setIsGpAvailable((market.getIsGpAvailable()));
    outputMarket.setRawHandicapValue(market.getRawHandicapValue());
    outputMarket.setLiveServChannels(
        market.getLiveServChannels().contains(",")
            ? market.getLiveServChannels().split(",")[0]
            : market.getLiveServChannels());
    outputMarket.setLiveServChildrenChannels(market.getLiveServChildrenChannels());
    outputMarket.setTemplateMarketId(market.getTemplateMarketId());
    outputMarket.setTemplateMarketName(market.getTemplateMarketName());
    outputMarket.setDrilldownTagNames(market.getDrilldownTagNames());
    outputMarket.setMinAccumulators(
        market.getMinAccumulators() != null ? market.getMinAccumulators() : 0);
    outputMarket.setMaxAccumulators(
        market.getMaxAccumulators() != null ? market.getMaxAccumulators() : 0);
    return outputMarket;
  }

  @Override
  protected OutputMarket createTarget() {
    return new OutputMarket();
  }
}
