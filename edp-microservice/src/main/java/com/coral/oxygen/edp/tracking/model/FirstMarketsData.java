package com.coral.oxygen.edp.tracking.model;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.Objects;
import java.util.concurrent.ConcurrentHashMap;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = false)
public class FirstMarketsData extends EventData {

  // something like cache, first 5 markets is a most common request
  // todo extract this?, cache should be separated from model
  @JsonIgnore
  private ConcurrentHashMap<Integer, FirstMarketsData> cacheByMarketsCount =
      new ConcurrentHashMap<>();

  private static final int[] commonFirstMarketsRequest = new int[] {5, 10, 15, 20};

  public FirstMarketsData(OutputEvent event) {
    super(event);
  }

  public FirstMarketsData getCopyWithMarketLimit(int marketLimit) {
    FirstMarketsData result = cacheByMarketsCount.get(marketLimit);
    if (Objects.isNull(result)) {

      result = new FirstMarketsData(getEvent().getCopyWithMarketLimit(marketLimit));
      cacheByMarketsCount.put(marketLimit, result);
    }
    return result;
  }

  public void populateCache() {
    for (int i : commonFirstMarketsRequest) {
      cacheByMarketsCount.put(i, new FirstMarketsData(getEvent().getCopyWithMarketLimit(i)));
    }
  }
}
