package com.coral.oxygen.middleware.ms.liveserv.controllers;

import com.coral.oxygen.middleware.ms.liveserv.LiveServService;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** Created by azayats on 10.05.17. */
@RestController
@RequestMapping(value = "subscription", produces = "application/json")
public class SubscriptionController {

  private LiveServService liveServService;

  @Autowired
  public void setLiveServService(LiveServService liveServService) {
    this.liveServService = liveServService;
  }

  @GetMapping(value = "all")
  public Map<String, SubscriptionStats> getAll() {
    return liveServService.getSubscriptions();
  }

  @GetMapping(value = "{channel}")
  public SubscriptionStats getByChannel( //
      @PathVariable("channel") String channel //
      ) {
    return liveServService.getSubscriptions().get(channel);
  }
}
