package com.ladbrokescoral.cashout.service.updates;

import static java.time.temporal.ChronoUnit.SECONDS;

import com.ladbrokescoral.cashout.model.context.UserRequestContextAccHistory;
import com.ladbrokescoral.cashout.model.safbaf.Entity;
import com.ladbrokescoral.cashout.model.safbaf.Event;
import com.ladbrokescoral.cashout.model.safbaf.Market;
import com.ladbrokescoral.cashout.model.safbaf.Selection;
import com.ladbrokescoral.cashout.model.safbaf.betslip.Betslip;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZoneOffset;
import java.time.format.DateTimeFormatter;
import lombok.RequiredArgsConstructor;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class UniversalUpdateProcessor implements UpdateProcessor<Entity> {

  private static final String UPDATE = "update";
  private static final long SYNC_DELTA_OB_KAFKA = 1L;
  private static final int MAX_MESSAGE_AGE_MINUTES = 5;

  private final EventUpdateProcessor eventUpdateProcessor;
  private final MarketUpdateProcessor marketUpdateProcessor;
  private final SelectionUpdateProcessor selectionUpdateProcessor;
  private final BetslipUpdateProcessor betslipUpdateProcessor;
  private final DateTimeFormatter isoFormatter = DateTimeFormatter.ISO_INSTANT;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Override
  public void process(UserRequestContextAccHistory userRequestContext, Entity msg) {
    if (isUpdateMsg(msg) && isANewUpdate(userRequestContext, msg)) {
      processSafUpdate(userRequestContext, msg);
    } else if (msg instanceof Betslip) {
      betslipUpdateProcessor.process(userRequestContext, (Betslip) msg);
    }
  }

  private boolean isANewUpdate(UserRequestContextAccHistory userRequestContext, Entity msg) {
    String recordModifiedTime = msg.getMeta().getRecordModifiedTime();
    try {
      LocalDateTime connectionDate =
          userRequestContext
              .getConnectionDate()
              .toInstant()
              .atZone(ZoneId.of(ZoneOffset.UTC.getId()))
              .minus(SYNC_DELTA_OB_KAFKA, SECONDS)
              .toLocalDateTime();
      Instant dateInstant = Instant.from(isoFormatter.parse(recordModifiedTime));
      LocalDateTime msgDate =
          LocalDateTime.ofInstant(dateInstant, ZoneId.of(ZoneOffset.UTC.getId()));

      Duration msgAge = Duration.between(LocalDateTime.now(), msgDate);
      boolean isNewMsg =
          connectionDate.isBefore(msgDate) && msgAge.toMinutes() < MAX_MESSAGE_AGE_MINUTES;
      if (isNewMsg) {
        ASYNC_LOGGER.debug(
            "Msg is NEW. Connection time - {}, Msg time - {}", connectionDate, msgDate);
      } else {
        ASYNC_LOGGER.warn(
            "Msg is OLD. Connection time - {}, Msg time - {} (msg age {})",
            connectionDate,
            msgDate,
            msgAge);
      }
      return isNewMsg;
    } catch (Exception e) {
      ASYNC_LOGGER.error("Unable parse date - {}", recordModifiedTime, e);
      return true;
    }
  }

  public void process(UserRequestContextAccHistory userRequestContext, Event msg) {
    eventUpdateProcessor.process(userRequestContext, msg);
  }

  public void process(UserRequestContextAccHistory userRequestContext, Market msg) {
    marketUpdateProcessor.process(userRequestContext, msg);
  }

  public void process(UserRequestContextAccHistory userRequestContext, Selection msg) {
    selectionUpdateProcessor.process(userRequestContext, msg);
  }

  public void process(UserRequestContextAccHistory userRequestContext, Betslip msg) {
    betslipUpdateProcessor.process(userRequestContext, msg);
  }

  private boolean isUpdateMsg(Entity msg) {
    return UPDATE.equals(msg.getMeta().getOperation());
  }

  private void processSafUpdate(UserRequestContextAccHistory userRequestContext, Entity msg) {
    if (msg instanceof Event) {
      eventUpdateProcessor.process(userRequestContext, (Event) msg);
    } else if (msg instanceof Market) {
      marketUpdateProcessor.process(userRequestContext, (Market) msg);
    } else if (msg instanceof Selection) {
      selectionUpdateProcessor.process(userRequestContext, (Selection) msg);
    }
  }
}
