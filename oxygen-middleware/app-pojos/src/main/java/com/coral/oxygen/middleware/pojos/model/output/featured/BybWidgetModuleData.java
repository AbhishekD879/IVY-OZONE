package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class BybWidgetModuleData extends EventsModuleData {

  private String title;

  public BybWidgetModuleData() {
    this.type = "BybWidgetData";
  }

  @ChangeDetect
  public String getTitle() {
    return title;
  }
}
