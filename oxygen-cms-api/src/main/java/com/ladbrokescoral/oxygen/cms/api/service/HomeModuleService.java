package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import java.util.List;
import javax.validation.Valid;

public interface HomeModuleService extends CrudService<HomeModule> {
  List<HomeModule> findByActiveState(boolean active);

  List<HomeModule> findByActiveStateAndPublishToChannel(boolean active, String brand);

  List<HomeModule> findAll(String brand, @Valid PageType pageType, String pageId);

  // segmention related methods
  List<HomeModule> findByActiveStateAndPublishToChannelBySegmantName(
      boolean active, String brand, String segmentName);

  List<HomeModule> findAll(
      String brand, @Valid PageType pageType, String pageId, String segmentName);

  List<HomeModule> findByActiveStateAndPublishToChannelAndApplyUniversalSegments(
      boolean active, String brand);
}
