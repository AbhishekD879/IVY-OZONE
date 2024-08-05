package com.coral.siteserver.model;

public class Aggregation {

  private String aggregatedRecordType;
  private Integer count;
  private Long id;
  private Long refRecordId;
  private String refRecordType;

  public String getAggregatedRecordType() {
    return aggregatedRecordType;
  }

  public void setAggregatedRecordType(String aggregatedRecordType) {
    this.aggregatedRecordType = aggregatedRecordType;
  }

  public Integer getCount() {
    return count;
  }

  public void setCount(Integer count) {
    this.count = count;
  }

  public Long getId() {
    return id;
  }

  public void setId(Long id) {
    this.id = id;
  }

  public Long getRefRecordId() {
    return refRecordId;
  }

  public void setRefRecordId(Long refRecordId) {
    this.refRecordId = refRecordId;
  }

  public String getRefRecordType() {
    return refRecordType;
  }

  public void setRefRecordType(String refRecordType) {
    this.refRecordType = refRecordType;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Aggregation{");
    sb.append("aggregatedRecordType='").append(aggregatedRecordType).append('\'');
    sb.append(", count=").append(count);
    sb.append(", id=").append(id);
    sb.append(", refRecordId=").append(refRecordId);
    sb.append(", refRecordType='").append(refRecordType).append('\'');
    sb.append('}');
    return sb.toString();
  }
}
