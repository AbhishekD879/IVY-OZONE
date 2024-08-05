package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SportsQuickLink;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.util.List;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@ToString
@Setter
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "id")
public class QuickLinkData extends AbstractModuleData {

  @Getter private String id;

  private String destination;
  private String svgId;
  private String title;
  private Integer displayOrder;
  private List<SegmentReference> segmentReferences;

  private List<String> fanzoneSegments;

  public QuickLinkData(SportsQuickLink sportsQuickLink) {
    this.id = sportsQuickLink.getId();
    this.destination = sportsQuickLink.getDestination();
    this.svgId = sportsQuickLink.getSvgId();
    this.title = sportsQuickLink.getTitle();
    this.displayOrder = sportsQuickLink.getDisplayOrder();
    this.pageType = sportsQuickLink.getPageType();
    super.setSegments(sportsQuickLink.getSegments());
    this.segmentReferences = sportsQuickLink.getSegmentReferences();
    this.fanzoneSegments = sportsQuickLink.getFanzoneSegments();
  }

  @ChangeDetect
  public Integer getDisplayOrder() {
    return displayOrder;
  }

  @ChangeDetect
  public String getDestination() {
    return destination;
  }

  @ChangeDetect
  public String getSvgId() {
    return svgId;
  }

  @ChangeDetect
  public String getTitle() {
    return title;
  }

  @Override
  public String idForChangeDetection() {
    return id;
  }

  @ChangeDetect(compareCollection = true)
  public List<SegmentReference> getSegmentReferences() {
    return segmentReferences;
  }

  @ChangeDetect
  public List<String> getFanzoneSegments() {
    return fanzoneSegments;
  }
}
