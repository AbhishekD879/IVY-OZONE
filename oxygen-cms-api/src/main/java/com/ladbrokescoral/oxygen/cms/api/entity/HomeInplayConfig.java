package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class HomeInplayConfig {
  private static final int DEFAULT_EVENTS_COUNT = 10;

  private int maxEventCount;
  private List<HomeInplaySport> homeInplaySports;

  public HomeInplayConfig() {
    this.maxEventCount = DEFAULT_EVENTS_COUNT;
    this.homeInplaySports = new ArrayList<>();
  }
}
