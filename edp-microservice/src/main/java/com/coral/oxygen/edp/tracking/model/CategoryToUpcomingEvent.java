package com.coral.oxygen.edp.tracking.model;

import com.coral.oxygen.edp.model.output.OutputEvent;
import com.egalacoral.spark.siteserver.model.Category;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = false)
@SuppressWarnings(
    "squid:S1948") // doesn't need to be Serializable due to using Jackson serialization
public class CategoryToUpcomingEvent extends Category {

  private OutputEvent event;

  public CategoryToUpcomingEvent(OutputEvent upcomingEvent, Category category) {
    this.event = upcomingEvent;
    this.setId(category.getId());
    this.setName(category.getCategoryName());
    this.setClassStatusCode(category.getClassStatusCode());
    this.setIsActive(category.getIsActive());
    this.setDisplayOrder(category.getDisplayOrder());
    this.setSiteChannels(category.getSiteChannels());
    this.setClassFlagCodes(category.getClassFlagCodes());
    this.setClassSortCode(category.getClassSortCode());
    this.setCategoryId(category.getCategoryId());
    this.setCategoryCode(category.getCategoryCode());
    this.setCategoryName(category.getCategoryName());
    this.setCategoryDisplayOrder(category.getCategoryDisplayOrder());
    this.setHasOpenEvent(category.getHasOpenEvent());
    this.setHasNext24HourEvent(category.getHasNext24HourEvent());
  }
}
