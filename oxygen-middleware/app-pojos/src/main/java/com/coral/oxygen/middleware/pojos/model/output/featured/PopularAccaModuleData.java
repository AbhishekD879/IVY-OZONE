package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.coral.oxygen.middleware.pojos.model.output.popular_bet.TrendingPosition;
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

  @ChangeDetect
  public String getTitle() {
    return title;
  }

  @ChangeDetect
  public Integer getDisplayOrder() {
    return displayOrder;
  }

  @ChangeDetect(compareCollection = true)
  public List<TrendingPosition> getPositions() {
    return positions;
  }

  @ChangeDetect
  public String getNumberOfTimeBackedLabel() {
    return numberOfTimeBackedLabel;
  }

  @ChangeDetect
  public Integer getNumberOfTimeBackedThreshold() {
    return numberOfTimeBackedThreshold;
  }

  @ChangeDetect
  public String getSubTitle() {
    return subTitle;
  }

  @Override
  public String idForChangeDetection() {
    return id;
  }
}
