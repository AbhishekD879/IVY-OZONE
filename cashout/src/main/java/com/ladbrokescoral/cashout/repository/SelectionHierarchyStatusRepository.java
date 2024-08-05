package com.ladbrokescoral.cashout.repository;

import java.math.BigInteger;
import java.util.Collection;
import java.util.List;
import reactor.core.publisher.Mono;

public interface SelectionHierarchyStatusRepository {
  void updateEventStatus(EntityStatus entityStatus);

  void updateMarketStatus(EntityStatus entityStatus);

  void updateSelectionStatus(EntityStatus entityStatus);

  Mono<List<EntityStatus>> fetchEventStatuses(Collection<BigInteger> eventIds);

  Mono<List<EntityStatus>> fetchMarketStatuses(Collection<BigInteger> marketIds);

  Mono<List<EntityStatus>> fetchSelectionStatuses(Collection<BigInteger> selectionIds);
}
