package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.AppUpdate;
import com.ladbrokescoral.oxygen.cms.api.repository.AppUpdateRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class AppUpdateService extends AbstractService<AppUpdate> {

  @Autowired
  public AppUpdateService(AppUpdateRepository repository) {
    super(repository);
  }
}
