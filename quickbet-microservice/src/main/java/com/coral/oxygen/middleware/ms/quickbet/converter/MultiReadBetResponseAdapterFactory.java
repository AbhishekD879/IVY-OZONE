package com.coral.oxygen.middleware.ms.quickbet.converter;

import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import org.springframework.stereotype.Component;

@Component
public class MultiReadBetResponseAdapterFactory {
  public MultiReadBetResponseAdapter from(BetsResponse betsResponse) {
    return new MultiReadBetResponseAdapter(betsResponse);
  }
}
