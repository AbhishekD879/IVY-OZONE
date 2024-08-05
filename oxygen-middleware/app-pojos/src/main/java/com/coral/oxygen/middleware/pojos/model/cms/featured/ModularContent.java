package com.coral.oxygen.middleware.pojos.model.cms.featured;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;
import java.util.stream.Collectors;

public class ModularContent extends ArrayList<ModularContentItem> {

  public ModularContent() {}

  public ModularContent(Collection<? extends ModularContentItem> c) {
    super(c);
  }

  public Collection<Long> getEnhMultiplesIds() {
    return getIds(ModularContentItem::getEnhMultiplesIds);
  }

  public Collection<Long> getEventsIds() {
    return getIds(ModularContentItem::getEventsIds);
  }

  public Collection<Long> getOutcomesIds() {
    return getIds(ModularContentItem::getOutcomesIds);
  }

  public Collection<Long> getRacingEventsIds() {
    return getIds(ModularContentItem::getRacingEventsIds);
  }

  public Collection<Long> getTypeIds() {
    return getIds(ModularContentItem::getTypeIds);
  }

  protected Collection<Long> getIds(Function<ModularContentItem, List<Long>> supplier) {
    return this.stream()
        .map(supplier)
        .filter(Objects::nonNull)
        .flatMap(Collection::stream)
        .collect(Collectors.toSet());
  }
}
