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
public class BetFailureDetail {
  private Long eventId;
  private Integer priceNum;
  private Integer priceDen;
  private String outcomeName;
  private String eventName;
  private Long outcomeId;
  private Long variantId;
}
