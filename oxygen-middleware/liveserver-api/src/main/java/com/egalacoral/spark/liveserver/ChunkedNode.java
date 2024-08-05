package com.egalacoral.spark.liveserver;

import java.util.Map;

/**
 * @author volodymyr.masliy on 2/28/18
 */
interface ChunkedNode {
  int getChunkSize();

  boolean isMaxChunkSizeReached();

  void subscribe(SubscriptionSubject subject);

  boolean isSubscribedAlready(SubscriptionSubject subject);

  Map<String, SubscriptionSubject> getSubscribedSubjectsMap();

  void compact();

  void clear();

  ChunkedNode getDelegate();
}
