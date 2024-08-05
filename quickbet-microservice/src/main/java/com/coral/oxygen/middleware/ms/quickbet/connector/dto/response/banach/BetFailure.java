package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach;

/** Created by JacksonGenerator on 5/4/18. */
import java.util.List;
import lombok.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BetFailure {
  private Integer betNo;

  @Singular("betErrorItem")
  private List<BetErrorItem> betError;

  private String betMaxStake;
  private String betMinStake;
}
