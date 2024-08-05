package com.coral.oxygen.middleware.featured.controller;

import com.coral.oxygen.middleware.featured.service.FeaturedDataService;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(value = "/api/featured")
@ConditionalOnProperty(name = "featured.scheduled.task.enabled")
public class FeaturedDataController {

  private final FeaturedDataService service;

  @Autowired
  public FeaturedDataController(FeaturedDataService service) {
    this.service = service;
  }

  @Cacheable(
      value = "getStructureById",
      key = "{ #root.methodName, #id }",
      unless = "#result == null")
  @GetMapping("/structure/{id}")
  public String structureById(@PathVariable("id") String id) {
    return service.getStructureById(id);
  }

  @GetMapping(value = "/generation", produces = MediaType.APPLICATION_JSON_VALUE)
  public String version() {
    return service.getVersion();
  }

  @Cacheable(value = "getModuleById", key = "{ #root.methodName, #id }", unless = "#result == null")
  @GetMapping("/module/{id}")
  public String moduleById(@PathVariable("id") String id) {
    return service.getModuleById(id);
  }

  @Cacheable(
      value = "getModuleByIdAndVersion",
      key = "{ #root.methodName, #id, #version }",
      unless = "#result == null")
  @GetMapping("/module/{id}/{version}")
  public String moduleById(@PathVariable("id") String id, @PathVariable("version") String version) {
    return service.getModuleByIdAndVersion(id, version);
  }

  @Cacheable(
      value = "getModuleByIdAndVersion",
      key = "{ #root.methodName, #id, #version }",
      unless = "#result == null")
  @GetMapping("/modules/{version}")
  public String modulesByVersion(
      @RequestParam(value = "ids") Set<String> moduleIds, @PathVariable("version") String version) {
    return moduleIds.stream()
        .map(id -> service.getModuleByIdAndVersion(id, version))
        .filter(m -> !Objects.isNull(m))
        .collect(Collectors.joining(",", "[", "]"));
  }

  @Cacheable(
      value = "getTopics",
      key = "{ #root.methodName, #id, #version }",
      unless = "#result == null")
  @GetMapping("/topics/{id}/{version}")
  public String topics(@PathVariable("id") String id, @PathVariable("version") String version) {
    return service.getTopics(id, version);
  }

  @Cacheable(value = "getSportPages", key = "{ #root.methodName }", unless = "#result == null")
  @GetMapping("/sport-pages")
  public String sportPages() {
    return service.getSportPages();
  }
}
