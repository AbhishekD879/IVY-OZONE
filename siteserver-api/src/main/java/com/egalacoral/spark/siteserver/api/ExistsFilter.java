package com.egalacoral.spark.siteserver.api;

import java.util.List;
import java.util.stream.Collectors;
import lombok.Data;

/**
 * Created by idomshchikov on 11/2/16.
 *
 * <p>Many requests allow the client to specify that Records of one RecordType be included in the
 * response only if related Records from another RecordType satisfy some client-supplied conditions.
 * This filtering is done using the "existsFilter" query parameters.
 */
@Data
public class ExistsFilter implements BaseFilter {

  private final List<String> queryMap;

  private ExistsFilter(ExistsFilterBuilder builder) {
    this.queryMap = builder.queryMap;
  }

  public static class ExistsFilterBuilder extends SimpleFilter.SimpleFilterBuilder {
    @Override
    public ExistsFilter build() {
      return new ExistsFilter(this);
    }
  }

  @Override
  public List<String> getQueryMap() {
    return queryMap;
  }

  @Override
  public String toString() {
    return queryMap.stream().map(Object::toString).collect(Collectors.joining("&"));
  }
}
