package com.entain.oxygen.betbuilder_middleware.bpg.client;

import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceRequest;
import com.entain.oxygen.betbuilder_middleware.bpg.model.BPGPriceResponse;
import com.entain.oxygen.betbuilder_middleware.exception.BetBuilderException;
import com.entain.oxygen.betbuilder_middleware.exception.PGConnectivityException;
import com.entain.oxygen.betbuilder_middleware.exception.PricingGatewayException;
import com.entain.oxygen.betbuilder_middleware.service.BBUtil;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.jboss.logging.MDC;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.util.context.ContextView;

@Service
public class PricingGatewayClient {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger();

  private final WebClient webClient;

  @Autowired
  public PricingGatewayClient(@Qualifier("pricingGatewayWebClient") WebClient webClient) {
    this.webClient = webClient;
  }

  public Mono<BPGPriceResponse> getPrice(BPGPriceRequest request) {
    return Mono.deferContextual(
            (ContextView contextView) -> {
              String correlationId = contextView.get(BBUtil.CORRELATION_ID);
              String bpgRequest = request != null ? BBUtil.toJson(request) : "";
              return webClient
                  .post()
                  .uri(uriBuilder -> uriBuilder.path("v2/pricing").build())
                  .contentType(MediaType.APPLICATION_JSON)
                  .accept(MediaType.APPLICATION_JSON)
                  .body(Mono.just(request), BPGPriceRequest.class)
                  .header(BBUtil.X_CORRELATION_ID, correlationId)
                  .exchangeToMono(
                      (ClientResponse clientResponse) -> {
                        setMDC(contextView, correlationId, bpgRequest);
                        return buildResponse(clientResponse);
                      })
                  .doOnError(
                      (Throwable error) -> {
                        setMDC(contextView, correlationId, bpgRequest);
                        ASYNC_LOGGER.error("PG Exception - {} -{} ", error, error.getMessage());
                        Mono.error(error);
                      })
                  .doFinally(signal -> MDC.clear());
            })
        .doFinally(signalType -> MDC.clear());
  }

  private static void setMDC(ContextView contextView, String correlationId, String bpgRequest) {
    MDC.put(BBUtil.CORRELATION_ID, correlationId);
    MDC.put(BBUtil.TRANSACTION_PATH, contextView.get(BBUtil.TRANSACTION_PATH));
    MDC.put(BBUtil.LCG_REQUEST_KEY, contextView.get(BBUtil.LCG_REQUEST));
    MDC.put(BBUtil.BPG_REQUEST_KEY, bpgRequest);
  }

  private Mono<BPGPriceResponse> buildResponse(ClientResponse response) {

    if (response.statusCode().is2xxSuccessful()) {
      return response
          .bodyToMono(BPGPriceResponse.class)
          .doOnNext(
              (BPGPriceResponse bpgResponse) -> {
                MDC.put(BBUtil.BPG_RESPONSE_KEY, BBUtil.toJson(bpgResponse));
                MDC.put(BBUtil.BPG_STATUS_KEY, "SUCCESS");
                if (bpgResponse.getPrices().stream()
                    .anyMatch(price -> price.getErrorCode() != 0 || price.getSgpId().isEmpty())) {
                  MDC.put(BBUtil.BPG_STATUS_KEY, "BUSINESS ERROR");
                }
              });
    } else if (response.statusCode().is5xxServerError()) {
      if (response.statusCode() == HttpStatus.SERVICE_UNAVAILABLE) {

        throw new PGConnectivityException("Pricing Gateway Connectivity Failed.");
      } else {
        throw new PricingGatewayException(
            "Pricing Gateway error. Please try again after sometime.");
      }
    } else if (response.statusCode().is4xxClientError()) {
      throw new IllegalArgumentException("Invalid Pricing Gateway Request");
    } else {
      throw new BetBuilderException("Unknown error while calling Pricing Gateway.");
    }
  }
}
