package com.coral.oxygen.middleware.ms.quickbet.connector;

import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.GeneralResponse;
import com.entain.oxygen.bettingapi.service.BettingService;
import io.vavr.collection.List;
import java.util.Optional;

class BetReader {

  private final String bettingToken;
  private final BettingService bettingService;

  BetReader(String bettingToken, BettingService bettingService) {
    this.bettingToken = bettingToken;
    this.bettingService = bettingService;
  }

  Optional<GeneralResponse<BetsResponse>> read(List<BetRef> betsToRead) {
    GeneralResponse<BetsResponse> generalResponse =
        bettingService.readBet(bettingToken, betsToRead.asJava());
    return Optional.ofNullable(generalResponse);
  }
}
