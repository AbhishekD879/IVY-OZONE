package com.ladbrokescoral.oxygen.timeline.api.config;

import java.util.Arrays;
import java.util.List;
import java.util.stream.StreamSupport;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.text.StringEscapeUtils;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.context.event.EventListener;
import org.springframework.core.env.AbstractEnvironment;
import org.springframework.core.env.EnumerablePropertySource;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class PropertiesPrinter {
  private static final List<String> EXCLUSIONS = Arrays.asList("GCLOUD_PRIVATE_KEY");

  private final AbstractEnvironment environment;

  @EventListener
  public void handleContextRefresh(ContextRefreshedEvent event) {
    String properties =
        StreamSupport.stream(environment.getPropertySources().spliterator(), false)
            .filter(source -> source instanceof EnumerablePropertySource)
            .map(EnumerablePropertySource.class::cast)
            .map(EnumerablePropertySource::getPropertyNames)
            .flatMap(Arrays::stream)
            .distinct()
            .filter(propertyName -> !EXCLUSIONS.contains(propertyName))
            .reduce(
                "Environment Properties: ",
                (collectedProperties, propertyName) ->
                    collectedProperties + formatProperty(propertyName));

    log.info(properties);
  }

  private String formatProperty(String propertyName) {
    return String.format(
        "%s=%s;",
        propertyName, StringEscapeUtils.escapeJava(environment.getProperty(propertyName)));
  }
}
