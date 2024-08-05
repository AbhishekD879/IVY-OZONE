package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import java.util.List;
import lombok.Data;

@Data
public class LuckyDipModuleData extends AbstractModuleData {
  private List<LuckyDipCategoryData> luckyDipCategoryData;
}
