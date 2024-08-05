package com.coral.oxygen.middleware.in_play.service;

import com.coral.oxygen.middleware.in_play.service.injector.InPlayDataInjector;
import com.coral.oxygen.middleware.pojos.model.cms.CmsInplayData;
import com.coral.oxygen.middleware.pojos.model.cms.SportItem;
import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import java.util.Map;
import java.util.function.Supplier;
import org.springframework.stereotype.Component;

/** Created by azayats on 25.01.17. */
@Component
public class CMSDataInjector implements InPlayDataInjector<CmsInplayData> {

  @Override
  public void injectData(InPlayData inPlayData, Supplier<CmsInplayData> initialDataSupplier) {
    CmsInplayData cmsInplayData = initialDataSupplier.get();

    Map<String, SportItem> mergedMap = cmsInplayData.getSportMap();

    InPlayData.allSportSegmentsStream(inPlayData)
        .forEach(
            sportSegment -> {
              String categoryId = String.valueOf(sportSegment.getCategoryId());
              SportItem mergedSportItem = mergedMap.get(categoryId);
              if (mergedSportItem != null) {
                sportSegment.setSportUri(mergedSportItem.getTargetUri());
                sportSegment.setShowInPlay(mergedSportItem.isShowInPlay());
                sportSegment.setSvgId(mergedSportItem.getSvgId());
                sportSegment.setCategoryPath(mergedSportItem.getCategoryPath());
              }
            });
  }
}
