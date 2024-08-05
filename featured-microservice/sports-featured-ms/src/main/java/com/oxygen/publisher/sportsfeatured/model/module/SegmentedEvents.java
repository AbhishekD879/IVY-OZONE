package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.TypeSegment;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class SegmentedEvents {

  private TypeSegment eventByTypeName;
  private List<EventsModuleData> events;
  private List<Long> eventIds;
}
