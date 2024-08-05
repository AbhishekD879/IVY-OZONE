package com.entain.oxygen.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
@EqualsAndHashCode(of = "horseId")
public class HorseInfo {

  private String horseId;
  private String horseName;
  private String note;
  private boolean notesAvailable;

  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSzz", timezone = "UTC")
  private LocalDateTime bookmarkedAt;

  private Boolean isCrcHorse;
}
