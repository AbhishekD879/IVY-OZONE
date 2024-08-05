package com.egalacoral.spark.timeform.model.horseracing;

import java.util.Date;

public class HRCourseMapInfo {

  private final String uuid;

  private final long size;

  private final Date lasUpdatedDate;

  private HRCourseMap courseMap;

  public HRCourseMapInfo(HRCourseMap courseMap) {
    this.courseMap = courseMap;
    this.uuid = courseMap.getUUID();
    this.size = courseMap.getBytes().length;
    this.lasUpdatedDate = courseMap.getUpdateDate();
  }

  public String getUuid() {
    return uuid;
  }

  public long getSize() {
    return size;
  }

  public Date getLasUpdatedDate() {
    return lasUpdatedDate;
  }

  public HRCourseMap getCourseMap() {
    return courseMap;
  }
}
