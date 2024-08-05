package com.ladbrokescoral.oxygen.timeline.api.registrators;

/** Created by Aliaksei Yarotski on 2/7/18. */
public interface ReloadableService {

  void start();

  void evict();

  boolean isHealthy();

  void onFail(Exception ex);

  default boolean getHealthStatusForExternal() {
    return isHealthy();
  }
}
