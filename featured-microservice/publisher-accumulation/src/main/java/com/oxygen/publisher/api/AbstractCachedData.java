package com.oxygen.publisher.api;

import com.oxygen.publisher.model.TicksMetrics;
import java.util.concurrent.atomic.AtomicInteger;
import lombok.Data;

/** Created by Aliaksei Yarotski on 2/1/18. */
@Data
public abstract class AbstractCachedData implements EntityLock {

  private AtomicInteger lock = new AtomicInteger(0);

  private TicksMetrics ticksMetrics = TicksMetrics.builder().build();

  public abstract boolean isEmpty();
}
