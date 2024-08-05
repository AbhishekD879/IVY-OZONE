package com.coral.oxygen.middleware.controller;

import com.coral.oxygen.middleware.in_play.service.InplayDataService;
import com.coral.oxygen.middleware.in_play.service.model.InPlayCache;
import com.coral.oxygen.middleware.pojos.model.cms.VirtualSportEvents;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportsRibbon;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "/api/inplay")
@ConditionalOnProperty(name = "inplay.scheduled.task.enabled")
public class InplayDataController {

  private final InplayDataService service;

  @Autowired
  public InplayDataController(InplayDataService service) {
    this.service = service;
  }

  @Cacheable(value = "getGeneration", unless = "#result == null")
  @GetMapping("/generation")
  public String getGeneration() {
    return service.getGeneration();
  }

  @Cacheable(
      value = "getInPlayModel",
      key = "{ #root.methodName, #version }",
      unless = "#result == null")
  @GetMapping("model/{version}")
  public InPlayData getInPlayModel(@PathVariable("version") String version) {
    return service.getInPlayModel(version);
  }

  @Cacheable(
      value = "getSportsRibbon",
      key = "{ #root.methodName, #version }",
      unless = "#result == null")
  @GetMapping("sportsribbon/{version}")
  public SportsRibbon getSportsRibbon(@PathVariable("version") String version) {
    return service.getSportsRibbon(version);
  }

  @Cacheable(
      value = "getInPlayCache",
      key = "{ #root.methodName, #version }",
      unless = "#result == null")
  @GetMapping("cache/{version}")
  public InPlayCache getInPlayCache(@PathVariable("version") String version) {
    return service.getInPlayCache(version);
  }

  @Cacheable(
      value = "getSportSegment",
      key = "{ #root.methodName, #storageKey }",
      unless = "#result == null")
  @GetMapping("sportsegment/{storageKey}")
  public SportSegment getSportSegment(@PathVariable("storageKey") String storageKey) {
    return service.getSportSegment(storageKey);
  }

  @Cacheable(
      value = "getVirtualSportData",
      key = "{ #root.methodName,#storageKey}",
      unless = "#result == null")
  @GetMapping("virtuals/{storageKey}")
  public List<VirtualSportEvents> getVirtualSportData(
      @PathVariable("storageKey") String storageKey) {
    return service.getVirtualSportData(storageKey);
  }
}
