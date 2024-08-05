package com.ladbrokescoral.reactions.client.bpp;

import static com.ladbrokescoral.reactions.exception.ErrorCode.BAD_REQUEST;

import com.ladbrokescoral.reactions.client.bpp.dto.BppTokenRequest;
import com.ladbrokescoral.reactions.client.bpp.dto.UserData;
import com.ladbrokescoral.reactions.config.ReactionPropertiesConfig;
import com.ladbrokescoral.reactions.exception.BadRequestException;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.exception.ServiceUnavailableException;
import java.net.SocketException;
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
public class DefaultBppClient implements BppClient {

  private static final String BPP_SERVICE_UNAVAILABLE = "Bpp service is unavailable.";
  public final WebClient webClient;
  private final ReactionPropertiesConfig propertiesConfig;

  public DefaultBppClient(
      final WebClient webClient, final ReactionPropertiesConfig propertiesConfig) {
    this.webClient = webClient;
    this.propertiesConfig = propertiesConfig;
  }

  @Override
  public Mono<UserData> getValidUser(String token) {

    return webClient
        .post()
        .uri(
            UriComponentsBuilder.fromUriString(propertiesConfig.getBppBaseUrl())
                .pathSegment(propertiesConfig.getBppTokenApiPath())
                .build()
                .toUri())
        .contentType(MediaType.APPLICATION_JSON)
        .accept(MediaType.APPLICATION_JSON)
        .bodyValue(new BppTokenRequest(token))
        .retrieve()
        .onStatus(
            HttpStatus::is4xxClientError,
            clientResponse ->
                clientResponse
                    .bodyToMono(String.class)
                    .switchIfEmpty(
                        Mono.defer(
                            () ->
                                Mono.error(
                                    new BadRequestException(
                                        "Client Error while retrieving bpp user information: "
                                            + clientResponse.statusCode().name(),
                                        BAD_REQUEST))))
                    .flatMap(
                        errorMsg ->
                            Mono.error(
                                new BadRequestException(
                                    "Client Error while retrieving bpp user information: "
                                        + clientResponse.statusCode().name()
                                        + "  "
                                        + errorMsg,
                                    BAD_REQUEST))))
        .onStatus(
            HttpStatus::is5xxServerError,
            clientResponse ->
                Mono.error(
                    new ServiceExecutionException(
                        "Server Error while retrieving bpp user information.")))
        .bodyToMono(UserData.class)
        .doOnError(
            WebClientRequestException.class,
            (Exception timeoutException) -> {
              throw new ServiceUnavailableException(BPP_SERVICE_UNAVAILABLE, timeoutException);
            })
        .doOnError(
            SocketException.class,
            (Exception socketException) -> {
              throw new ServiceUnavailableException(BPP_SERVICE_UNAVAILABLE, socketException);
            });
  }
}
