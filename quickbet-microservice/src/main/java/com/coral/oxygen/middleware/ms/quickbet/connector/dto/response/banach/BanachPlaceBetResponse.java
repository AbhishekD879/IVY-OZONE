package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach;

/** Created by JacksonGenerator on 5/4/18. */
import com.coral.oxygen.middleware.ms.quickbet.connector.ValidPrice;
import java.util.List;
import lombok.*;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class BanachPlaceBetResponse {
  private BetFailure betFailure;

  @Singular("betPlacementItem")
  private List<BetPlacementItem> betPlacement;

  private ValidPrice validPrice;
  private Integer responseCode;
}
