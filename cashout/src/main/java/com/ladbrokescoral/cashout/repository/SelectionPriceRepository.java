package com.ladbrokescoral.cashout.repository;

import com.ladbrokescoral.cashout.model.context.SelectionPrice;
import com.newrelic.api.agent.Trace;
import java.time.Duration;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.data.redis.core.ReactiveValueOperations;
import org.springframework.stereotype.Repository;
import org.springframework.util.CollectionUtils;
import reactor.core.publisher.Mono;

@Repository
public class SelectionPriceRepository implements ReactiveRepository<SelectionPrice> {

  private static final String SELECTION_PRICE = "SelectionPrice_";
  private final ReactiveValueOperations<String, SelectionPrice> valueOperations;

  @Value("${redis.selection.price.ttl}")
  private long hours = 24L;

  @Autowired
  public SelectionPriceRepository(
      ReactiveRedisTemplate<String, SelectionPrice> reactiveRedisTemplate) {
    valueOperations = reactiveRedisTemplate.opsForValue();
  }

  @Override
  @Trace(metricName = "/Redis/Save/Selection", async = true)
  public Mono<Boolean> save(String selectionId, SelectionPrice value) {
    return valueOperations.set(buildKey(selectionId), value, Duration.ofHours(hours));
  }

  @Override
  @Trace(metricName = "/Redis/Save/Selection", async = true)
  public Mono<Boolean> save(SelectionPrice selPrice) {
    return valueOperations.set(
        buildKey(selPrice.getOutcomeId()), selPrice, Duration.ofHours(hours));
  }

  @Override
  @Trace(metricName = "/Redis/Get/Single", async = true)
  public Mono<SelectionPrice> get(String selectionId) {
    return valueOperations.get(buildKey(selectionId));
  }

  @Override
  @Trace(metricName = "/Redis/Get/Multiple", async = true)
  public Mono<List<SelectionPrice>> multiGet(Collection<String> selectionIds) {
    if (CollectionUtils.isEmpty(selectionIds)) {
      return Mono.empty();
    }
    List<String> redisKeys = selectionIds.stream().map(this::buildKey).collect(Collectors.toList());
    return valueOperations.multiGet(redisKeys).filter(Objects::nonNull);
  }

  @Override
  @Trace(metricName = "/Redis/Delete/Single", async = true)
  public Mono<Boolean> delete(String selectionId) {
    return valueOperations.delete(buildKey(selectionId));
  }

  private String buildKey(String key) {
    return SELECTION_PRICE + key;
  }
}
