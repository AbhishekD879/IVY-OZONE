package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import java.io.Serializable;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class SegmentOrderdModule implements Serializable {

  private double segmentOrder;

  private EventsModule eventsModule;
  private HighlightCarouselModule highlightCarouselModule;
  private List<EventsModuleData> eventsModuleData;
  protected Boolean cashoutAvail;

  public SegmentOrderdModule(double segmentOrder, HighlightCarouselModule highlightCarouselModule) {
    this.segmentOrder = segmentOrder;
    this.highlightCarouselModule = highlightCarouselModule;
  }

  public SegmentOrderdModule(double segmentOrder, EventsModule eventsModule) {
    this.segmentOrder = segmentOrder;
    this.eventsModule = eventsModule;
  }
}
