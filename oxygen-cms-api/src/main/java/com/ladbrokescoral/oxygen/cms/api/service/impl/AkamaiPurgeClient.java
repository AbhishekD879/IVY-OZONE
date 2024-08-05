package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.akamai.edgegrid.signer.ClientCredential;
import com.akamai.edgegrid.signer.googlehttpclient.GoogleHttpClientEdgeGridRequestSigner;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.api.client.http.ByteArrayContent;
import com.google.api.client.http.GenericUrl;
import com.google.api.client.http.HttpRequest;
import com.google.api.client.http.HttpRequestFactory;
import com.google.api.client.http.HttpResponse;
import com.google.api.client.http.apache.ApacheHttpTransport;
import com.ladbrokescoral.oxygen.cms.api.entity.CCUPurgeRequest;
import com.ladbrokescoral.oxygen.cms.configuration.AkamaiFastPurgeConfig;
import com.newrelic.api.agent.NewRelic;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class AkamaiPurgeClient {
  private final AkamaiFastPurgeConfig config;
  private final ObjectMapper mapper;
  private final Set<String> purgeCodes;

  @Autowired
  public AkamaiPurgeClient(AkamaiFastPurgeConfig config, ObjectMapper mapper) {
    this.config = config;
    this.mapper = mapper;
    this.purgeCodes = Arrays.stream(config.getCpCode()).collect(Collectors.toSet());
  }

  public List<Optional<InvalidateCacheResult>> invalidateAll() {
    return Stream.of(instantiateHttpRequest().map(this::signHttpRequest).map(this::execute))
        .collect(Collectors.toList());
  }
  /** Take a look: https://developer.akamai.com/api/core_features/fast_purge/v3.html */
  private Optional<HttpRequest> instantiateHttpRequest() {
    try {
      HttpRequestFactory requestFactory = new ApacheHttpTransport().createRequestFactory();
      URI uri =
          new URI(
              config.getScheme(), config.getHost(), config.getInvalidateCpCodePath(), null, null);
      CCUPurgeRequest ccuPurgeRequest = CCUPurgeRequest.builder().objects(purgeCodes).build();
      HttpRequest request =
          requestFactory.buildPostRequest(
              new GenericUrl(uri),
              ByteArrayContent.fromString(
                  "application/json", mapper.writeValueAsString(ccuPurgeRequest)));
      request.getHeaders().set("Host", config.getHost());
      return Optional.of(request);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Error creating http request", e);
      return Optional.empty();
    }
  }

  private HttpRequest signHttpRequest(HttpRequest request) {
    ClientCredential credential =
        new ClientCredential.ClientCredentialBuilder()
            .clientToken(config.getClientToken())
            .accessToken(config.getAccessToken())
            .clientSecret(config.getClientSecret())
            .host(config.getHost())
            .build();
    GoogleHttpClientEdgeGridRequestSigner signer =
        new GoogleHttpClientEdgeGridRequestSigner(credential);
    try {
      signer.sign(request);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Error signing http request", e);
    }
    return request;
  }

  private InvalidateCacheResult execute(HttpRequest request) {
    try {
      HttpResponse response = request.execute();
      String responseBody = readContent(response.getContent());
      log.info("Fast purge status: {}", responseBody);
      return new InvalidateCacheResult(
          response.getStatusCode(), responseBody, "Akamai", purgeCodes);
    } catch (Exception e) {
      NewRelic.noticeError(e);
      log.error("Error during fast purge request with exception", e);
      return new InvalidateCacheResult(
          HttpStatus.INTERNAL_SERVER_ERROR.value(), e.getMessage(), "Akamai", purgeCodes);
    }
  }

  private String readContent(InputStream responseStream) throws IOException {
    try (BufferedReader br =
        new BufferedReader(new InputStreamReader(responseStream, StandardCharsets.UTF_8))) {
      return br.lines().collect(Collectors.joining(System.lineSeparator()));
    }
  }
}
