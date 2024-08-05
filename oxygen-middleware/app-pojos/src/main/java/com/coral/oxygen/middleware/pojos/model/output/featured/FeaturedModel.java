package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@ToString
@EqualsAndHashCode
@Builder
@AllArgsConstructor
@NoArgsConstructor
public class FeaturedModel implements AbstractFeaturedModel {

  private String pageId;
  private String directiveName;
  private Map<Long, EventsModuleData> eventsModuleData = new HashMap<>();
  @Builder.Default private List<AbstractFeaturedModule<?>> modules = new ArrayList<>();
  private String showTabOn;
  private String title;
  private boolean visible;
  private boolean featureStructureChanged;
  private Map<String, SegmentView> segmentWiseModules = new HashMap<>();
  // This property holding the FanzoneSegmentView map for each fanzone segments.
  private Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap<>();
  private SurfaceBetModule surfaceBetModule;
  private QuickLinkModule quickLinkModule;
  private InplayModule inplayModule;
  private TeamBetsModule teamBetsModule;
  private FanBetsModule fanBetsModule;
  private boolean segmented;
  private boolean useFSCCached;
}
