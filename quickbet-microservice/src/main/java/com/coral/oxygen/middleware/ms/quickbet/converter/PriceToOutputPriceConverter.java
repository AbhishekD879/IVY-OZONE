package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.egalacoral.spark.siteserver.model.Price;
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
    return outputPrice;
  }

  @Override
  protected OutputPrice createTarget() {
    return new OutputPrice();
  }
}
