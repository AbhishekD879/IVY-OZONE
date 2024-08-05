package com.coral.oxygen.middleware.common.imdg;

import com.coral.oxygen.middleware.common.configuration.DistributedKey;
import java.util.List;
import org.springframework.boot.actuate.health.HealthIndicator;

/**
 * Abstraction for in memory data grid instance
 *
 * @author volodymyr.masliy
 */
public interface DistributedInstance {

  String getProviderName();

  <K, V> DistributedMap<K, V> getMap(DistributedKey key);

  DistributedAtomicLong getAtomicLong(DistributedKey key);

  HealthIndicator getHealthIndicator();

  String getValue(DistributedKey key, String suffix);

  String getValue(DistributedKey key);

  List<String> getValues(DistributedKey key, List<String> suffixes);

  String updateExpirableValue(DistributedKey key, String suffix, String newValue);

  String updateExpirableValue(DistributedKey key, String newValue);
}
