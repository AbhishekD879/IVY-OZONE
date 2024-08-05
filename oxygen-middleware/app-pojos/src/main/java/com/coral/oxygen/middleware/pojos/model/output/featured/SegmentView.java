package com.coral.oxygen.middleware.pojos.model.output.featured;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;

@Data
public class SegmentView implements Serializable {

  private Map<String, SegmentOrderdModule> highlightCarouselModules = new HashMap<>();
  private Map<String, SegmentOrderdModule> eventModules = new HashMap<>();
  private Map<String, SegmentOrderdModuleData> quickLinkData = new HashMap<>();
  private Map<String, SegmentOrderdModuleData> surfaceBetModuleData = new HashMap<>();
  private Map<String, SegmentOrderdModuleData> inplayModuleData = new HashMap<>();
  private Map<String, Double> defaultSegmentReferenceSortOder = new HashMap<>();
}
