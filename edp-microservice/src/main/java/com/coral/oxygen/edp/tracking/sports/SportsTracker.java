package com.coral.oxygen.edp.tracking.sports;

import com.coral.oxygen.edp.tracking.DataConsumer;
import com.coral.oxygen.edp.tracking.NoStorageTracker;
import com.coral.oxygen.edp.tracking.Subscription;
import com.coral.oxygen.edp.tracking.UpdateScheduler;
import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class SportsTracker extends NoStorageTracker<String, List<CategoryToUpcomingEvent>> {

  @Autowired
  public SportsTracker(
      DataConsumer<String, List<CategoryToUpcomingEvent>> consumer,
      UpdateScheduler updateScheduler) {
    super(consumer);
    updateScheduler.setTracker(this);
  }

  @Trace(dispatcher = true)
  @Override
  public void addSubscription(Subscription<String, List<CategoryToUpcomingEvent>> client) {
    String transactionName = "SportsTracker_addSubscription";
    NewRelic.setTransactionName(null, transactionName);
    NewRelic.incrementCounter("Custom/" + transactionName);
    super.addSubscription(client);
  }

  @Trace(dispatcher = true)
  @Override
  public void removeSubscription(String clientId, String ticket) {
    String transactionName = "SportsTracker_removeSubscription";
    NewRelic.setTransactionName(null, transactionName);
    NewRelic.incrementCounter("Custom/" + transactionName);
    // since subscribers are stored by client id, we need to use clientId for removal as well
    super.removeSubscription(clientId, clientId);
  }
}
