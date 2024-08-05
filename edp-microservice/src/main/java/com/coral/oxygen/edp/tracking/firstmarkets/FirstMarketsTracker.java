package com.coral.oxygen.edp.tracking.firstmarkets;

import com.coral.oxygen.edp.tracking.AbstractTracker;
import com.coral.oxygen.edp.tracking.DataConsumer;
import com.coral.oxygen.edp.tracking.DataStorage;
import com.coral.oxygen.edp.tracking.Subscription;
import com.coral.oxygen.edp.tracking.model.FirstMarketsData;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

/** Created by azayats on 18.12.17. */
@Component
public class FirstMarketsTracker extends AbstractTracker<Long, FirstMarketsData> {

  public FirstMarketsTracker(
      DataStorage<Long, FirstMarketsData> storage, DataConsumer<Long, FirstMarketsData> consumer) {
    super(storage, consumer, new FirstMarketsChangeDetector());
  }

  @Scheduled(cron = "${edp.firstmarkets.refresh.data.cron.expression}", zone = "${time.zone}")
  @Override
  public void refreshData() {
    super.refreshData();
  }

  @Trace(dispatcher = true)
  @Override
  public void addSubscription(Subscription<Long, FirstMarketsData> client) {
    String transactionName = "FirstMarketsTracker_addSubscription";
    NewRelic.setTransactionName(null, transactionName);
    NewRelic.incrementCounter("Custom/" + transactionName);
    super.addSubscription(client);
  }

  @Trace(dispatcher = true)
  @Override
  public void removeSubscription(String clientId, Long ticket) {
    String transactionName = "FirstMarketsTracker_removeSubscription";
    NewRelic.setTransactionName(null, transactionName);
    NewRelic.incrementCounter("Custom/" + transactionName);
    super.removeSubscription(clientId, ticket);
  }
}
