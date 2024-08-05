package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventTreeNodeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StreamAndBetShortNode;
import com.ladbrokescoral.oxygen.cms.api.mapping.EventTreeMapper;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeLoadEventTree;
import java.time.Instant;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.springframework.stereotype.Component;

@Component
public class SABSiteServeService {

  private final SiteServeLoadEventTree loadEventTree;
  private final EventTreeMapper mapper;

  public SABSiteServeService(SiteServeLoadEventTree loadEventTree, EventTreeMapper mapper) {
    this.loadEventTree = loadEventTree;
    this.mapper = mapper;
  }

  public Map<String, Set<StreamAndBetShortNode>> getActualStreamAndBetMap(
      String brand, Integer categoryId) {
    List<SiteServeEventTreeNodeDto> siteServeEventTreeNodeDtos =
        loadEventTree.loadEventsInNode(brand, categoryId, Instant.now());
    return mapper.toDtoMap(siteServeEventTreeNodeDtos);
  }
}
