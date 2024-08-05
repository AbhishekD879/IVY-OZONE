package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class SegmentOrderdModule {

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
