package com.coral.oxygen.middleware.ms.liveserv;

import com.coral.oxygen.middleware.ms.liveserv.model.messages.EventMessageEnvelope;

/** Created by azayats on 08.05.17. */
public interface MessageHandler {

  void handle(EventMessageEnvelope envelope);
}
