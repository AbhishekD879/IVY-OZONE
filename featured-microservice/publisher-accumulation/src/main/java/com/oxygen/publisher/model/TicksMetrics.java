package com.oxygen.publisher.model;

import java.util.concurrent.atomic.AtomicInteger;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Builder
@Data
@NoArgsConstructor
@AllArgsConstructor
public class TicksMetrics {

  @Builder.Default private AtomicInteger liveUpdatesTickCounter = new AtomicInteger(0);

  public void incLiveUpdatesTickCounter() {
    this.liveUpdatesTickCounter.incrementAndGet();
  }

  public int popLiveUpdatesTickCounter() {
    int ret = liveUpdatesTickCounter.get();
    liveUpdatesTickCounter.set(0);
    return ret;
  }
}
