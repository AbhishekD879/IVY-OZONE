package com.coral.oxygen.middleware.common.mappers;

import com.egalacoral.spark.siteserver.model.Children;
import java.util.List;
import java.util.Objects;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;

@Component
public class SiteServeChildrenMapper {

  public <T> List<T> map(List<Children> children, Function<Children, T> getChild) {
    return children.stream().map(getChild).filter(Objects::nonNull).collect(Collectors.toList());
  }
}
