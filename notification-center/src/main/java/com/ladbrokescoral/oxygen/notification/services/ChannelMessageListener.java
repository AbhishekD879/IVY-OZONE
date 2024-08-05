package com.ladbrokescoral.oxygen.notification.services;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.redis.connection.Message;
import org.springframework.data.redis.connection.MessageListener;
import org.springframework.stereotype.Service;

@Slf4j
@Data
@Service
public class ChannelMessageListener implements MessageListener {

  private LiveServService liveService;

  public void onMessage(Message message, byte[] pattern) {
    logger.info(message.toString());
    liveService.subscribe(message.toString());
  }
}
