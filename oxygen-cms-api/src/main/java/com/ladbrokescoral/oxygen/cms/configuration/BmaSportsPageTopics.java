package com.ladbrokescoral.oxygen.cms.configuration;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Getter
public class BmaSportsPageTopics {

  @Value(value = "${coral.kafka.topic.cms-sports}")
  private String coralSportsTopic;

  @Value(value = "${coral.kafka.topic.cms-sportcategories}")
  private String coralSportcategoriesTopic;

  @Value(value = "${coral.kafka.topic.cms-moduleribbontabs}")
  private String coralModuleribbontabsTopic;

  @Value(value = "${coral.kafka.topic.cms-homemodules}")
  private String coralHomemodulesTopic;

  @Value(value = "${coral.kafka.topic.cms-sportquicklinks}")
  private String coralSportquicklinksTopic;

  @Value(value = "${coral.kafka.topic.cms-ycleagues}")
  private String coralYcleaguesTopic;

  @Value(value = "${coral.kafka.topic.cms-systemconfigurations}")
  private String coralSystemconfigurationsTopic;

  @Value(value = "${coral.kafka.topic.cms-assetmanagement}")
  private String coralAssetmanagementTopic;

  @Value(value = "${coral.kafka.topic.cms-fanzones}")
  private String coralFanzonesTopic;

  @Value(value = "${coral.kafka.topic.cms-sportModules}")
  private String coralSportModulesTopic;

  @Value(value = "${coral.kafka.topic.cms-homeInplaySport}")
  private String coralHomeInplaySportTopic;

  @Value(value = "${coral.kafka.topic.cms-sporttabs}")
  private String coralSporttabsTopic;

  @Value(value = "${coral.kafka.topic.cms-surfaceBet}")
  private String coralSurfaceBetTopic;

  @Value(value = "${coral.kafka.topic.cms-surfacebetArchive}")
  private String coralSurfacebetArchiveTopic;

  @Value(value = "${coral.kafka.topic.cms-highlightCarousel}")
  private String coralHighlightCarouselTopic;

  @Value(value = "${coral.kafka.topic.cms-highlightCarouselArchive}")
  private String coralHighlightCarouselArchiveTopic;

  @Value(value = "${coral.kafka.topic.cms-segments}")
  private String coralSegmentsTopic;

  @Value(value = "${coral.kafka.topic.cms-segmentedModules}")
  private String coralSegmentedModulesTopic;
}
