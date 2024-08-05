package com.oxygen.publisher.sportsfeatured.model.module.data.inplay;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import com.oxygen.publisher.sportsfeatured.model.module.data.AbstractModuleData;
import java.util.Collection;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "categoryCode")
public class SportSegment extends AbstractModuleData {

  private Integer categoryId;
  private String topLevelType;
  private Boolean showInPlay;
  private String categoryName;
  private String categoryCode;
  private String categoryPath;
  private List<TypeSegment> eventsByTypeName;
  private Collection<Long> eventsIds;
  private Integer displayOrder;
  private String sportUri;
  private String svgId;
  private int eventCount;
  private List<String> marketSelectorOptions;
  private String marketSelector;
}
