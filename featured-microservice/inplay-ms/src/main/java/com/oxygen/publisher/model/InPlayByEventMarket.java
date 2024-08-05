package com.oxygen.publisher.model;

import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;
import lombok.AccessLevel;
import lombok.Data;
import lombok.Setter;

/** Created by Aliaksei Yarotski on 4/12/18. */
@Data
public class InPlayByEventMarket {

  private ModuleDataItem moduleDataItem;

  @Setter(AccessLevel.NONE)
  private Set<RawIndex> cacheRefs = ConcurrentHashMap.newKeySet();

  private List<OutputMarket> primaryMarkets;

  public Set<RawIndex> getCacheRefsByLevel(final int level) {
    return this.cacheRefs.stream()
        .filter(ref -> ref.getLevel() == level)
        .collect(Collectors.toSet());
  }

  public boolean hasIndexForLevel(final int level) {
    return this.cacheRefs.stream().filter(ref -> ref.getLevel() == level).findAny().isPresent();
  }

  public boolean addCacheRef(RawIndex index) {
    return cacheRefs.add(index);
  }
}
