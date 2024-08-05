package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.StaticTextOtf;
import com.ladbrokescoral.oxygen.cms.api.repository.StaticTextOtfRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Slf4j
@Component
public class StaticTextOtfService extends SortableService<StaticTextOtf> {

  private final StaticTextOtfRepository staticTextOtfRepository;

  @Autowired
  public StaticTextOtfService(StaticTextOtfRepository staticTextOtfRepository) {
    super(staticTextOtfRepository);
    this.staticTextOtfRepository = staticTextOtfRepository;
  }

  @Override
  public StaticTextOtf save(StaticTextOtf entity) {
    if (entity.isEnabled() && isActiveAlreadyExists(entity)) {
      throw new IllegalArgumentException(
          "Only one active Static Text per page could be configured at the time");
    }
    return staticTextOtfRepository.save(entity);
  }

  private boolean isActiveAlreadyExists(StaticTextOtf entity) {
    return staticTextOtfRepository.existsByPageNameAndEnabledIsTrueAndIdNotAndBrandIs(
        entity.getPageName(), entity.getId(), entity.getBrand());
  }
}
