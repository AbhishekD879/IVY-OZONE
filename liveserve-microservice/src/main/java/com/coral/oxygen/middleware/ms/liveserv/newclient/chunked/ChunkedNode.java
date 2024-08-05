package com.coral.oxygen.middleware.ms.liveserv.newclient.chunked;

import com.coral.oxygen.middleware.ms.liveserv.newclient.LiveUpdatesChannel;
import java.util.Map;

/**
 * @author volodymyr.masliy on 2/28/18
 */
interface ChunkedNode {
  int getChunkSize();

  boolean isMaxChunkSizeReached();

  void subscribe(LiveUpdatesChannel subject);

  void unsubscribe(LiveUpdatesChannel subject);

  boolean isSubscribedAlready(LiveUpdatesChannel subject);

  Map<String, LiveUpdatesChannel> getSubscribedSubjectsMap();

  void compact();

  void clear();

  ChunkedNode getDelegate();
}
