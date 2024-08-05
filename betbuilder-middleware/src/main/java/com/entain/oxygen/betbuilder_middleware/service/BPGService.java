package com.entain.oxygen.betbuilder_middleware.service;

import com.entain.oxygen.betbuilder_middleware.api.request.CheckPriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.request.PriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.response.CheckPriceResponse;
import com.entain.oxygen.betbuilder_middleware.api.response.PriceResponse;
import com.entain.oxygen.betbuilder_middleware.bpg.client.PricingGatewayClient;
import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceRequest;
import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceResponse;
import com.entain.oxygen.betbuilder_middleware.bpg.model.Combination;
import com.entain.oxygen.betbuilder_middleware.bpg.model.Price;
import com.entain.oxygen.betbuilder_middleware.redis.dto.CombinationCache;
import com.entain.oxygen.betbuilder_middleware.service.helper.PriceServiceHelper;
import java.util.Map;
import java.util.function.Function;
import org.jboss.logging.MDC;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import reactor.core.publisher.Mono;

@Service
public class BPGService {
  private final ModelMapper modelMapper;
  private final PricingGatewayClient pricingGatewayClient;
  private final PriceServiceHelper priceServiceHelper;

  @Autowired
  public BPGService(
      ModelMapper modelMapper,
      PricingGatewayClient pricingGatewayClient,
      PriceServiceHelper priceServiceHelper) {
    this.modelMapper = modelMapper;
    this.pricingGatewayClient = pricingGatewayClient;
    this.priceServiceHelper = priceServiceHelper;
  }

  public Mono<PriceResponse> getPrice(PriceRequest request) {
    BPGPriceRequest bpgPriceRequest = transformRequest(request, BPGPriceRequest.class);
    return transformResponse(pricingGatewayClient.getPrice(bpgPriceRequest));
  }

  public Function<Map<String, CombinationCache>, Mono<CheckPriceResponse>> getLatestPrices(
      CheckPriceRequest request, String correlationId) {
    return (Map<String, CombinationCache> combination) -> {
      MDC.put(BBUtil.CORRELATION_ID, correlationId);
      if (CollectionUtils.isEmpty(combination)) {
        return Mono.just(priceServiceHelper.buildResponse(request, null, null));
      } else {
        return getLatestPriceFromPG(request, combination);
      }
    };
  }

  public BPGPriceRequest transformRequest(PriceRequest request, Class<BPGPriceRequest> clazz) {
    return modelMapper.map(request, clazz);
  }

  private Mono<PriceResponse> transformResponse(Mono<BPGPriceResponse> price) {
    return price.map(bpgPriceResponse -> modelMapper.map(bpgPriceResponse, PriceResponse.class));
  }

  private Mono<CheckPriceResponse> getLatestPriceFromPG(
      CheckPriceRequest request, Map<String, CombinationCache> combination) {
    return pricingGatewayClient
        .getPrice(buildPGRequest(combination))
        .map(
            (BPGPriceResponse response) -> {
              response
                  .getPrices()
                  .forEach(
                      (Price price) -> {
                        if (price.getSuspensionState() == null) {
                          price.setSuspensionState(1);
                        }
                      });
              return priceServiceHelper.buildResponse(request, response, combination);
            });
  }

  private BPGPriceRequest buildPGRequest(Map<String, CombinationCache> combination) {
    BPGPriceRequest bpgPriceRequest = new BPGPriceRequest();
    bpgPriceRequest.setBatchId("LCG-BB-BATCH-" + System.currentTimeMillis());
    bpgPriceRequest
        .getCombinations()
        .addAll(combination.values().stream().map(this::tranformCombination).toList());
    return bpgPriceRequest;
  }

  private Combination tranformCombination(CombinationCache combinationCache) {
    return modelMapper.map(combinationCache, Combination.class);
  }
}
