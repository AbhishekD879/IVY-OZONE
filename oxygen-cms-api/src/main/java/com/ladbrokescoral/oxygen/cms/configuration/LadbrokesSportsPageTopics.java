package com.ladbrokescoral.oxygen.cms.configuration;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Getter
public class LadbrokesSportsPageTopics {

  @Value(value = "${ladbrokes.kafka.topic.cms-sports}")
  private String sportsTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-sportcategories}")
  private String sportcategoriesTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-moduleribbontabs}")
  private String moduleribbontabsTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-homemodules}")
  private String homemodulesTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-sportquicklinks}")
  private String sportquicklinksTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-ycleagues}")
  private String ycleaguesTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-systemconfigurations}")
  private String systemconfigurationsTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-assetmanagement}")
  private String assetmanagementTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-fanzones}")
  private String fanzonesTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-sportModules}")
  private String sportModulesTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-homeInplaySport}")
  private String homeInplaySportTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-sporttabs}")
  private String sporttabsTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-surfaceBet}")
  private String surfaceBetTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-surfacebetArchive}")
  private String surfacebetArchiveTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-highlightCarousel}")
  private String highlightCarouselTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-highlightCarouselArchive}")
  private String highlightCarouselArchiveTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-segments}")
  private String segmentsTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-segmentedModules}")
  private String segmentedModulesTopic;
}
