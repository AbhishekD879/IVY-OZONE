package com.oxygen.publisher.sportsfeatured.model.module.data;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class VirtualRaceCarouselData extends AbstractModuleData {
  private String name;
  private String startTime;
  private String classId;
  private String effectiveGpStartTime;
}
