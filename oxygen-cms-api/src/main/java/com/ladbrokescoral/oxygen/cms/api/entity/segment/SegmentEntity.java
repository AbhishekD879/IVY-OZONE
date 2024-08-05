package com.ladbrokescoral.oxygen.cms.api.entity.segment;

import java.util.List;

public interface SegmentEntity {

  public String getId();

  public void setId(String id);

  public List<SegmentReference> getSegmentReferences();

  public void setSegmentReferences(List<SegmentReference> segmentReferences);

  public List<String> getInclusionList();

  public List<String> getExclusionList();

  public String getArchivalId();

  public void setArchivalId(String archivalId);

  public boolean isUniversalSegment();

  public void setInclusionList(List<String> segments);

  public void setExclusionList(List<String> segments);

  public String getBrand();

  public void setMessage(String message);
}
