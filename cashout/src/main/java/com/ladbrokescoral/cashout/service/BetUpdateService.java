package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.bpptoken.BppToken;
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.newrelic.api.agent.Token;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface BetUpdateService {

  Flux<UpdateDto> getAccHistoryUpdatedBets(
      BppToken username, Mono<List<BetSummaryModel>> bets, Token newRelicToken);

  void createSubscriptionInInternalPubSub(
      UUID connectionId, BppToken bppToken, Date connectionDate, List<BetSummaryModel> betList);

  void unsubscribeInInternalPubSub(UUID connectionId);

  Map<UUID, UserRequestContextAccHistory> getUserContexts();
}
