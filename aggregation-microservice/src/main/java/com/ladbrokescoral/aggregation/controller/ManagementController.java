package com.ladbrokescoral.aggregation.controller;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
public class ManagementController {
  @Autowired private ReactiveRedisTemplate<String, byte[]> reactiveRedisImageTemplate;

  @PostMapping("mng/clearAll")
  public Mono<String> clearAllCache() {
    return reactiveRedisImageTemplate
        .getConnectionFactory()
        .getReactiveConnection()
        .serverCommands()
        .flushAll();
  }

  @GetMapping("mng/cache")
  public Mono<List<String>> getCachedKeys(
      @RequestParam(required = false, defaultValue = "*") String pattern) {
    return reactiveRedisImageTemplate.keys(pattern).collectList();
  }

  @PostMapping("mng/clear/silks")
  public Mono<Long> clearSilksByIds(@RequestParam List<String> ids) {
    return Flux.fromIterable(ids)
        .map(id -> String.format("*/%s.gif", id))
        .flatMap(id -> reactiveRedisImageTemplate.keys(id))
        .collectList()
        .flatMap(urls -> reactiveRedisImageTemplate.delete(urls.toArray(new String[] {})))
        .onErrorReturn(0L)
        .defaultIfEmpty(0L);
  }
}
