package com.ladbrokescoral.oxygen.timeline.api.service;

import com.ladbrokescoral.oxygen.timeline.api.model.message.Message;
import com.ladbrokescoral.oxygen.timeline.api.model.message.PostMessage;
import org.springframework.data.domain.Page;

public interface PostMessageService {
  Page<PostMessage> findPage(int page);

  Page<PostMessage> findPageBefore(Message.TimeBasedId id);
}
