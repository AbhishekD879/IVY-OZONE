package com.coral.oxygen.edp.tracking;

import com.newrelic.api.agent.Trace;
import java.util.Collections;
import java.util.Map;

public class NoStorageTracker<T, D> extends AbstractTracker<T, D> {

  /** Passing param storage as null to super, so there won't be any storage for this tracker */
  public NoStorageTracker(DataConsumer<T, D> consumer) {
    super(null, consumer, (newData, oldData) -> true);
  }

  /**
   * Skipping the call to the storage in which is present in super method directly requesting data
   */
  @Trace(dispatcher = true)
  @Override
  public void addSubscription(Subscription<T, D> client) {
    addSubscriptionInternal(client);
    requestData(Collections.singleton(client.getTicket()));
  }

  /** Skipping saving to the storage when new data arrives */
  @Override
  protected void processNewData(Map<T, D> newData) {
    newData.keySet().parallelStream().forEach(ticket -> emitData(ticket, newData.get(ticket)));
  }
}
