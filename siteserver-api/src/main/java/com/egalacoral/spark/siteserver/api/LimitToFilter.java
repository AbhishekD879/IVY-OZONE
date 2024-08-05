package com.egalacoral.spark.siteserver.api;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by idomshchikov on 11/2/16.
 *
 * <p>A LimitTo filter may be specied by the client for some record-types on certain requests to
 * cause only the higest or lowest ranked record accordingly to some speci ed criteria to be
 * returned in the response.
 */
public class LimitToFilter implements BaseFilter {

  private final List<String> queryMap;

  private LimitToFilter(LimitToFilterBuilder builder) {
    this.queryMap = builder.queryMap;
  }

  public static class LimitToFilterBuilder {
    private final List<String> queryMap = new ArrayList<>();

    public LimitToFilter build() {
      return new LimitToFilter(this);
    }

    public LimitToFilterBuilder addField(String field, LimitToOperation limitToOperation) {
      queryMap.add(field + SEPARATOR + limitToOperation.getName());
      return this;
    }

    public LimitToFilterBuilder addFieldWithHighestRank(String field) {
      return addField(field, LimitToOperation.HIGHEST);
    }

    public LimitToFilterBuilder addFieldWithLowestRank(String field) {
      return addField(field, LimitToOperation.LOWEST);
    }
  }

  @Override
  public List<String> getQueryMap() {
    return queryMap;
  }
}
