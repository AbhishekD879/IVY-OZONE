package com.coral.oxygen.edp.tracking;

/** Created by azayats on 18.12.17. */
public interface Tracker<T, D> {

  void addSubscription(Subscription<T, D> client);

  void removeSubscription(String clientId, T ticket);

  void refreshData();
}
