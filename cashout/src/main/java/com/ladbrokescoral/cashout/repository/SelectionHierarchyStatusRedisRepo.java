package com.ladbrokescoral.cashout.repository;

import java.math.BigInteger;
import java.time.Duration;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

@Component
@RequiredArgsConstructor
public class SelectionHierarchyStatusRedisRepo implements SelectionHierarchyStatusRepository {

  private static final Duration TTL = Duration.ofHours(24);
  private final ReactiveRedisTemplate<String, EntityStatus> entityStatusRepo;

  @Override
  public void updateEventStatus(EntityStatus entityStatus) {
    entityStatusRepo
        .opsForValue()
        .set(eventKey(entityStatus.getEntityId()), entityStatus, TTL)
        .subscribe();
  }

  @Override
  public void updateMarketStatus(EntityStatus entityStatus) {
    entityStatusRepo
        .opsForValue()
        .set(marketKey(entityStatus.getEntityId()), entityStatus, TTL)
        .subscribe();
  }

  @Override
  public void updateSelectionStatus(EntityStatus entityStatus) {
    entityStatusRepo
        .opsForValue()
        .set(selectionKey(entityStatus.getEntityId()), entityStatus, TTL)
        .subscribe();
  }

  @Override
  public Mono<List<EntityStatus>> fetchEventStatuses(Collection<BigInteger> eventIds) {
    return multiGet(toSetOfRedisKeys(eventIds, this::eventKey));
  }

  @Override
  public Mono<List<EntityStatus>> fetchMarketStatuses(Collection<BigInteger> marketIds) {
    return multiGet(toSetOfRedisKeys(marketIds, this::marketKey));
  }

  @Override
  public Mono<List<EntityStatus>> fetchSelectionStatuses(Collection<BigInteger> selectionIds) {
    return multiGet(toSetOfRedisKeys(selectionIds, this::selectionKey));
  }

  private Set<String> toSetOfRedisKeys(
      Collection<BigInteger> ids, Function<BigInteger, String> keyFunction) {
    return ids.stream().map(keyFunction).collect(Collectors.toSet());
  }

  private Mono<List<EntityStatus>> multiGet(Set<String> keys) {
    if (keys.isEmpty()) {
      return Mono.empty();
    } else {
      return entityStatusRepo
          .opsForValue()
          .multiGet(keys)
          .map(list -> list.stream().filter(Objects::nonNull).collect(Collectors.toList()));
    }
  }

  private String eventKey(BigInteger eventId) {
    return "EVENT_STATUS_" + eventId;
  }

  private String marketKey(BigInteger marketId) {
    return "MARKET_STATUS_" + marketId;
  }

  private String selectionKey(BigInteger selectionId) {
    return "SELECTION_STATUS_" + selectionId;
  }
}
