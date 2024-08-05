package com.coral.oxygen.middleware.pojos.model.output.featured;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.cms.featured.SegmentReference;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.OutputPrice;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import java.math.BigInteger;
import java.util.List;
import lombok.EqualsAndHashCode;
import lombok.Setter;

@Setter
@EqualsAndHashCode(callSuper = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "objId")
public class SurfaceBetModuleData extends EventsModuleData {

  private String title;
  private String content;
  private String contentHeader;
  private String svgId;
  private String svgBgId;
  private BigInteger selectionId;
  private OutputPrice oldPrice;
  private String svgBgImgPath;
  // BMA-62181: This property will be have list of Fanzone segments
  private List<String> fanzoneSegments;
  // Fanzone BMA-62182 : this property will be hold multiple teamIds of choosen Fanzone inclusion
  private List<SegmentReference> segmentReferences;
  private String objId;
  private Boolean displayOnDesktop;

  public SurfaceBetModuleData() {
    this.type = "SurfaceBetModuleData";
  }

  @ChangeDetect
  public String getSvgBgId() {
    return svgBgId;
  }

  @ChangeDetect
  public String getSvgBgImgPath() {
    return svgBgImgPath;
  }

  @ChangeDetect
  public String getTitle() {
    return title;
  }

  @ChangeDetect
  public String getContent() {
    return content;
  }

  @ChangeDetect
  public String getSvgId() {
    return svgId;
  }

  @ChangeDetect
  public String getContentHeader() {
    return contentHeader;
  }

  @ChangeDetect
  public BigInteger getSelectionId() {
    return selectionId;
  }

  @ChangeDetect(compareNestedObject = true)
  public OutputPrice getOldPrice() {
    return oldPrice;
  }

  @Override
  public String idForChangeDetection() {
    return String.valueOf(selectionId);
  }

  @ChangeDetect
  @Override
  public List<String> getSegments() {
    return super.getSegments();
  }
  // BMA-62181: This property will be help to get list of Fanzone segments.
  @ChangeDetect
  public List<String> getFanzoneSegments() {
    return fanzoneSegments;
  }

  @ChangeDetect(compareCollection = true)
  public List<SegmentReference> getSegmentReferences() {
    return segmentReferences;
  }

  public String getObjId() {
    return objId;
  }

  @ChangeDetect
  public Boolean isDisplayOnDesktop() {
    return displayOnDesktop;
  }
}
