package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import com.ladbrokescoral.oxygen.cms.api.entity.PopularTab;
import com.ladbrokescoral.oxygen.cms.api.repository.PopularTabRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class PopularTabService extends SortableService<PopularTab> {

  public PopularTabService(PopularTabRepository popularTabRepository) {
    super(popularTabRepository);
  }
}
