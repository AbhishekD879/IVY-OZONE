package com.ladbrokescoral.oxygen.questionengine.listeners;

import com.ladbrokescoral.oxygen.event.ConfigMapEvent;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ApplicationListener;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.Map;

@Profile("!INTEGRATION-TEST")
@Component
@RequiredArgsConstructor
@Slf4j
public class CmsConfigEventListener implements ApplicationListener<ConfigMapEvent> {

  private final Map<String, List<String>> configMap;

  @Override
  public void onApplicationEvent(ConfigMapEvent event) {
    log.info("Received ConfigMapEvent - " + event.getConfigMap());
    configMap.putAll(event.getConfigMap());
  }
}
