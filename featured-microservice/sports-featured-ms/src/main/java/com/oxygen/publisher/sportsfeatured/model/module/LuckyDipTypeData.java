package com.oxygen.publisher.sportsfeatured.model.module;

import java.util.List;
import lombok.Data;

@Data
public class LuckyDipTypeData {
  private String typeName;
  private List<LuckyDipMarketData> luckyDipMarketData;
}
