package com.egalacoral.spark.siteserver.model;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public abstract class IdentityWithChildren extends Identity {

  private List<Children> children = new ArrayList<>();

  public <T> List<T> getConcreteChildren(Function<Children, T> mappingFunction) {
    return this.getChildren().stream()
        .map(mappingFunction)
        .filter(Objects::nonNull)
        .collect(Collectors.toList());
  }
}
