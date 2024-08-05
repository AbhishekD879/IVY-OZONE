package com.coral.oxygen.middleware.featured.consumer.sportpage;

import com.coral.oxygen.middleware.pojos.model.output.featured.SegmentView;

public interface SegmentOrderProcessor {
  /** Featured Modules range */
  Double MODULE_DISPLAY_ORDER = Double.valueOf(10000000);

  Double DEFAULT_DISPLAY_ORDER = Double.valueOf(1000);
  /**
   * Default start value for the Segmented sort order for which there is no Segmented Reference Sort
   * order.
   */
  Double SEGMENT_DISPLAY_ORDER = Double.valueOf(1000000);

  default double getSortOrderFromSegmentView(SegmentView segmentView, String moduleType) {
    double sortOrder =
        segmentView.getDefaultSegmentReferenceSortOder().containsKey(moduleType)
            ? segmentView.getDefaultSegmentReferenceSortOder().get(moduleType)
                + DEFAULT_DISPLAY_ORDER
            : SEGMENT_DISPLAY_ORDER;
    segmentView.getDefaultSegmentReferenceSortOder().put(moduleType, sortOrder);
    return sortOrder;
  }
}
