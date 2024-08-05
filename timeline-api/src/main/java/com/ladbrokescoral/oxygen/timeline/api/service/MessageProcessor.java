package com.ladbrokescoral.oxygen.timeline.api.service;

import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;

public interface MessageProcessor<M extends Message> {
  void process(M message);
}
