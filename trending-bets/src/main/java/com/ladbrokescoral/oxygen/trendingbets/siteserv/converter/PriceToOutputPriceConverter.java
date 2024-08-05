package com.ladbrokescoral.oxygen.trendingbets.siteserv.converter;

import com.egalacoral.spark.siteserver.model.Price;
import com.ladbrokescoral.oxygen.trendingbets.model.OutputPrice;
import org.springframework.stereotype.Component;

@Component
public class PriceToOutputPriceConverter extends BaseConverter<Price, OutputPrice> {

  @Override
  protected OutputPrice populateResult(Price price, OutputPrice outputPrice) {
    outputPrice.setId(price.getId());
    outputPrice.setPriceDec(price.getPriceDec());
    outputPrice.setPriceDen(price.getPriceDen());
    outputPrice.setPriceNum(price.getPriceNum());
    outputPrice.setPriceType(price.getPriceType());
    outputPrice.setHandicapValueDec(price.getHandicapValueDec());
    outputPrice.setRawHandicapValue(price.getRawHandicapValue());
    outputPrice.setPriceStreamType(price.getPriceStreamType());
    outputPrice.setPriceAmerican(price.getPriceAmerican());
    outputPrice.setIsActive(price.getIsActive());
    return outputPrice;
  }

  @Override
  protected OutputPrice createTarget() {
    return new OutputPrice();
  }
}
