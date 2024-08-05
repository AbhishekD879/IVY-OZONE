package com.oxygen.publisher.sportsfeatured.model.module.data;

import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
public class PopularAccaModuleData extends AbstractModuleData {
  @Getter private String id;
  private String title;
  private String subTitle;
  private String svgId;
  private Integer displayOrder;
  private String numberOfTimeBackedLabel;
  private Integer numberOfTimeBackedThreshold;
  private List<TrendingPosition> positions;
}
