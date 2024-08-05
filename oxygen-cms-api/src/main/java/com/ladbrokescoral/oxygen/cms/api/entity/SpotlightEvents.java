package com.ladbrokescoral.oxygen.cms.api.entity;

import com.egalacoral.spark.siteserver.model.Event;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode
@AllArgsConstructor
@NoArgsConstructor
public class SpotlightEvents implements HasBrand {
  private String brand;
  private List<TypeEvent> typeEvents;

  @Data
  @AllArgsConstructor
  @NoArgsConstructor
  public static class TypeEvent {
    private String typeId;
    private String typeName;
    private List<Event> events;
  }
}
