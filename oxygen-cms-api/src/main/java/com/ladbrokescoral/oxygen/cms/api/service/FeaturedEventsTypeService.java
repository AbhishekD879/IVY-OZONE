package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.FeaturedEventsType;
import com.ladbrokescoral.oxygen.cms.api.repository.FeaturedEventsTypeRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class FeaturedEventsTypeService extends AbstractService<FeaturedEventsType> {

  @Autowired
  public FeaturedEventsTypeService(FeaturedEventsTypeRepository repository) {
    super(repository);
  }
}
