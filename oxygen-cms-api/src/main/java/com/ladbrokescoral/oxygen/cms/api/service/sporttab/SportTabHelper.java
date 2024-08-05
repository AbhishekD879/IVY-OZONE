package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import java.util.Comparator;
import org.springframework.util.CollectionUtils;

public class SportTabHelper {

  private SportTabHelper() {}

  private static final Comparator<SortableEntity> SORT_ORDER_COMPARATOR =
      Comparator.comparing(
          SortableEntity::getSortOrder, Comparator.nullsFirst(Comparator.naturalOrder()));

  public static void sortTrendingTabs(SportTab tab) {
    if (!CollectionUtils.isEmpty(tab.getTrendingTabs())) {
      tab.getTrendingTabs().sort(SORT_ORDER_COMPARATOR);
      tab.getTrendingTabs().forEach(SportTabHelper::sortPopularTabs);
    }
  }

  public static void sortPopularTabs(TrendingTab tab) {
    if (!CollectionUtils.isEmpty(tab.getPopularTabs())) {
      tab.getPopularTabs().sort(SORT_ORDER_COMPARATOR);
    }
  }
}
