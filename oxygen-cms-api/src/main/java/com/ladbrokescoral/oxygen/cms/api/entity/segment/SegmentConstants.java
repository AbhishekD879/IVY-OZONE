package com.ladbrokescoral.oxygen.cms.api.entity.segment;

import static java.util.Comparator.naturalOrder;
import static java.util.Comparator.nullsLast;

import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import java.util.Comparator;
import java.util.List;

public class SegmentConstants {

  private SegmentConstants() {}

  public static final String UNIVERSAL = "Universal";

  public static final boolean isUniversalSegmentChanged(
      List<? extends SegmentEntity> segmentEntities) {
    return segmentEntities.stream().parallel().anyMatch(SegmentEntity::isUniversalSegment);
  }

  public static final Comparator<SurfaceBet> SURFACE_BET_UNIV_DEFAULT_SORT_ORDER =
      Comparator.comparing(SurfaceBet::getSortOrder, nullsLast(naturalOrder()))
          .thenComparing(SurfaceBet::getCreatedAt, nullsLast(naturalOrder()));

  public static final Comparator<SportCategory> SPORT_CAT_UNIV_DEFAULT_SORT_ORDER =
      Comparator.comparing(SportCategory::getSortOrder, nullsLast(naturalOrder()))
          .thenComparing(SportCategory::getCreatedAt, nullsLast(naturalOrder()));
}
