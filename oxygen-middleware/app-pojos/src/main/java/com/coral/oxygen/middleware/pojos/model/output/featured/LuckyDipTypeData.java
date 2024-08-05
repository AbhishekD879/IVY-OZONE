package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import java.io.Serializable;
import java.util.List;
import lombok.Data;

@Data
public class LuckyDipTypeData implements IdHolder, Serializable {
  private String typeName;
  private List<LuckyDipMarketData> luckyDipMarketData;

  @ChangeDetect(compareCollection = true)
  public List<LuckyDipMarketData> getLuckyDipMarketData() {
    return luckyDipMarketData;
  }

  @Override
  public String idForChangeDetection() {
    return typeName;
  }
}
