package com.ladbrokescoral.oxygen.questionengine.listeners;

import com.ladbrokescoral.oxygen.event.PublicApiEvent;
import com.ladbrokescoral.oxygen.model.ApiCollectionConfig;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.service.CmsService;
import java.util.*;
import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.ApplicationListener;
import org.springframework.context.annotation.Profile;
import org.springframework.stereotype.Component;
import org.springframework.util.CollectionUtils;

@Profile("!INTEGRATION-TEST")
@Component
@RequiredArgsConstructor
@Slf4j
public class CmsQuestionEngineListener implements ApplicationListener<PublicApiEvent> {

  private final Map<String, List<String>> configMap;
  private final QuizService quizService;

  private final CmsService cmsService;

  private static final String CONFIG_MAP = "configMap";

  @Value("${cms.brand}")
  private String brand;

  private List<String> cmsEndPoints = new ArrayList<>();

  @Value("#{'${cms.endpoints}'.split(',')}")
  private List<String> endpoints;

  @SneakyThrows
  @Override
  public void onApplicationEvent(PublicApiEvent event) {
    String collectionName = event.getCollectionName();
    log.info("Received PublicApiEvent - " + event.getCollectionName());
    if (StringUtils.isNotBlank(collectionName)
        && collectionName.replace("\"", "").equals(CONFIG_MAP)) {
      repopulateConfigMap();
    } else if (isEndPointMatch(configMap, endpoints, collectionName.replace("\"", ""))) {
      quizService.findPreviousLiveAndFutureQuizzes();
    }
  }

  private void repopulateConfigMap() {
    List<ApiCollectionConfig> apiCollectionConfigs = cmsService.apiCollectionConfig(brand);
    if (!CollectionUtils.isEmpty(apiCollectionConfigs)) {
      configMap.clear();
      apiCollectionConfigs.forEach(
          (ApiCollectionConfig config) -> configMap.put(config.getKey(), config.getValues()));
      log.debug("After refreshed ConfigMap Values: {} ", configMap);
    }
  }

  public boolean isEndPointMatch(
      Map<String, List<String>> configMap, List<String> endpoints, String collectionName) {
    return configMap.entrySet().stream()
        .filter(
            e ->
                Objects.nonNull(e.getValue())
                    && e.getValue().contains(collectionName)
                    && endpoints.contains(e.getKey()))
        .map(e -> true)
        .findAny()
        .isPresent();
  }
}
