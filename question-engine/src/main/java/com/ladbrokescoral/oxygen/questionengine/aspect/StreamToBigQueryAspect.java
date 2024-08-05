package com.ladbrokescoral.oxygen.questionengine.aspect;

import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.QuizSubmitDto;
import com.ladbrokescoral.oxygen.questionengine.service.BigQueryStreamingService;
import lombok.RequiredArgsConstructor;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Aspect
@Component
@RequiredArgsConstructor
@ConditionalOnProperty("application.enableBigQueryStreaming")
public class StreamToBigQueryAspect {
  private final BigQueryStreamingService bigQueryStreamingService;

  @Async("streamToBigQueryTaskExecutor")
  @AfterReturning("@annotation(com.ladbrokescoral.oxygen.questionengine.aspect.annotation.StreamToBigQuery) && args(submission, ..)")
  public void streamToBigQuery(QuizSubmitDto submission) throws IOException {
    bigQueryStreamingService.streamUserEntry(submission);
  }
}
