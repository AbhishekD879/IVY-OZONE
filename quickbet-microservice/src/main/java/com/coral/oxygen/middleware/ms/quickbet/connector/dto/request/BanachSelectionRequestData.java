package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request;

import com.ladbrokescoral.oxygen.byb.banach.dto.external.VirtualSelectionDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class BanachSelectionRequestData {
  private long obEventId;
  private List<Long> selectionIds = new ArrayList<>();
  private List<VirtualSelectionDto> playerSelections = new ArrayList<>();
}
