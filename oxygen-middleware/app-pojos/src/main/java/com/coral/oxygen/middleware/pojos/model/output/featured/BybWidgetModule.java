package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import lombok.EqualsAndHashCode;
import lombok.Setter;
import lombok.ToString;

@Setter
@ToString(callSuper = true)
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "_id")
public class BybWidgetModule extends AbstractFeaturedModule<BybWidgetModuleData> {

  private int marketCardVisibleSelections;
  private boolean showAll;

  @ChangeDetect
  public int getMarketCardVisibleSelections() {
    return marketCardVisibleSelections;
  }

  @ChangeDetect
  public boolean isShowAll() {
    return showAll;
  }

  public BybWidgetModule() {
    this.showExpanded = true;
  }

  @JsonIgnore
  @Override
  public ModuleType getModuleType() {
    return ModuleType.BYB_WIDGET;
  }
}
