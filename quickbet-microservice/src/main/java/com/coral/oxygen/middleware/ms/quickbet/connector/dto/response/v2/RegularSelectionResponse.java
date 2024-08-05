package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.v2;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputEvent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.OutputPrice;
import com.entain.oxygen.bettingapi.model.bet.api.response.Freebet;
import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by azayats on 23.11.17. */
@Data
@NoArgsConstructor
public class RegularSelectionResponse {
  private OutputEvent event;
  private OutputPrice selectionPrice;
  private RegularSelectionRequest request;
  private OddsBoostToken oddsBoost;
  private boolean lDip;
  private String lDipMar;
  private List<Freebet> freebetList;
  private String maxPayout;
}
