package com.ladbrokescoral.cashout.model.safbaf;

import com.coral.bpp.api.model.bet.api.response.accountHistory.response.BetSummaryModel;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Outcome;
import com.coral.bpp.api.model.bet.api.response.accountHistory.response.Part;
import com.ladbrokescoral.cashout.service.SelectionData;
import java.math.BigInteger;
import java.util.List;
import java.util.stream.Collectors;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

@Data
@EqualsAndHashCode(callSuper = true)
public class Event extends Entity implements HasStatus {
  private BigInteger eventKey;
  private String eventStatus;
  private String isEventStarted;
  private String eventFlagCodes;
  private boolean isEventFinished;

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Override
  public boolean changeStatus(SelectionData data, boolean newStatus) {
    return data.changeEventStatus(newStatus);
  }

  @Override
  public String getStatus() {
    return getEventStatus();
  }

  @Override
  public String reasonForUpdate() {
    return "StatusChanged/Event/" + this.getEventStatus();
  }

  public void applyEventStartedChange(SelectionData data) {
    String isEventStartedValue = this.isEventStarted.equalsIgnoreCase("true") ? "Y" : "N";
    for (BetSummaryModel bet : data.getBets()) {
      for (Part part : partsInLeg(bet)) {
        Outcome outcome = part.getOutcome().get(0);
        BigInteger selectionId = new BigInteger(outcome.getId());
        if (selectionId == data.getSelectionId()) {
          ASYNC_LOGGER.info(
              " Updated outcome isOff value for eventId {} ,selectionId {} ,oldIsEventStartedValue {} newUpdatedValue {}",
              this.eventKey,
              data.getSelectionId(),
              outcome.getEvent().getIsOff(),
              isEventStartedValue);
          outcome.getEvent().setIsOff(isEventStartedValue);
        }
      }
    }
  }

  private static List<Part> partsInLeg(BetSummaryModel bet) {
    return bet.getLeg().stream().flatMap(l -> l.getPart().stream()).collect(Collectors.toList());
  }
}
