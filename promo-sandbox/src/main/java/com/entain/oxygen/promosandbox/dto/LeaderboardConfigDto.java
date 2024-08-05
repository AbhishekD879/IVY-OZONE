package com.entain.oxygen.promosandbox.dto;

import java.io.Serializable;
import lombok.Data;

@Data
public class LeaderboardConfigDto implements Serializable {
  private static final long serialVersionUID = 1L;
  private String leaderboardId;
  private String filePath;
}
