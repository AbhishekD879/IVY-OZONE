package com.ladbrokescoral.aggregation.controller;

import com.ladbrokescoral.aggregation.service.AggregationService;
import java.text.MessageFormat;
import java.util.List;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.ObjectUtils;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;

@Slf4j
@RestController
@RequiredArgsConstructor
public class AggregationController {

  private final AggregationService aggregationService;

  @GetMapping(
      value = {"/silks/{imageProvider}/{ids}", "/silks/{imageProvider}/{version}/{ids}"},
      produces = "image/png")
  public Mono<byte[]> requestImageAggregation(
      @RequestHeader(value = "TestOrigin", required = false) String testOrigin,
      @RequestHeader(value = "Origin", required = false) String origin,
      @RequestHeader(value = "Referer", required = false) String referer,
      ServerWebExchange serverWebExchange,
      @PathVariable String imageProvider,
      @PathVariable(required = false) String version,
      @PathVariable List<String> ids) {
    String requestId = serverWebExchange.getLogPrefix();
    String brand = detectBrand(testOrigin, origin, referer);
    String providerWithBrand = detectProvider(brand, imageProvider, version);
    return aggregationService.imageAggregationByProvider(ids, providerWithBrand, requestId);
  }

  @GetMapping(value = "/silks/racingpost/v3/{eventIds}", produces = "image/gif")
  public Mono<byte[]> requestImageAggregation(
      @RequestHeader(value = "TestOrigin", required = false) String testOrigin,
      @RequestHeader(value = "Origin", required = false) String origin,
      @RequestHeader(value = "Referer", required = false) String referer,
      ServerWebExchange serverWebExchange,
      @PathVariable List<String> eventIds) {
    String requestId = serverWebExchange.getLogPrefix();
    String brand = detectBrand(testOrigin, origin, referer);
    return aggregationService.imageAggregationByBrand(eventIds, brand, requestId);
  }

  private String detectBrand(String testOrigin, String origin, String referer) {
    String host = ObjectUtils.isEmpty(testOrigin) ? detectBrand(origin, referer) : testOrigin;
    return String.valueOf(host).contains("coral.co.uk") ? "coral" : "ladbrokes";
  }

  private String detectBrand(String origin, String referer) {
    return (origin != null) ? origin : referer;
  }

  private String detectProvider(String brand, String provider, String version) {
    return version == null
        ? MessageFormat.format("{0}-{1}", provider, brand)
        : MessageFormat.format("{0}-{1}-{2}", provider, version, brand);
  }
}
