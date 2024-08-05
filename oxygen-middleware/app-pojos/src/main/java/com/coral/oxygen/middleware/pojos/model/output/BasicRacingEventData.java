package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public abstract class BasicRacingEventData extends AbstractModuleData {
  private String id;
  private String name;
  private String startTime;
  private String effectiveGpStartTime;
  private String eventStatusCode;
  private String liveServChannels;
  private String liveServChildrenChannels;

  @ChangeDetect(minor = true)
  public String getEventStatusCode() {
    return eventStatusCode;
  }

  @Override
  public String idForChangeDetection() {
    return id;
  }
}
