package com.coral.oxygen.edp.service;

import com.ladbrokescoral.oxygen.cms.client.api.CmsApiClient;
import com.ladbrokescoral.oxygen.cms.client.model.StreamAndBetDto;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;

@Service
public class CmsApiServiceCacheable implements CmsApiService {
  private CmsApiClient cmsApiClient;
  private final String cmsBrand;

  @Autowired
  public CmsApiServiceCacheable(@Value("${cms.brand}") String cmsBrand, CmsApiClient client) {
    this.cmsBrand = cmsBrand;
    cmsApiClient = client;
  }

  @Cacheable("dto")
  @Override
  public Optional<List<StreamAndBetDto>> getStreamAndBetDto() {
    return cmsApiClient.getStreamAndBetDto(cmsBrand);
  }
}
