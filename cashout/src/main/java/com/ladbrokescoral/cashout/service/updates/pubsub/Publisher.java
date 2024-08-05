package com.ladbrokescoral.cashout.service.updates.pubsub;

import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.Entity;
import com.ladbrokescoral.cashout.model.safbaf.Event;
import com.ladbrokescoral.cashout.model.safbaf.Market;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.model.safbaf.betslip.Betslip;
import java.math.BigInteger;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.messaging.Message;
import org.springframework.messaging.support.GenericMessage;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class Publisher implements UpdateMessageHandler<Message<?>> {

  private static final int SECOND = 2;
  private static final Pattern splitPattern = Pattern.compile(":");
  private final ConcurrentHashMap<String, Map<String, Subscriber>> eventConcurrentHashMap =
      new ConcurrentHashMap<>();
  private final ConcurrentHashMap<String, Map<String, Subscriber>> marketConcurrentHashMap =
      new ConcurrentHashMap<>();
  private final ConcurrentHashMap<String, Map<String, Subscriber>> selectionConcurrentHashMap =
      new ConcurrentHashMap<>();
  private final ConcurrentHashMap<String, Map<String, Subscriber>> betslipConcurrentHashMap =
      new ConcurrentHashMap<>();
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  public void subscribe(Subscriber subscriber, UserRequestContextAccHistory userRequestContext) {
    subscribeToEvents(subscriber, userRequestContext);
    subscribeToMarkets(subscriber, userRequestContext);
    subscribeToOutcomes(subscriber, userRequestContext);
    subscribeToBetslip(subscriber, userRequestContext);
  }

  public void unsubscribe(UserRequestContextAccHistory userRequestContext, String subscriberId) {
    unsubscribeEvents(userRequestContext, subscriberId);
    unsubscribeMarkets(userRequestContext, subscriberId);
    unsubscribeSelections(userRequestContext, subscriberId);
    unsubscribeBetSlip(userRequestContext, subscriberId);
  }

  private void subscribeToEvents(
      Subscriber subscriber, UserRequestContextAccHistory userRequestContext) {
    List<String> subscriberAddedToEvents =
        userRequestContext
            .getIndexedData()
            .getAllEventIds()
            .parallelStream()
            .map(
                eventId -> {
                  String eventKey = buildEventMapKey(eventId);
                  return addSubscriberToEntity(subscriber, eventKey, eventConcurrentHashMap);
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug(
        "User with token {} was subscribed to events - {}",
        subscriber.getToken(),
        subscriberAddedToEvents);
  }

  private void subscribeToMarkets(
      Subscriber subscriber, UserRequestContextAccHistory userRequestContext) {
    List<String> subscriberAddedToMarkets =
        userRequestContext
            .getIndexedData()
            .getAllMarketIds()
            .parallelStream()
            .map(
                marketId -> {
                  String marketKey = buildMarketMapKey(marketId);
                  return addSubscriberToEntity(subscriber, marketKey, marketConcurrentHashMap);
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug(
        "User with token {} was subscribed to markets - {}",
        subscriber.getToken(),
        subscriberAddedToMarkets);
  }

  private void subscribeToOutcomes(
      Subscriber subscriber, UserRequestContextAccHistory userRequestContext) {
    List<String> subscriberAddedToOutcomes =
        userRequestContext
            .getIndexedData()
            .getAllSelectionIds()
            .parallelStream()
            .map(
                selectionId -> {
                  String selectionKey = buildSelectionMapKey(selectionId);
                  return addSubscriberToEntity(
                      subscriber, selectionKey, selectionConcurrentHashMap);
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug(
        "User with token {} was subscribed to selections - {}",
        subscriber.getToken(),
        subscriberAddedToOutcomes);
  }

  private void subscribeToBetslip(
      Subscriber subscriber, UserRequestContextAccHistory userRequestContext) {
    List<String> betKeys =
        userRequestContext
            .getUserBets()
            .parallelStream()
            .map(
                bet -> {
                  String betKey = buildBetslipMapKey(bet.getId());
                  addSubscriberToEntity(subscriber, betKey, betslipConcurrentHashMap);
                  return betKey;
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug("Subscribed for partial updates for betIds - {}", betKeys);
  }

  private String addSubscriberToEntity(
      Subscriber subscriber,
      String entityKey,
      ConcurrentHashMap<String, Map<String, Subscriber>> entityConcurrentHashMap) {
    entityConcurrentHashMap.putIfAbsent(entityKey, new ConcurrentHashMap<>());
    entityConcurrentHashMap.get(entityKey).putIfAbsent(subscriber.getSubscriberId(), subscriber);
    return entityKey;
  }

  private void unsubscribeEvents(
      UserRequestContextAccHistory userRequestContext, String subscriberId) {
    List<String> eventKeys =
        userRequestContext
            .getIndexedData()
            .getAllEventIds()
            .parallelStream()
            .map(
                eventId -> {
                  String eventKey = buildEventMapKey(eventId);
                  Optional.ofNullable(eventConcurrentHashMap.get(eventKey))
                      .ifPresent(subscribers -> subscribers.remove(subscriberId));
                  return eventKey;
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug(
        "User with token {} was unsubscribed from event updates - {}",
        userRequestContext.getToken(),
        eventKeys);
  }

  private void unsubscribeMarkets(
      UserRequestContextAccHistory userRequestContext, String subscriberId) {
    List<String> marketKeys =
        userRequestContext
            .getIndexedData()
            .getAllMarketIds()
            .parallelStream()
            .map(
                marketId -> {
                  String marketKey = buildMarketMapKey(marketId);
                  Optional.ofNullable(marketConcurrentHashMap.get(marketKey))
                      .ifPresent(subscribers -> subscribers.remove(subscriberId));
                  return marketKey;
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug(
        "User with token {} was unsubscribed from market updates - {}",
        userRequestContext.getToken(),
        marketKeys);
  }

  private void unsubscribeSelections(
      UserRequestContextAccHistory userRequestContext, String subscriberId) {
    List<String> selectionKeys =
        userRequestContext
            .getIndexedData()
            .getAllSelectionIds()
            .parallelStream()
            .map(
                selectionId -> {
                  String selectionKey = buildSelectionMapKey(selectionId);
                  Optional.ofNullable(selectionConcurrentHashMap.get(selectionKey))
                      .ifPresent(subscribers -> subscribers.remove(subscriberId));
                  return selectionKey;
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug(
        "User with token {} was unsubscribed from selection updates - {}",
        userRequestContext.getToken(),
        selectionKeys);
  }

  private void unsubscribeBetSlip(
      UserRequestContextAccHistory userRequestContext, String subscriberId) {
    List<String> betKeys =
        userRequestContext
            .getUserBets()
            .parallelStream()
            .map(
                bet -> {
                  String betKey = buildBetslipMapKey(bet.getId());
                  Optional.ofNullable(betslipConcurrentHashMap.get(betKey))
                      .ifPresent(subscribers -> subscribers.remove(subscriberId));
                  return betKey;
                })
            .collect(Collectors.toList());
    ASYNC_LOGGER.debug("Unsubscribed from betslip updates - {}", betKeys);
  }

  private Mono<List<String>> processNotify(
      Entity entity,
      String mapKey,
      ConcurrentHashMap<String, Map<String, Subscriber>> entityConcurrentHashMap) {
    if (!entityConcurrentHashMap.containsKey(mapKey)) {
      return Mono.just(Collections.emptyList());
    } else {
      return Mono.just(entityConcurrentHashMap.get(mapKey))
          .map(Map::values)
          .map(
              subscribers ->
                  subscribers
                      .parallelStream()
                      .map(
                          subscriber -> {
                            subscriber.notify(new GenericMessage<>(entity));
                            return subscriber.getToken();
                          })
                      .collect(Collectors.toList()));
    }
  }

  private String buildEventMapKey(BigInteger eventId) {
    return "E_" + eventId;
  }

  private String buildMarketMapKey(BigInteger marketId) {
    return "M_" + marketId;
  }

  private String buildSelectionMapKey(BigInteger selectionId) {
    return "S_" + selectionId;
  }

  private String buildBetslipMapKey(String betId) {
    return "B_" + betId;
  }

  @Override
  public void handleUpdateMessage(Message<?> message) {
    Entity msg = (Entity) message.getPayload();
    if (msg instanceof Event) {
      Event event = (Event) msg;
      processNotify(event, buildEventMapKey(event.getEventKey()), eventConcurrentHashMap)
          .subscribe(
              subscribers ->
                  ASYNC_LOGGER.debug(
                      "Following subscribers was notified - {}, about event - {}",
                      subscribers,
                      event.getEventKey()));
    } else if (msg instanceof Market) {
      Market market = (Market) msg;
      processNotify(market, buildMarketMapKey(market.getMarketKey()), marketConcurrentHashMap)
          .subscribe(
              subscribers ->
                  ASYNC_LOGGER.debug(
                      "Following subscribers was notified - {}, about market - {}",
                      subscribers,
                      market.getMarketKey()));
    } else if (msg instanceof Selection) {
      Selection selection = (Selection) msg;
      if (Objects.isNull(selection.getSelectionKey()) && selection.getRule4().isPresent()) {
        processNotify(
                selection,
                buildMarketMapKey(getMarketkey(selection.getMeta().getParents())),
                marketConcurrentHashMap)
            .subscribe(
                subscribers ->
                    ASYNC_LOGGER.debug(
                        "Following subscribers was notified - {}, about market rule4 applied - {}",
                        subscribers,
                        getMarketkey(selection.getMeta().getParents())));
      } else {
        processNotify(
                selection,
                buildSelectionMapKey(selection.getSelectionKey()),
                selectionConcurrentHashMap)
            .subscribe(
                subscribers ->
                    ASYNC_LOGGER.debug(
                        "Following subscribers was notified - {}, about selection - {}",
                        subscribers,
                        selection.getSelectionKey()));
      }
    } else if (msg instanceof Betslip) {
      Betslip betslip = (Betslip) msg;
      betslip.getBets().getBet().stream()
          .findFirst()
          .ifPresent(
              bet ->
                  processNotify(
                          betslip, buildBetslipMapKey(bet.getBetKey()), betslipConcurrentHashMap)
                      .subscribe(
                          subscribers ->
                              ASYNC_LOGGER.debug(
                                  "Following subscribers was notified - {}, about partial cashout or betslip - {}",
                                  subscribers,
                                  bet.getBetKey())));
    }
  }

  private BigInteger getMarketkey(String msg) {
    String[] split = splitPattern.split(msg);
    return new BigInteger(split[split.length - 1].substring(SECOND));
  }
}
