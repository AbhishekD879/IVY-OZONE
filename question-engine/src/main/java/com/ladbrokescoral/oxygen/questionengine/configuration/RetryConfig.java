package com.ladbrokescoral.oxygen.questionengine.configuration;

import lombok.RequiredArgsConstructor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.retry.RetryCallback;
import org.springframework.retry.RetryContext;
import org.springframework.retry.RetryListener;
import org.springframework.retry.listener.RetryListenerSupport;
import org.springframework.retry.support.RetryTemplate;

import java.util.Collections;
import java.util.List;

@Configuration
@RequiredArgsConstructor
public class RetryConfig {

  @Bean
  public RetryTemplate retryTemplate() {
    return new RetryTemplate();
  }

  @Bean
  public List<RetryListener> retryListeners() {
    return Collections.singletonList(new RetryListenerSupport() {
      private final Logger log = LoggerFactory.getLogger(getClass());

      @Override
      public <T, E extends Throwable> void onError(
          RetryContext context, RetryCallback<T, E> callback, Throwable throwable) {
        log.error(
            "Retryable method '{}' an exception: '{}'. Retry count: '{}'. Stacktrace: {}",
            context.getAttribute("context.name"),
            throwable,
            context.getRetryCount(),
            throwable.getStackTrace()
        );
      }
    });
  }

}
