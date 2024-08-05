package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import java.io.Serializable;
import java.util.List;
import lombok.Data;

@Data
public class LuckyDipCategoryData extends AbstractModuleData implements IdHolder, Serializable {
  private String sportName;
  private String svgId;
  private List<LuckyDipTypeData> luckyDipTypeData;
  private Double displayOrder;

  @Override
  public String idForChangeDetection() {
    return sportName;
  }

  @ChangeDetect
  public String getSvgId() {
    return svgId;
  }

  @ChangeDetect(compareCollection = true)
  public List<LuckyDipTypeData> getLuckyDipTypeData() {
    return luckyDipTypeData;
  }

  @ChangeDetect
  public Double getDisplayOrder() {
    return displayOrder;
  }
}
