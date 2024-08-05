package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import com.google.gson.annotations.SerializedName;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode
public abstract class SportPageModuleDataItem {

  @SerializedName("@type")
  private String type;

  private PageType pageType;

  private List<String> segments;

  private List<SegmentReference> segmentReferences;
  // This property holding the Fanzone inclusion Segments
  private List<String> fanzoneSegments;

  public String getType() {
    return type;
  }

  public void setType(String type) {
    this.type = type;
  }

  public PageType getPageType() {
    return pageType;
  }

  public void setPageType(PageType pageType) {
    this.pageType = pageType;
  }

  public List<String> getSegments() {
    return segments;
  }

  public void setSegments(List<String> segments) {
    this.segments = segments;
  }

  public List<SegmentReference> getSegmentReferences() {
    return segmentReferences;
  }

  public void setSegmentReferences(List<SegmentReference> segmentReferences) {
    this.segmentReferences = segmentReferences;
  }
  /*
  Its helps to get Fanzone Segments
   */
  public List<String> getFanzoneSegments() {
    return this.fanzoneSegments;
  }
  /*
  Its helps to set Fanzone Segments
   */
  public void setFanzoneSegments(List<String> fanzoneSegments) {
    this.fanzoneSegments = fanzoneSegments;
  }

  protected SportPageModuleDataItem(String type, PageType pageType) {
    super();
    this.type = type;
    this.pageType = pageType;
  }
}
