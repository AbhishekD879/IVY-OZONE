package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.ladbrokescoral.cashout.bpptoken.BppToken;
import com.ladbrokescoral.cashout.bpptoken.BppTokenOperations;
import com.ladbrokescoral.cashout.model.context.IndexedSportsData;
import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.model.safbaf.Entity;
import com.ladbrokescoral.cashout.service.updates.UniversalUpdateProcessor;
import com.ladbrokescoral.cashout.service.updates.pubsub.Publisher;
import com.ladbrokescoral.cashout.service.updates.pubsub.Subscriber;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Token;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.math.NumberUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.messaging.MessageHandler;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
@RequiredArgsConstructor
public class BetUpdateServiceImpl implements BetUpdateService {

  private final Publisher publisher;
  private final UniversalUpdateProcessor universalUpdateProcessor;
  private final UserFluxBetUpdatesContext betUpdatesContext;
  private final Map<UUID, UserRequestContextAccHistory> userContextForConnectionId =
      new ConcurrentHashMap<>();
  private final Function<IndexedSportsData, UnknownSelectionDataService>
      unknownSelectionDataFactory;
  private final BppTokenOperations bppTokenOperations;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  /*-
   * Creates kafka event/market/selection (Saf) and  betslip (Baf) liveupdates handler for user
   *
   * @param username - unique username
   * @param bppToken    - BPP user token, used by BPP to identify user
   * @param userBets - user bets, used for filtering kafka liveupdates interested for user
   * @return betDetail response from BPP or new cashout price from Cashout V4
   */
  @Override
  public Flux<UpdateDto> getAccHistoryUpdatedBets(
      BppToken bppToken, Mono<List<BetSummaryModel>> userBets, Token newRelicToken) {
    Date connectionDate = new Date();

    return Flux.create(
        sink ->
            userBets.subscribe(
                betList -> {
                  List<BetSummaryModel> betsWithCashoutAvailable =
                      betList.stream()
                          .filter(
                              bet ->
                                  NumberUtils.isCreatable(bet.getCashoutValue())
                                      || "CASHOUT_SELN_SUSPENDED".equals(bet.getCashoutValue()))
                          .collect(Collectors.toList());

                  betsWithCashoutAvailable.forEach(
                      bet -> betUpdatesContext.register(bet.getId(), sink));

                  String token = bppToken.getToken();
                  betUpdatesContext.register(token, sink);

                  UserRequestContextAccHistory userRequestContext =
                      UserRequestContextAccHistory.builder()
                          .username(bppToken.getEncodedUser().getSportBookUserName())
                          .tokenExpiresIn(bppToken.getTimeLeftToExpire())
                          .token(token)
                          .connectionDate(connectionDate)
                          .userBets(betsWithCashoutAvailable)
                          .build();

                  UnknownSelectionDataService unknownSelectionData =
                      unknownSelectionDataFactory.apply(userRequestContext.getIndexedData());

                  unknownSelectionData.resolveUnknowns();

                  MessageHandler handler =
                      message -> {
                        Entity msg = (Entity) message.getPayload();
                        universalUpdateProcessor.process(userRequestContext, msg);
                      };
                  Subscriber subscriber =
                      new Subscriber(UUID.randomUUID().toString(), token, handler);
                  sink.onCancel(
                      () -> {
                        ASYNC_LOGGER.info(
                            "User {} stopped listening updates by cancel event", token);
                        NewRelic.incrementCounter("/User/Subscription/Unsubscribe/ByCancel");
                      });
                  sink.onDispose(
                      () -> {
                        ASYNC_LOGGER.info(
                            "User {} was unsubscribed from all kafka updates by dispose", token);
                        NewRelic.incrementCounter("/User/Subscription/Unsubscribe/ByDispose");
                        publisher.unsubscribe(userRequestContext, subscriber.getSubscriberId());
                        newRelicToken.linkAndExpire();
                      });
                  try {
                    publisher.subscribe(subscriber, userRequestContext);
                    ASYNC_LOGGER.info("User {} was subscribed to all kafka updates", token);
                    NewRelic.incrementCounter("/User/Subscription/Subscribed");
                  } catch (Exception e) {
                    ASYNC_LOGGER.error("User {} was NOT subscribed to kafka updated", token, e);
                    NewRelic.incrementCounter("/User/Subscription/Fail");
                    NewRelic.noticeError(e);
                  }
                }));
  }

  @Override
  public void createSubscriptionInInternalPubSub(
      UUID connectionId, BppToken bppToken, Date connectionDate, List<BetSummaryModel> bets) {
    String token = bppToken.getToken();
    UserRequestContextAccHistory userRequestContext =
        UserRequestContextAccHistory.builder()
            .username(bppToken.getEncodedUser().getSportBookUserName())
            .tokenExpiresIn(bppToken.getTimeLeftToExpire())
            .token(token)
            .connectionDate(connectionDate)
            .userBets(bets)
            .build();

    UnknownSelectionDataService unknownSelectionData =
        unknownSelectionDataFactory.apply(userRequestContext.getIndexedData());

    unknownSelectionData.resolveUnknowns();

    MessageHandler handler =
        message -> {
          Entity msg = (Entity) message.getPayload();
          universalUpdateProcessor.process(userRequestContext, msg);
        };
    Subscriber subscriber = new Subscriber(connectionId.toString(), token, handler);
    try {
      publisher.subscribe(subscriber, userRequestContext);
      ASYNC_LOGGER.info("User {} was subscribed to all kafka updates", token);
      NewRelic.incrementCounter("/User/Subscription/Subscribed");
      userContextForConnectionId.put(connectionId, userRequestContext);
    } catch (Exception e) {
      ASYNC_LOGGER.error("User {} was NOT subscribed to kafka updated", token, e);
      NewRelic.incrementCounter("/User/Subscription/Fail");
      NewRelic.noticeError(e);
    }
  }

  @Override
  public void unsubscribeInInternalPubSub(UUID connectionId) {
    if (userContextForConnectionId.containsKey(connectionId)) {
      UserRequestContextAccHistory ctx = userContextForConnectionId.remove(connectionId);
      publisher.unsubscribe(ctx, connectionId.toString());
    } else {
      ASYNC_LOGGER.warn("User context wasn't found for connection {}", connectionId);
    }
  }

  @Override
  public Map<UUID, UserRequestContextAccHistory> getUserContexts() {
    return userContextForConnectionId;
  }
}
