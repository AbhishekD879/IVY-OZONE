package com.entain.oxygen.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import java.time.LocalDateTime;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class MUserStable {

  private String userName;

  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSzz", timezone = "UTC")
  private LocalDateTime lastModifiedAt;
}
