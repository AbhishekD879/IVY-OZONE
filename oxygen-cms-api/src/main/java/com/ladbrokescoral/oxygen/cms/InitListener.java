package com.ladbrokescoral.oxygen.cms;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.util.CustomEvent;
import com.ladbrokescoral.oxygen.cms.util.EventEnum;
import java.util.Arrays;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.ApplicationListener;
import org.springframework.context.annotation.Profile;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.stereotype.Component;

@Data
@AllArgsConstructor
@Slf4j
@Component
@Profile("!UNIT")
public class InitListener implements ApplicationListener<ContextRefreshedEvent> {
  private final ApplicationEventPublisher applicationEventPublisher;

  @Override
  public void onApplicationEvent(ContextRefreshedEvent event) {

    Arrays.asList("bma", "ladbrokes").stream().forEach(this::publishByBrand);
  }

  public void publishByBrand(String brand) {
    for (EventEnum value : EventEnum.values()) {
      try {
        if (value.isPublishEvent()) {
          applicationEventPublisher.publishEvent(
              new CustomEvent<>(
                  (HasBrand) value.getClazz().getDeclaredConstructor().newInstance(),
                  value.getCollectionName(),
                  brand));
        }
      } catch (Exception e) {
        log.error("error while publishing event", e);
      }
    }
  }
}
