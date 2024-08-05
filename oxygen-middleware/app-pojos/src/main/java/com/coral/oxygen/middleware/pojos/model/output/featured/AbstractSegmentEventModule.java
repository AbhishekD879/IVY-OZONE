package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public abstract class AbstractSegmentEventModule extends AbstractFeaturedModule<EventsModuleData> {
  // This property holding the Fanzone inclusion Segments
  private List<String> fanzoneSegments;
  private List<SegmentReference> segmentReferences;
  private Map<String, SegmentView> moduleSegmentView = new HashMap<>();
  // This property holding the FanzoneSegmentView map for each fanzone segments.
  private Map<String, FanzoneSegmentView> fanzoneModuleSegmentView = new HashMap<>();

  public List<SegmentReference> getSegmentReferences() {
    return segmentReferences;
  }

  public void setSegmentReferences(List<SegmentReference> segmentReferences) {
    this.segmentReferences = segmentReferences;
  }

  public Map<String, SegmentView> getModuleSegmentView() {
    return moduleSegmentView;
  }

  public void setModuleSegmentView(Map<String, SegmentView> moduleSegmentView) {
    this.moduleSegmentView = moduleSegmentView;
  }

  // Its helps to get Fanzone Segments.
  public List<String> getFanzoneSegments() {
    return fanzoneSegments;
  }

  // Its helps to set Fanzone Segments.
  public void setFanzoneSegments(List<String> fanzoneSegments) {
    this.fanzoneSegments = fanzoneSegments;
  }
  // This property get the FanzoneSegmentView map for each fanzone segments.
  public Map<String, FanzoneSegmentView> getFanzoneModuleSegmentView() {
    return this.fanzoneModuleSegmentView;
  }
  // This property set the FanzoneSegmentView map for each fanzone segments.
  public void setFanzoneModuleSegmentView(
      Map<String, FanzoneSegmentView> fanzoneModuleSegmentView) {
    this.fanzoneModuleSegmentView = fanzoneModuleSegmentView;
  }
}
