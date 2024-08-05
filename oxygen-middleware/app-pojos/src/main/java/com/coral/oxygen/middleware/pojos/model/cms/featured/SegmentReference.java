package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import java.io.Serializable;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public class SegmentReference implements IdHolder, Serializable {

  private String segment;
  private Double displayOrder;

  public String getSegment() {
    return segment;
  }

  public void setSegment(String segment) {
    this.segment = segment;
  }

  @ChangeDetect
  public Double getDisplayOrder() {
    return displayOrder;
  }

  public void setDisplayOrder(Double displayOrder) {
    this.displayOrder = displayOrder;
  }

  @Override
  public String idForChangeDetection() {
    return segment;
  }
}
