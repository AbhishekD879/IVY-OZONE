package com.oxygen.publisher.sportsfeatured.util;

import static com.oxygen.publisher.sportsfeatured.context.SportsSocketMessages.ERROR_400;

import com.corundumstudio.socketio.SocketIOClient;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.model.module.EventInputDTO;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SportsHelper {

  public static final String HASH = "#";
  public static final String SPORT_ID = "sportId";
  public static final int HOME_PAGE_ID = 0;
  public static final int FAN_ZONE_PAGE_ID = 160;

  public static final int ONE = 1;
  public static final int TWO = 2;
  public static final int THREE = 3;

  private SportsHelper() {}

  public static EventInputDTO getEventInputDTO(
      final SocketIOClient client, final String eventInput, final boolean isLogin) {

    final String[] events = eventInput.split(HASH);

    EventInputDTO.Builder builder = EventInputDTO.builder();

    if (isLogin) {
      if (events.length == ONE) {
        builder.withSportId(events[0]);
      } else if (events.length == TWO) {
        builder.withSportId(events[0]);
        builder.withSegmentId(events[1]);
      } else {
        final IllegalStateException illegalStateException =
            new IllegalStateException("Invalid combination found in the onLogin from UI.");

        log.error("Exception while session creation.", illegalStateException);
        client.sendEvent(
            ERROR_400.messageId(),
            "Invalid combination found in the onLogin from UI: {}",
            eventInput,
            "  Please enter valid combination like sportId# or sportId#segmentId");
      }
    } else {

      // these checks help us to avoid the ArrayIndexOutOfBoundsException
      if (events.length == TWO) {
        builder.withSportId(events[0]);
        builder.withModuleId(events[1]);
      } else if (events.length == THREE) {
        builder.withSportId(events[0]);
        builder.withModuleId(events[1]);
        builder.withSegmentId(events[TWO]);
      } else {
        final IllegalStateException illegalStateException =
            new IllegalStateException("Invalid combination found in the onSubscribe from UI.");
        log.error("Exception while session creation.", illegalStateException);
        client.sendEvent(
            ERROR_400.messageId(),
            "Invalid combination found in the onSubscribe from UI: {}",
            eventInput,
            "  Please enter valid combination like sportId#moduleId or sportId#moduleId#segmentId");
      }
    }

    return builder.build();
  }

  public static PageRawIndex checkValidSportId(
      final SocketIOClient client, final SportsCachedData cache, final String sportId) {

    final IllegalArgumentException exception;
    if (cache.getSportPageData().containsKey(sportId)) {
      return cache.getSportPageData().get(sportId);
    } else {
      exception =
          new IllegalArgumentException(
              "Invalid sportId found in page-switch call. the sportId is: " + sportId);
      log.error("Exception while page-switch. ", exception);
      client.sendEvent(
          ERROR_400.messageId(),
          "Invalid sportId found in page-switch call from UI. the sportId is: {}",
          sportId,
          "  Please enter valid sportId, that available in CMS.");
    }

    throw exception;
  }

  public static String getValidSportQueryParam(SocketIOClient client) {

    final IllegalArgumentException exception;
    String sportId = client.getHandshakeData().getSingleUrlParam(SPORT_ID);
    if (sportId != null) {
      return sportId;
    } else {
      exception =
          new IllegalArgumentException(
              "sportId query-param not found in onConnect call. the url is: "
                  + client.getHandshakeData().getUrl());
      log.error("Exception while onConnect. ", exception);
      client.sendEvent(
          ERROR_400.messageId(),
          "sportId query-param not found in onConnect from UI. the url is: {}",
          client.getHandshakeData().getUrl(),
          "  Please add the sportId as query param in onConnect call.");
    }
    throw exception;
  }
}
