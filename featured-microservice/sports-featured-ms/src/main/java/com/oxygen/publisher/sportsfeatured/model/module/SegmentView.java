package com.oxygen.publisher.sportsfeatured.model.module;

import java.util.HashMap;
import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
public class SegmentView {
  private Map<String, SegmentOrderdModule> highlightCarouselModules = new HashMap<>();
  private Map<String, SegmentOrderdModule> eventModules = new HashMap<>();
  private Map<String, SegmentOrderdModuleData> quickLinkData = new HashMap<>();
  private Map<String, SegmentOrderdModuleData> surfaceBetModuleData = new HashMap<>();
  private Map<String, SegmentOrderdModuleData> inplayModuleData = new HashMap<>();
}
