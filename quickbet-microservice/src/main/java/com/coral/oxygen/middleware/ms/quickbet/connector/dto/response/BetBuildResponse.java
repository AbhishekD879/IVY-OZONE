package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import com.entain.oxygen.bettingapi.model.bet.api.response.buildBet.BetBuildResponseModel;
import io.vavr.collection.Set;
import lombok.Value;

@Value
public class BetBuildResponse {
  private BetBuildResponseModel betBuildResponseModel;
  private Set<String> failedOutcomeIds;
}
