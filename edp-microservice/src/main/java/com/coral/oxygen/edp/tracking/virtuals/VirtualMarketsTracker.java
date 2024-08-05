package com.coral.oxygen.edp.tracking.virtuals;

import com.coral.oxygen.edp.tracking.*;
import com.coral.oxygen.edp.tracking.model.EventData;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import org.springframework.stereotype.Component;

@Component
public class VirtualMarketsTracker extends NoStorageTracker<Long, EventData> {

  public VirtualMarketsTracker(DataConsumer<Long, EventData> consumer) {
    super(consumer);
  }

  @Trace(dispatcher = true)
  @Override
  public void addSubscription(Subscription<Long, EventData> client) {
    String transactionName = "VirtualMarketsTracker_addSubscription";
    NewRelic.setTransactionName(null, transactionName);
    NewRelic.incrementCounter("Custom/" + transactionName);
    super.addSubscription(client);
  }

  @Trace(dispatcher = true)
  @Override
  public void removeSubscription(String clientId, Long ticket) {
    String transactionName = "VirtualMarketsTracker_removeSubscription";
    NewRelic.setTransactionName(null, transactionName);
    NewRelic.incrementCounter("Custom/" + transactionName);
    super.removeSubscription(clientId, ticket);
  }
}
