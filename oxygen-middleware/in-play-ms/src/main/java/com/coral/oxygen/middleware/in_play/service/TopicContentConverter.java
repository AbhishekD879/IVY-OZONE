package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.in_play.service.model.safbaf.Entity;
import com.coral.oxygen.middleware.in_play.service.model.safbaf.KafkaSafUpdate;
import com.coral.oxygen.middleware.util.JsonUtil;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class TopicContentConverter {

  public Optional<Entity> convertSafUpdateToPojo(String message) {
    KafkaSafUpdate kafkaSafUpdate = JsonUtil.fromJson(message, KafkaSafUpdate.class);
    return Optional.ofNullable(kafkaSafUpdate.getEvent());
  }
}
