package com.entain.oxygen.betbuilder_middleware.api;

import com.entain.oxygen.betbuilder_middleware.api.request.CheckPriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.request.PriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.response.CheckPriceResponse;
import com.entain.oxygen.betbuilder_middleware.api.response.PriceResponse;
import com.entain.oxygen.betbuilder_middleware.service.BBUtil;
import com.entain.oxygen.betbuilder_middleware.service.PriceService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
public class PriceApi {

  private final PriceService priceService;

  @Autowired
  public PriceApi(PriceService priceService) {
    this.priceService = priceService;
  }

  @PostMapping("/price")
  public Mono<PriceResponse> getPrice(@RequestBody PriceRequest request) {
    return priceService
        .getPrice(request)
        .contextWrite(context -> context.put(BBUtil.LCG_REQUEST, BBUtil.toJson(request)));
  }

  @PostMapping("/checkPrice")
  public Mono<CheckPriceResponse> checkPrice(@Valid @RequestBody CheckPriceRequest request) {
    return priceService
        .getLatestPrices(request)
        .contextWrite(context -> context.put(BBUtil.LCG_REQUEST, BBUtil.toJson(request)));
  }
}
