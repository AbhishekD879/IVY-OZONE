package com.coral.oxygen.middleware.ms.quickbet.converter;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.egalacoral.spark.siteserver.model.Price;
import org.junit.jupiter.api.Test;

public class PriceToOutputPriceConverterTest {

  @Test
  public void testConvert() {
    Price price = TestUtils.deserializeWithGson("converter/price.json", Price.class);

    PriceToOutputPriceConverter converter = new PriceToOutputPriceConverter();

    OutputPrice outputPrice = converter.convert(price);

    assertThat(price.getId()).isEqualTo(outputPrice.getId());
    assertThat(price.getHandicapValueDec()).isEqualTo(outputPrice.getHandicapValueDec());
    assertThat(price.getPriceType()).isEqualTo(outputPrice.getPriceType());
    assertThat(price.getPriceDec()).isEqualTo(outputPrice.getPriceDec());
    assertThat(price.getRawHandicapValue()).isEqualTo(outputPrice.getRawHandicapValue());
    assertThat(price.getPriceDen()).isEqualTo(outputPrice.getPriceDen());
    assertThat(price.getPriceNum()).isEqualTo(outputPrice.getPriceNum());
  }
}
