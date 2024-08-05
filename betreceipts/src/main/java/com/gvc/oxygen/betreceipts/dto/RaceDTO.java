package com.gvc.oxygen.betreceipts.dto;

import java.io.Serializable;
import java.util.List;
import lombok.Data;
import nonapi.io.github.classgraph.json.Id;
import org.springframework.data.redis.core.RedisHash;

@Data
@RedisHash("df")
public class RaceDTO implements Serializable {

  private String diomed;
  @Id private String id;
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
