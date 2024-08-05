package com.oxygen.publisher.sportsfeatured.model;

import com.oxygen.publisher.sportsfeatured.model.module.AbstractFeaturedModule;
import java.util.Objects;
import java.util.function.Predicate;
import lombok.RequiredArgsConstructor;
import lombok.ToString;

/** Predicate class for module filtering */
@ToString
@RequiredArgsConstructor
public class Identifier implements Predicate<AbstractFeaturedModule<?>> {

  private final ModuleType moduleType;

  @Override
  public boolean test(AbstractFeaturedModule<?> module) {
    return Objects.nonNull(module) && moduleType.equals(module.getModuleType());
  }
}
