package com.ladbrokescoral.oxygen.questionengine.job;

import com.ladbrokescoral.oxygen.questionengine.service.BigQueryStreamingService;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
@RequiredArgsConstructor
@ConditionalOnProperty("application.enableBigQueryStreaming")
public class StreamToBigQueryScheduler {
  private final BigQueryStreamingService bigQueryStreamingService;

  @Scheduled(fixedDelayString = "${google-cloud.big-query.streamCmsConfigPeriodMillis}")
  public void streamCmsConfiguration() throws IOException {
    bigQueryStreamingService.streamCmsConfiguration();
  }
  @Scheduled(fixedDelayString = "${google-cloud.big-query.streamResultsPeriodMillis}")
  public void streamResults() throws IOException {
    bigQueryStreamingService.streamResults();
  }
}
