package com.coral.oxygen.middleware.common.imdg.adapters.redisson;

import java.util.concurrent.TimeUnit;
import lombok.AllArgsConstructor;
import lombok.Getter;

/**
 * @author volodymyr.masliy
 */
@Getter
@AllArgsConstructor
public class OxygenRedissonConfig {
  private String prefix;
  private long mapEntriesTtl;
  private TimeUnit mapEntriesTtlUnits;
}
