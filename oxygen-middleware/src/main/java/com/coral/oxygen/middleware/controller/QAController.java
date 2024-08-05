package com.coral.oxygen.middleware.controller;

import com.coral.oxygen.middleware.featured.service.impl.InplayDataRestService;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.egalacoral.spark.liveserver.Message;
import com.egalacoral.spark.liveserver.Subscriber;
import com.egalacoral.spark.liveserver.SubscriptionSubject;
import com.egalacoral.spark.liveserver.service.LiveServerSubscriptionsQAStorage;
import java.util.Map;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RequiredArgsConstructor
@RestController
@RequestMapping(value = "/api/qa")
public class QAController {

  private final LiveServerSubscriptionsQAStorage liveServerStorageService;
  private final Subscriber liveServerSubscriber;
  private final InplayDataRestService inplayDataRestService;

  @GetMapping("/liveserver/messages")
  public Map<String, Message> getMessages() {
    return liveServerStorageService.getMessages();
  }

  @GetMapping("liveserver/payload")
  public Map getLiveserverPayload() {
    return liveServerSubscriber.getPayloadItems();
  }

  @GetMapping("/inplay")
  public InPlayData getinplaydata(@RequestParam String version) {
    return inplayDataRestService.getInplayData(version);
  }

  @GetMapping("/liveserver/subscriptions")
  public Map<String, SubscriptionSubject> getSubscriptions() {
    return liveServerStorageService.getSubscriptions();
  }
}
