package com.coral.oxygen.middleware.ms.liveserv.newclient.liveserve;

import java.util.List;

public interface LiveServerListener {
  void onMessage(List<Message> message);

  void onError(Throwable e);
}
