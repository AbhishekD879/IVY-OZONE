package com.oxygen.publisher.sportsfeatured.model.module;

import com.fasterxml.jackson.annotation.JsonIgnore;
import lombok.Data;

@Data
public class LuckyDipMarketData {
  private String eventId;
  private String eventName;
  private String marketId;
  private String marketDescription;
  private String typeId;
  private String typeName;
  private Integer categoryId;
  private String categoryName;
  @JsonIgnore private String svgId;
}
