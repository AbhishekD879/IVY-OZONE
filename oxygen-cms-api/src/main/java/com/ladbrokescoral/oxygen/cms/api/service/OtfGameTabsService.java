package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.OtfGameTabs;
import com.ladbrokescoral.oxygen.cms.api.repository.OtfGameTabsRepository;
import org.springframework.stereotype.Service;

@Service
public class OtfGameTabsService extends AbstractService<OtfGameTabs> {

  public OtfGameTabsService(OtfGameTabsRepository otfGameTabsRepository) {
    super(otfGameTabsRepository);
  }
}
