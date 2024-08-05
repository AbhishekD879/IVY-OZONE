package com.oxygen.publisher.sportsfeatured.model.module.data;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
public class QuickLinkData extends AbstractModuleData {
  private String id;
  private String destination;
  private String svgId;
  private String title;
  private Integer displayOrder;
}
