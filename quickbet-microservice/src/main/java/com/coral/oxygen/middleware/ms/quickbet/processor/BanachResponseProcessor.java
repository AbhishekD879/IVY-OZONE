package com.coral.oxygen.middleware.ms.quickbet.processor;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public abstract class BanachResponseProcessor {

  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  protected BanachResponseProcessor nextProcessor;

  public void setNextProcessor(BanachResponseProcessor nextProcessor) {
    this.nextProcessor = nextProcessor;
  }

  /** Indicates that current processor is able to process response */
  protected abstract boolean canBeProcessed(PlaceBetResponseDto response);

  /** Processes the response by sending data to client using session object */
  protected abstract void doProcessResponse(Session session, PlaceBetResponseDto response);

  public void tryProcessResponse(Session session, PlaceBetResponseDto response) {
    if (canBeProcessed(response)) {
      ASYNC_LOGGER.info("Processing with {}", this.getClass().getSimpleName());
      doProcessResponse(session, response);
    } else if (nextProcessor != null) {
      nextProcessor.tryProcessResponse(session, response);
    } else {
      ASYNC_LOGGER.error("No banach response processors left");
      throw new IllegalStateException("No banach response processors left");
    }
  }

  protected void clearSelection(Session session) {
    session.setBanachSelectionData(null);
    session.save();
    session.unsubscribeFromAllRooms();
  }
}
