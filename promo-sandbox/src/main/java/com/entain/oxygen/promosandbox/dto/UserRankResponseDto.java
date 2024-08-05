package com.entain.oxygen.promosandbox.dto;

import java.io.Serializable;
import java.time.Instant;
import lombok.Data;

@Data
public class UserRankResponseDto implements Serializable {
  private static final long serialVersionUID = 1L;
  private transient Instant lastFileModified;
  private transient Object userRank;
  private transient Object topXRank;
}
