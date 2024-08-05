package com.entain.oxygen.betbuilder_middleware.service.helper;

import com.entain.oxygen.betbuilder_middleware.api.request.CheckPriceRequest;
import com.entain.oxygen.betbuilder_middleware.api.request.SelectionStatus;
import com.entain.oxygen.betbuilder_middleware.api.response.AggPrice;
import com.entain.oxygen.betbuilder_middleware.api.response.CheckPriceResponse;
import com.entain.oxygen.betbuilder_middleware.api.response.FractionalOdds;
import com.entain.oxygen.betbuilder_middleware.api.response.PriceOdds;
import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceResponse;
import com.entain.oxygen.betbuilder_middleware.bpg.model.Price;
import com.entain.oxygen.betbuilder_middleware.redis.dto.CombinationCache;
import com.entain.oxygen.betbuilder_middleware.service.BBUtil;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;

@Component
public class PriceServiceHelper {
  private static final String SUCCESS = "success";
  private static final Integer STATUS_CODE = 9;
  private static final String STATUS_MESSAGE = "Invalid Hash";
  /**
   * Builds the CheckPrice response In case of errors for any combination, PG would not return the
   * hash for that particular combination,In such cases We rely on the request for the hash to
   * populate the response
   */
  public CheckPriceResponse buildResponse(
      CheckPriceRequest request,
      BPGPriceResponse bpgPriceResponse,
      Map<String, CombinationCache> comboMap) {
    MDC.put(BBUtil.LCG_REQUEST_KEY, BBUtil.toJson(request));
    CheckPriceResponse checkPriceResponse = new CheckPriceResponse();
    checkPriceResponse.setTransId(request.getTransId());
    /* In case no hash in the request is present in the Redis, status code 9 with status message
    'Invalid Hash' is formed */
    if (CollectionUtils.isEmpty(comboMap))
      handleResponseWhenHashesAreNotPresent(request, checkPriceResponse);
    else {
      List<AggPrice> prices =
          bpgPriceResponse.getPrices().stream()
              .map(price -> (buildPrice(price, comboMap)))
              .collect(Collectors.toList());

      /* If there are any hashes , for which no combination has been returned by
      Redis(invalid hashes)
      Identify those hashes and build the error response for those hashes */
      if (comboMap.size() != request.getCombinations().size()) {
        List<AggPrice> invalidHashPrices =
            request.getCombinations().stream()
                .filter(combination -> !(comboMap.containsKey(combination.getBbHash())))
                .map(combination -> (buildErrorPrice(combination.getBbHash())))
                .toList();
        prices.addAll(invalidHashPrices);
      }
      checkPriceResponse.setPrices(prices);
    }
    return checkPriceResponse;
  }

  private void handleResponseWhenHashesAreNotPresent(
      CheckPriceRequest request, CheckPriceResponse checkPriceResponse) {
    List<AggPrice> prices =
        request.getCombinations().stream()
            .map(combo -> (buildErrorPrice(combo.getBbHash())))
            .toList();
    checkPriceResponse.setPrices(prices);
  }

  // Build Price for invalid hashes(Hashes for which no combination is returned by the Redis)
  private AggPrice buildErrorPrice(String hash) {
    AggPrice aggPrice = new AggPrice();
    aggPrice.setBbHash(hash);
    aggPrice.setStatusCode(STATUS_CODE);
    aggPrice.setStatusMessage(STATUS_MESSAGE);
    return aggPrice;
  }

  private AggPrice buildPrice(Price price, Map<String, CombinationCache> comboMap) {
    AggPrice aggPrice = new AggPrice();
    if (StringUtils.hasText(price.getSgpId())) {
      aggPrice.setBbHash(price.getSgpId());
    } else {
      /* Below logic is to retreive the hash from the Redis Combination Object
      For a combination,If the hash is not present(error scenario) in the PG response, compare
      the combination Id of the PG response and the
      combination id from the redis, when they match,
      retreive the hash from the redis Combination and populate the same in the response*/

      comboMap
          .keySet()
          .forEach(
              (String hash) ->
                  comboMap
                      .entrySet()
                      .forEach(
                          (Map.Entry<String, CombinationCache> combo) -> {
                            if (combo.getValue().getId().equals(price.getCombinationId())) {
                              aggPrice.setBbHash(combo.getValue().getHash());
                            }
                          }));
    }
    aggPrice.setStatusCode(price.getStatus());
    aggPrice.setStatusMessage(price.getStatus() == 1 ? SUCCESS : price.getErrorMessage());
    aggPrice.setSuspState(
        price.getSuspensionState() == 1 ? SelectionStatus.ACTIVE : SelectionStatus.SUSPENDED);
    aggPrice.setPrice(buildOdds(price));
    return aggPrice;
  }

  private PriceOdds buildOdds(Price price) {
    PriceOdds priceOdds = new PriceOdds();
    if (price.getOdds() != null) {
      priceOdds.setDecimal(price.getOdds().getDecimal());
      priceOdds.setFractional(buildFractionalOdds(price));
    }
    return priceOdds;
  }

  private FractionalOdds buildFractionalOdds(Price price) {
    FractionalOdds fractional = null;
    if (price.getOdds().getFractional() != null) {
      fractional = new FractionalOdds();
      fractional.setNum(price.getOdds().getFractional().getNumerator());
      fractional.setDen(price.getOdds().getFractional().getDenominator());
    }
    return fractional;
  }
}
