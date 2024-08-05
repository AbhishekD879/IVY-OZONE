package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.QualificationRuleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.QualificationRule;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QualificationRulePublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class QualificationRuleAfterSaveListener extends BasicMongoEventListener<QualificationRule> {
  private final QualificationRulePublicService service;
  private static final String PATH_TEMPLATE = "api/{0}/one-two-free";
  private static final String FILE_NAME = "qualification-rule";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  private static final String COLLECTION_NAME = "qualification-rule";

  @Value(value = "${ladbrokes.kafka.topic.cms-qualification-rule}")
  private String ladsQualificationRuleTopic;

  public QualificationRuleAfterSaveListener(
      final QualificationRulePublicService service,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<QualificationRule> event) {
    String brand = event.getSource().getBrand();
    Optional<QualificationRuleDto> content = service.findByBrand(brand);
    uploadOptional(brand, PATH_TEMPLATE, FILE_NAME, content);
    ladsCoralKafkaPublisher.publishMessage(ladsQualificationRuleTopic, brand, COLLECTION_NAME);
  }
}
