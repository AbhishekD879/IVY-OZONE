package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.repository.TrendingTabRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class TrendingTabService extends SortableService<TrendingTab> {

  public TrendingTabService(TrendingTabRepository trendingTabRepository) {
    super(trendingTabRepository);
  }
}
