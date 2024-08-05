package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.module.data.QuickLinkData;
import com.oxygen.publisher.sportsfeatured.model.module.data.SurfaceBetModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment;
import java.util.List;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class SegmentOrderdModuleData {

  private double segmentOrder;

  private QuickLinkData quickLinkData;
  private SurfaceBetModuleData surfaceBetModuleData;
  private SportSegment inplayData;
  private List<SegmentedEvents> limitedEvents;
  private List<Long> eventIds;
  private int eventCount;

  public SegmentOrderdModuleData(double segmentOrder, QuickLinkData quickLinkData) {
    this.segmentOrder = segmentOrder;
    this.quickLinkData = quickLinkData;
  }

  public SegmentOrderdModuleData(double segmentOrder, SurfaceBetModuleData surfaceBetModuleData) {
    this.segmentOrder = segmentOrder;
    this.surfaceBetModuleData = surfaceBetModuleData;
  }

  public SegmentOrderdModuleData(double segmentOrder, SportSegment inplayData) {
    this.segmentOrder = segmentOrder;
    this.inplayData = inplayData;
  }
}
