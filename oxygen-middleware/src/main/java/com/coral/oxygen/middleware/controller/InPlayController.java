package com.coral.oxygen.middleware.controller;

import com.coral.oxygen.middleware.in_play.service.InPlayStorageService;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.google.gson.Gson;
import java.util.Collection;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@Slf4j
@RestController
@RequestMapping(value = "/api/debug/inplay")
@ConditionalOnProperty(name = "rest.testing.enabled")
public class InPlayController {

  private final InPlayStorageService storageService;
  private final Gson gson;

  @Autowired
  public InPlayController(InPlayStorageService storageService, Gson gson) {
    this.storageService = storageService;
    this.gson = gson;
  }

  @GetMapping
  public String getData() {
    log.info("GET latest inplay data");
    return String.valueOf(storageService.getLatestInPlayData());
  }

  @GetMapping("/LatestSportsRibbon")
  public String getLatestSportsRibbon() {
    return String.valueOf(storageService.getLatestSportsRibbon());
  }

  @GetMapping("/LatestSportSegment")
  public String getLatestSportSegment(@RequestParam("key") String key) {
    String latestSportSegment = storageService.getLatestSportSegment(key);
    return String.valueOf(latestSportSegment);
  }

  @GetMapping("/AllLastSportSegmets")
  public String getAllLastSportSegmets() {
    Collection<SportSegment> latestSportSegmentsObjects =
        storageService.getLatestSportSegmentsObjects();
    return String.valueOf(gson.toJson(latestSportSegmentsObjects));
  }
}
