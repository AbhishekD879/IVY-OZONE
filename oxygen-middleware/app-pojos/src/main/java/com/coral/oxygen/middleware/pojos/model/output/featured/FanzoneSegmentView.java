package com.coral.oxygen.middleware.pojos.model.output.featured;

import java.io.Serializable;
import java.util.LinkedHashMap;
import java.util.Map;
import lombok.Data;

/**
 * This class is use for preparing the Fanzone segment view map. This Map will have Fanzone segments
 * as key & value will be the highlightCarouselModules & surfaceBetModules
 */
@Data
public class FanzoneSegmentView implements Serializable {
  private Map<String, HighlightCarouselModule> highlightCarouselModules = new LinkedHashMap<>();
  private Map<String, SurfaceBetModuleData> surfaceBetModuleData = new LinkedHashMap<>();
  private Map<String, QuickLinkData> quickLinkModuleData = new LinkedHashMap<>();
  private Map<String, TeamBetsConfig> teamBetsModuleData = new LinkedHashMap<>();
  private Map<String, FanBetsConfig> fanBetsModuleData = new LinkedHashMap<>();
}
