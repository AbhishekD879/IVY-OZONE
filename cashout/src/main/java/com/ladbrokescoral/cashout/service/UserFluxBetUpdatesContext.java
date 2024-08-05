package com.ladbrokescoral.cashout.service;

import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.updates.UserUpdateTrigger;
import com.ladbrokescoral.cashout.service.updates.UserUpdateTriggerDto;
import com.newrelic.api.agent.NewRelic;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map.Entry;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentMap;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;
import reactor.core.publisher.FluxSink;

@Component
public class UserFluxBetUpdatesContext implements UserUpdateTrigger {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");
  private static final String BASE_BET_UPDATE_COUNTER_TEMPLATE = "Custom/UserBetUpdatesCtx/";
  private final ConcurrentMap<String, List<FluxSink<UpdateDto>>> betUpdatesSinks =
      new ConcurrentHashMap<>();

  public void register(String emitKey, FluxSink<UpdateDto> betUpdateSink) {
    betUpdatesSinks.putIfAbsent(emitKey, new ArrayList<>());
    betUpdatesSinks.computeIfPresent(
        emitKey,
        (key, sinks) -> {
          sinks.add(betUpdateSink);
          ASYNC_LOGGER.info(
              "Registered new sink with key: {}. new size: {}", emitKey, sinks.size());
          return sinks;
        });
  }

  public void sendBetUpdate(String emitKey, UpdateDto betUpdate) {
    List<FluxSink<UpdateDto>> sinks = getValidSinks(emitKey);
    if (sinks.isEmpty()) {
      ASYNC_LOGGER.debug("Bet update wasn't delivered by emitKey{}", emitKey);
      incrementFailed(betUpdate);
    } else {
      ASYNC_LOGGER.debug("Sending betUpdates [{}] to {}", sinks.size(), emitKey);
      sinks.forEach(s -> s.next(betUpdate));
      incrementSent(betUpdate);
      incrementSentToSinks(betUpdate, sinks.size());
    }
  }

  private StringBuilder updateTypeTemplate(UpdateDto betUpdate) {
    return new StringBuilder(BASE_BET_UPDATE_COUNTER_TEMPLATE)
        .append(betUpdate.getCashoutData() != null ? "CashoutUpdate" : "BetUpdate")
        .append("/");
  }

  private void incrementFailed(UpdateDto betUpdate) {
    NewRelic.incrementCounter(updateTypeTemplate(betUpdate).append("Failed").toString());
  }

  private void incrementSent(UpdateDto betUpdate) {
    NewRelic.incrementCounter(updateTypeTemplate(betUpdate).append("SentBetId").toString());
  }

  private void incrementSentToSinks(UpdateDto betUpdate, int sinksSize) {
    NewRelic.incrementCounter(
        updateTypeTemplate(betUpdate).append("SentSinks").toString(), sinksSize);
  }

  private List<FluxSink<UpdateDto>> getValidSinks(String emitKey) {
    return betUpdatesSinks.getOrDefault(emitKey, Collections.emptyList()).stream()
        .filter(Objects::nonNull)
        .filter(sink -> !sink.isCancelled())
        .collect(Collectors.toList());
  }

  public void sendException(String emitKey, Throwable t) {
    List<FluxSink<UpdateDto>> sinks = getValidSinks(emitKey);
    if (sinks.isEmpty()) {
      ASYNC_LOGGER.debug("Exception wasn't delivered by emitKey{}", emitKey);
    } else {
      ASYNC_LOGGER.debug("Sending betUpdate exception [{}] to {}", sinks.size(), emitKey);
      sinks.forEach(s -> s.error(t));
    }
  }

  @Scheduled(fixedDelay = 1_800_000) // 30 minutes
  protected void cleanUp() {
    List<String> keysToCleanup =
        betUpdatesSinks.entrySet().stream()
            .filter(entry -> shouldBeRemoved(entry.getValue()))
            .map(Entry::getKey)
            .collect(Collectors.toList());

    ASYNC_LOGGER.info("Removing betUpdate sink keys[{}]: {}", keysToCleanup.size(), keysToCleanup);
    keysToCleanup.forEach(
        key ->
            betUpdatesSinks.computeIfPresent(
                key,
                (k, v) -> {
                  // need to do this check again, but now in synchronized manner
                  if (shouldBeRemoved(v)) {
                    return null;
                  } else {
                    return v;
                  }
                }));
  }

  private boolean shouldBeRemoved(List<FluxSink<UpdateDto>> v) {
    return v == null || v.isEmpty() || v.stream().allMatch(FluxSink::isCancelled);
  }

  @Override
  public void triggerCashoutSuspension(UserUpdateTriggerDto suspensionDto) {
    suspensionDto.getBetIds().stream()
        .map(
            betId -> {
              Bet bet = new Bet();
              bet.setBetId(betId);
              bet.setCashoutValue("CASHOUT_SELN_SUSPENDED");
              bet.setCashoutStatus(
                  "Suspended by cashout microservice: bet has suspended selection(s)");
              return bet;
            })
        .map(betSuspension -> UpdateDto.builder().bet(betSuspension).build())
        .forEach(betUpdate -> sendBetUpdate(suspensionDto.getToken(), betUpdate));
  }

  @Override
  public void triggerBetSettled(UserUpdateTriggerDto suspensionDto) {
    if (suspensionDto != null && !CollectionUtils.isEmpty(suspensionDto.getBetIds())) {
      suspensionDto.getBetIds().stream()
          .map(this::settledBet)
          .map(bet -> UpdateDto.builder().bet(bet).build())
          .forEach(update -> sendBetUpdate(update.getBet().getBetId(), update));
    }
  }

  private Bet settledBet(String betId) {
    Bet bet = new Bet();
    bet.setBetId(betId);
    bet.setCashoutValue("BET_SETTLED");
    bet.setSettled("Y");
    return bet;
  }
}
