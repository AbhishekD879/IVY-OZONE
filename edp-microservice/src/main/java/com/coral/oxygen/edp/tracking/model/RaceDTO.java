package com.coral.oxygen.edp.tracking.model;

import java.io.Serializable;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RaceDTO implements Serializable {

  private String diomed;
  private String courseName;
  private String goingCode;
  private String going;
  private String obStartTime;
  private Integer rpCourseId;
  private String raceName;
  private Integer yards;
  private String distance;
  private String verdict;
  private String time;
  private Integer rpRaceId;
  private String raceType;
  private List<HorseDTO> horses;
}
