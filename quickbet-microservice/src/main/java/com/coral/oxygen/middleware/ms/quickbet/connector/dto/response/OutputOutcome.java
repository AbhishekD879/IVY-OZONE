package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by azayats on 24.10.17. */
@Data
@NoArgsConstructor
@AllArgsConstructor
public final class OutputOutcome {
  private String id;
  private String name;
  private String outcomeStatusCode;
  private String outcomeMeaningMajorCode;
  private String outcomeMeaningMinorCode;
  private boolean hasPriceStream;
}
