package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineSplashConfig;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.TimelineSplashConfigRepository;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class TimelineSplashConfigService extends AbstractService<TimelineSplashConfig> {
  private final TimelineSplashConfigRepository timelineSplashConfigRepository;

  public TimelineSplashConfigService(
      TimelineSplashConfigRepository timelineSplashConfigRepository) {
    super(timelineSplashConfigRepository);
    this.timelineSplashConfigRepository = timelineSplashConfigRepository;
  }

  @Override
  public TimelineSplashConfig save(TimelineSplashConfig entity) {
    if (timelineSplashConfigRepository.existsByBrand(entity.getBrand())) {
      throw new IllegalArgumentException(
          String.format("Only one TimelineConfig could exist per brand: '%s'", entity.getBrand()));
    }

    return super.save(entity);
  }

  @Override
  public TimelineSplashConfig update(
      TimelineSplashConfig existingEntity, TimelineSplashConfig updateEntity) {
    if (!existingEntity.getBrand().equals(updateEntity.getBrand())) {
      throw new IllegalArgumentException(
          "Brand cannot be cannot be changed once TimelineConfig is created");
    }

    return timelineSplashConfigRepository.save(updateEntity);
  }

  public TimelineSplashConfig findOneByBrand(String brand) {
    return timelineSplashConfigRepository.findOneByBrand(brand).orElseThrow(NotFoundException::new);
  }

  public Optional<TimelineSplashConfig> findOptionalByBrand(String brand) {
    return timelineSplashConfigRepository.findOneByBrand(brand);
  }
}
