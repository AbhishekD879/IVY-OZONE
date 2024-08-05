package com.coral.oxygen.middleware.ms.quickbet;

import java.util.Collection;

/** Created by azayats on 11.10.17. */
public interface SessionListener {

  void subscribeToRooms(Collection<String> names);

  void unsubscribeFromRooms(Collection<String> names);

  void sendData(String message, Object data);
}
