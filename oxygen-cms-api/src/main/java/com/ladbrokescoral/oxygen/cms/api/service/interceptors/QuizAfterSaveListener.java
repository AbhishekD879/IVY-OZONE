package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Brand;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QuestionEnginePublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class QuizAfterSaveListener extends BasicMongoEventListener<Quiz> {
  private final QuestionEnginePublicService service;
  private static final String QUIZ_DATA = "quiz";
  private static final String PATH_TEMPLATE = "api/{0}/question-engine";
  private final LadsCoralKafkaPublisher ladsCoralKafkaPublisher;
  private static final String COLLECTION_NAME = "quiz";

  @Value(value = "${coral.kafka.topic.cms-quiz}")
  private String coralQuizTopic;

  @Value(value = "${ladbrokes.kafka.topic.cms-quiz}")
  private String ladsQuizTopic;

  public QuizAfterSaveListener(
      final QuestionEnginePublicService service,
      final DeliveryNetworkService context,
      LadsCoralKafkaPublisher ladsCoralKafkaPublisher) {
    super(context);
    this.service = service;
    this.ladsCoralKafkaPublisher = ladsCoralKafkaPublisher;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<Quiz> event) {
    String brand = event.getSource().getBrand();
    List<QuizDto> content = service.getQuizByBrand(brand);
    uploadCollection(brand, PATH_TEMPLATE, QUIZ_DATA, content);
    String topic = brand.equalsIgnoreCase(Brand.BMA) ? coralQuizTopic : ladsQuizTopic;
    ladsCoralKafkaPublisher.publishMessage(topic, brand, COLLECTION_NAME);
  }
}
