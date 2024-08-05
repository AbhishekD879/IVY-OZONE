package com.ladbrokescoral.reactions.client.cms;

import static com.ladbrokescoral.reactions.exception.ErrorCode.BAD_REQUEST;

import com.fasterxml.jackson.databind.JsonNode;
import com.ladbrokescoral.reactions.config.ReactionPropertiesConfig;
import com.ladbrokescoral.reactions.exception.BadRequestException;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.exception.ServiceUnavailableException;
import java.net.SocketException;
import java.util.List;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.WebClientRequestException;
import org.springframework.web.util.UriComponentsBuilder;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 15-06-2023
 */
@Component
public class DefaultCMSClient implements CMSClient {

  private static final String CMS_SERVICE_UNAVAILABLE = "CMS service is unavailable.";

  private final ReactionPropertiesConfig reactionPropertiesConfig;
  private final WebClient webClient;

  public DefaultCMSClient(
      final ReactionPropertiesConfig reactionPropertiesConfig, final WebClient webClient) {
    this.reactionPropertiesConfig = reactionPropertiesConfig;
    this.webClient = webClient;
  }

  @Override
  public Mono<List<String>> getActiveSelectionIdAndSurfaceBetIdKeys() {

    return webClient
        .get()
        .uri(
            UriComponentsBuilder.fromUriString(reactionPropertiesConfig.getCmsBaseUrl())
                .pathSegment(reactionPropertiesConfig.getCmsSurfaceBetApiPath())
                .build()
                .toUri())
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .onStatus(
            HttpStatus::is4xxClientError,
            clientResponse ->
                Mono.error(
                    new BadRequestException(
                        "Client Error while retrieving CMS sport pages information.", BAD_REQUEST)))
        .onStatus(
            HttpStatus::is5xxServerError,
            clientResponse ->
                Mono.error(
                    new ServiceExecutionException(
                        "Server Error while retrieving CMS sport pages information.")))
        .bodyToMono(new ParameterizedTypeReference<List<String>>() {})
        .doOnError(
            WebClientRequestException.class,
            (Exception timeoutException) -> {
              throw new ServiceUnavailableException(CMS_SERVICE_UNAVAILABLE);
            })
        .doOnError(
            SocketException.class,
            (Exception socketException) -> {
              throw new ServiceUnavailableException(CMS_SERVICE_UNAVAILABLE);
            });
  }

  @Override
  public Mono<JsonNode> getCmsHealth() {

    return webClient
        .get()
        .uri(
            UriComponentsBuilder.fromUriString(reactionPropertiesConfig.getCmsBaseUrl())
                .pathSegment(reactionPropertiesConfig.getCmsHealthApiPath())
                .build()
                .toUri())
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .onStatus(
            HttpStatus::is4xxClientError,
            clientResponse ->
                Mono.error(
                    new BadRequestException(
                        "Client Error while retrieving CMS health information.", BAD_REQUEST)))
        .onStatus(
            HttpStatus::is5xxServerError,
            clientResponse ->
                Mono.error(
                    new ServiceExecutionException(
                        "Server Error while retrieving CMS health information.")))
        .bodyToMono(JsonNode.class)
        .doOnError(
            WebClientRequestException.class,
            (Exception timeoutException) -> {
              throw new ServiceUnavailableException(CMS_SERVICE_UNAVAILABLE);
            })
        .doOnError(
            SocketException.class,
            (Exception socketException) -> {
              throw new ServiceUnavailableException(CMS_SERVICE_UNAVAILABLE);
            });
  }
}
