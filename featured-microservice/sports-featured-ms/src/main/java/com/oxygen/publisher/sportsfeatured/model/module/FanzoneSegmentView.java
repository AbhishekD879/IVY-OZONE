package com.oxygen.publisher.sportsfeatured.model.module;

import com.oxygen.publisher.sportsfeatured.model.module.data.FanBetsConfig;
import com.oxygen.publisher.sportsfeatured.model.module.data.QuickLinkData;
import com.oxygen.publisher.sportsfeatured.model.module.data.SurfaceBetModuleData;
import com.oxygen.publisher.sportsfeatured.model.module.data.TeamBetsConfig;
import java.util.HashMap;
import java.util.Map;
import lombok.*;

/**
 * This class is use for preparing the Fanzone segment view map. This Map will have Fanzone segments
 * as key & value will be the highlightCarouselModules & surfaceBetModules.
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class FanzoneSegmentView {
  private Map<String, HighlightCarouselModule> highlightCarouselModules = new HashMap<>();
  private Map<String, SurfaceBetModuleData> surfaceBetModuleData = new HashMap<>();
  private Map<String, QuickLinkData> quickLinkModuleData = new HashMap<>();
  private Map<String, TeamBetsConfig> teamBetsModuleData = new HashMap<>();
  private Map<String, FanBetsConfig> fanBetsModuleData = new HashMap<>();
}
