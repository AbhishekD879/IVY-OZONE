package com.ladbrokescoral.oxygen.cms.api.service.impl;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.cms.configuration.CloudFlareConfig;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import com.newrelic.api.agent.NewRelic;
import java.io.IOException;
import java.util.Optional;
import java.util.Set;
import lombok.Builder;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;

@Slf4j
@RequiredArgsConstructor
@Component
public class CloudFlareClient {

  public static final String SERVICE_NAME = "CloudFlare";
  public static final String SERVICE_NAME_CACHE_TAG = "CloudFlare-CacheTag";
  public static final String PURGE_CACHE_PATH = "zones/%s/purge_cache";

  private final CloudFlareConfig config;

  @Qualifier("okHttpClient")
  private final OkHttpClient httpClient;

  private final ObjectMapper mapper;

  public Optional<InvalidateCacheResult> invalidate(String zoneId, Set<String> paths) {
    log.info("Sending purge_cache requests for paths {}", paths);
    try (Response response =
        doPost(
            PathUtil.concatUri(config.getEndpoint(), String.format(PURGE_CACHE_PATH, zoneId)),
            InvalidateRequest.builder().files(paths).build())) {
      String responseBody = response.body().string();
      log.info("Fast purge status: {}", responseBody);
      return Optional.of(
          new InvalidateCacheResult(response.code(), responseBody, SERVICE_NAME, paths));
    } catch (IOException e) {
      NewRelic.noticeError(e);
      log.error("Failed to invalidate cache", e);
      return Optional.of(
          new InvalidateCacheResult(
              HttpStatus.INTERNAL_SERVER_ERROR.value(), e.getMessage(), SERVICE_NAME, paths));
    }
  }

  public Optional<InvalidateCacheResult> invalidateCacheTags(String zoneId, Set<String> tags) {
    log.info("Sending purge_cache requests for Cache Tags {}", tags);
    try (Response response =
        doPost(
            PathUtil.concatUri(config.getEndpoint(), String.format(PURGE_CACHE_PATH, zoneId)),
            InvalidateRequest.builder().tags(tags).build())) {
      String responseBody = response.body().string();
      log.info("Fast purge status: {}", responseBody);
      return Optional.of(
          new InvalidateCacheResult(response.code(), responseBody, SERVICE_NAME_CACHE_TAG, tags));
    } catch (IOException e) {
      NewRelic.noticeError(e);
      log.error("Failed to invalidate cache", e);
      return Optional.of(
          new InvalidateCacheResult(
              HttpStatus.INTERNAL_SERVER_ERROR.value(),
              e.getMessage(),
              SERVICE_NAME_CACHE_TAG,
              tags));
    }
  }

  private Response doPost(String purgeCacheUrl, InvalidateRequest invalidateRequest)
      throws IOException {
    Request request =
        new Request.Builder()
            .url(purgeCacheUrl)
            .addHeader(HttpHeaders.AUTHORIZATION, config.getToken())
            .post(
                RequestBody.create(
                    okhttp3.MediaType.parse(MediaType.APPLICATION_JSON_VALUE),
                    mapper.writeValueAsString(invalidateRequest)))
            .build();
    return httpClient.newCall(request).execute();
  }

  @Data
  @JsonInclude(JsonInclude.Include.NON_NULL)
  @Builder
  static class InvalidateRequest {
    private Set<String> files;
    private Set<String> tags;
  }
}
