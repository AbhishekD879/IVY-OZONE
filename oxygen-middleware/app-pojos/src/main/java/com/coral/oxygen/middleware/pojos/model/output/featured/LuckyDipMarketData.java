package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.fasterxml.jackson.annotation.JsonIgnore;
import java.io.Serializable;
import lombok.Data;

@Data
public class LuckyDipMarketData implements IdHolder, Serializable {
  private String eventId;
  private String eventName;
  private String eventStatus;
  private String marketId;
  private String marketDescription;
  private String marketStatus;
  private String typeId;
  private String typeName;
  private Integer categoryId;
  private String categoryName;
  private String eventStartTime;
  private Integer eventDisplayOrder;
  private Integer marketDisplayOrder;
  @JsonIgnore private String svgId;

  @ChangeDetect
  public String getEventName() {
    return eventName;
  }

  @ChangeDetect
  public String getMarketDescription() {
    return marketDescription;
  }

  @ChangeDetect
  public String getEventStatus() {
    return eventStatus;
  }

  @ChangeDetect
  public String getMarketStatus() {
    return marketStatus;
  }

  @ChangeDetect
  public String getSvgId() {
    return svgId;
  }

  @ChangeDetect
  public String getEventStartTime() {
    return eventStartTime;
  }

  @ChangeDetect
  public Integer getEventDisplayOrder() {
    return eventDisplayOrder;
  }

  @ChangeDetect
  public Integer getMarketDisplayOrder() {
    return marketDisplayOrder;
  }

  @Override
  public String idForChangeDetection() {
    return marketId;
  }
}
