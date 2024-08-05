package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach;

/** Created by JacksonGenerator on 5/4/18. */
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BetErrorItem {
  private Integer betFailureCode;
  private String betFailureDesc;
  private String betFailureReason;
  private String betFailureDebug;
  private BetFailureDetail betFailureDetail;
}
