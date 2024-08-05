package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.module.data.AbstractModuleData;
import java.util.List;
import lombok.Data;

@Data
public class LuckyDipCategoryData extends AbstractModuleData {
  private String sportName;
  private String svgId;
  private List<LuckyDipTypeData> luckyDipTypeData;
  private Double displayOrder;
}
