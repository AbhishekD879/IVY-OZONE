package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.entain.oxygen.bettingapi.model.bet.api.response.placeBetV2.RespBetPlace;
import org.springframework.stereotype.Component;

@Component
public class MultiPlaceBetResponseAdapterFactory {
  public MultiPlaceBetResponseAdapter from(RespBetPlace respBetPlace) {
    return new MultiPlaceBetResponseAdapter(respBetPlace);
  }
}
