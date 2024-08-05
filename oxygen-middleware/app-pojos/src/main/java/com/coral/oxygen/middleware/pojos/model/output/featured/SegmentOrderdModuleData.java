package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.output.inplay.SportSegment;
import java.io.Serializable;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class SegmentOrderdModuleData implements Serializable {

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

  @ChangeDetect(compareList = true)
  public List<SegmentedEvents> getLimitedEvents() {
    return limitedEvents;
  }
}
