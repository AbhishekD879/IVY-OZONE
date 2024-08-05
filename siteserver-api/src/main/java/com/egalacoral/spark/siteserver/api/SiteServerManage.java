package com.egalacoral.spark.siteserver.api;

import com.egalacoral.spark.siteserver.model.HealthCheck;
import java.util.Optional;

/** Created by Aliaksei Yarotski on 10/10/17. */
public interface SiteServerManage {

  void evictConnections();

  Optional<HealthCheck> getHealthCheck();
}
