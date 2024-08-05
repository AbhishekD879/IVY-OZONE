package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.timeline.TimelineConfigDto;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Config;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineConfigRepository;
import com.ladbrokescoral.oxygen.cms.kafka.TimelineKafkaPublisher;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class TimelineConfigService extends AbstractService<Config> {

  private final TimelineConfigRepository timelineConfigRepository;

  private final TimelineKafkaPublisher timelineKafkaPublisher;

  public TimelineConfigService(
      TimelineConfigRepository timelineConfigRepository,
      TimelineKafkaPublisher timelineKafkaPublisher) {
    super(timelineConfigRepository);
    this.timelineConfigRepository = timelineConfigRepository;
    this.timelineKafkaPublisher = timelineKafkaPublisher;
  }

  @Override
  public Config save(Config entity) {
    if (timelineConfigRepository.existsByBrand(entity.getBrand())) {
      throw new IllegalArgumentException(
          String.format("Only one TimelineConfig could exist per brand: '%s'", entity.getBrand()));
    }

    return super.save(entity);
  }

  @Override
  public Config update(Config existingEntity, Config updateEntity) {
    if (!existingEntity.getBrand().equals(updateEntity.getBrand())) {
      throw new IllegalArgumentException(
          "Brand cannot be cannot be changed once TimelineConfig is created");
    }
    sendConfigMessage(updateEntity);
    return timelineConfigRepository.save(updateEntity);
  }

  public Config findOneByBrand(String brand) {
    return timelineConfigRepository.findOneByBrand(brand).orElseThrow(NotFoundException::new);
  }

  public Optional<Config> findOptionalByBrand(String brand) {
    return timelineConfigRepository.findOneByBrand(brand);
  }

  private void sendConfigMessage(Config config) {
    TimelineConfigDto configDto =
        new TimelineConfigDto().setEnabled(config.isEnabled()).setBrand(config.getBrand());
    this.timelineKafkaPublisher.publishTimelineConfigMessage(configDto.getBrand(), configDto);
  }
}
