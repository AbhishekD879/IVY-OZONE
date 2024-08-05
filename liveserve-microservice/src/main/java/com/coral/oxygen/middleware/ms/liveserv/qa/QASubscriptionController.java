package com.coral.oxygen.middleware.ms.liveserv.qa;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Created by azayats on 10.05.17. */
@RestController
@ConditionalOnProperty(name = "qa.subscription.enabled")
@RequestMapping(value = "qa/subscription", produces = "application/json")
public class QASubscriptionController {

  private LiveServService liveServService;

  @Autowired
  public void setLiveServService(LiveServService liveServService) {
    this.liveServService = liveServService;
  }

  @GetMapping(value = "add/{channel}")
  public SubscriptionStats subscribe( //
      @PathVariable("channel") String channel //
      ) {
    liveServService.subscribe(channel);
    return liveServService.getSubscriptions().get(channel);
  }

  @GetMapping(value = "remove/{channel}")
  public void unsubscribe( //
      @PathVariable("channel") String channel //
      ) {
    liveServService.unsubscribe(channel);
  }
}
