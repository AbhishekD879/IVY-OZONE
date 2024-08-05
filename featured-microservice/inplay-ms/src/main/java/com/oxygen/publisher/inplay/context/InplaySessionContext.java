package com.oxygen.publisher.inplay.context;

import static com.oxygen.publisher.inplay.context.InplaySocketMessages.*;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.context.AbstractSessionContext;
import com.oxygen.publisher.context.AbstractSocketEventListener;
import com.oxygen.publisher.inplay.service.request.GetSportRequestData;
import com.oxygen.publisher.inplay.service.request.GetTypeRequestData;
import com.oxygen.publisher.inplay.service.request.YesNoFlag;
import com.oxygen.publisher.model.BaseObject;
import com.oxygen.publisher.model.InPlayCache;
import com.oxygen.publisher.model.ModuleDataItem;
import com.oxygen.publisher.model.RawIndex;
import com.oxygen.publisher.model.SportSegment;
import com.oxygen.publisher.model.TicksMetrics;
import java.util.*;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

/** Created by Aliaksei Yarotski on 1/29/18. */
@RequiredArgsConstructor
@Slf4j
public class InplaySessionContext extends AbstractSessionContext {

  @Getter private final String appVersion;
  private final InplayMiddlewareContext inplayMiddlewareContext;
  private static final Object EMPTY_RESPONSE = new Object();

  public TicksMetrics getTicksMetrics() {
    return inplayMiddlewareContext.getInplayCachedData().getTicksMetrics();
  }

  @Override
  @Trace(metricName = "Websocket/onConnect", dispatcher = true)
  public void onConnect(SocketIOClient client) {
    log.info("New Connection # {}", client.getSessionId());
    client.sendEvent(APP_VERSION_RESPONSE.messageId(), getAppVersion());
  }

  /**
   * Called on 'GET_RIBBON' event.
   *
   * @param client the socket relation
   */
  @Trace(metricName = "Websocket/onGetRibbon", dispatcher = true)
  public void onGetRibbon(SocketIOClient client) {
    client.sendEvent(
        GET_RIBBON_RESPONSE.messageId(),
        inplayMiddlewareContext.getInplayCachedData().getSportsRibbon());
  }

  /**
   * Called on 'GET_VIRTUAL_SPORTS_RIBBON_REQUEST' event
   *
   * @param client the socket relation
   */
  @Trace(metricName = "Websocket/onGetVirtualRibbon", dispatcher = true)
  public void onGetVirtualRibbon(SocketIOClient client) {
    client.sendEvent(
        GET_VIRTUAL_SPORTS_RIBBON_RESPONSE.messageId(),
        inplayMiddlewareContext.getInplayCachedData().getStructure().getVirtualSportList());
  }

  /**
   * Called on 'GET_LS_RIBBON' event.
   *
   * @param client the socket relation
   */
  @Trace(metricName = "Websocket/onGetRibbonWithLiveStreamsEvents", dispatcher = true)
  public void onGetRibbonWithLiveStreamsEvents(SocketIOClient client) {
    client.sendEvent(
        GET_LS_RIBBON_RESPONSE.messageId(),
        inplayMiddlewareContext.getInplayCachedData().getSportsRibbonWithLiveStreams());
  }

  /*
  Close client session if cache wasn't populated at least one time. Closed connection
   */
  private boolean cachePopulatedAtLeastOnce(SocketIOClient client) {
    if (inplayMiddlewareContext.getInplayCachedData().getStructure() == null) {
      client.disconnect();
      String errorMessage =
          String.format(
              "Unexpected state! Inplay cache is null. Closing connection for %s user.",
              String.valueOf(client.getSessionId()));
      log.error(errorMessage);
      NewRelic.noticeError(errorMessage);
      return false;
    }
    return true;
  }

  /**
   * Called on 'GET_INPLAY_STRUCTURE' event.
   *
   * @param client the socket relation
   */
  @Trace(metricName = "Websocket/onGetInplayStructure", dispatcher = true)
  public void onGetInplayStructure(SocketIOClient client) {
    if (cachePopulatedAtLeastOnce(client)) {
      client.sendEvent(
          GET_INPLAY_STRUCTURE_RESPONSE.messageId(),
          inplayMiddlewareContext.getInplayCachedData().getStructureWithoutStreamEvents());
    }
  }

  /**
   * Called on 'GET_INPLAY_LS_STRUCTURE' event.
   *
   * @param client the socket relation
   */
  @Trace(metricName = "Websocket/onGetInplayStructureWithLiveStream", dispatcher = true)
  public void onGetInplayStructureWithLiveStreams(SocketIOClient client) {
    if (cachePopulatedAtLeastOnce(client)) {
      client.sendEvent(
          GET_INPLAY_LS_STRUCTURE_RESPONSE.messageId(),
          inplayMiddlewareContext.getInplayCachedData().getStructure());
    }
  }

  /**
   * Called on 'GET_SPORT' event.
   *
   * @param client the socket relation
   * @param requestData deserialized request parameters
   */
  @Trace(metricName = "Websocket/onGetSport", dispatcher = true)
  public void onGetSport(SocketIOClient client, Map<String, Object> requestData) {
    GetSportRequestData sportRequestData = new GetSportRequestData(requestData);
    if (!sportRequestData.isValid()) {
      return;
    }
    String responseMessage =
        String.format(
            GET_SPORT_RESPONSE_TEMPLATE.messageId(),
            sportRequestData.getCategoryId() + "::" + sportRequestData.getTopLevelType());

    String marketSelector = sportRequestData.getMarketSelector();
    if (marketSelector != null && marketSelector.contains(",")) {
      getSportForSLP(sportRequestData, client, responseMessage);
    } else {
      InPlayCache.SportSegmentCache sportSegmentCache =
          getSportSegmentCacheForGetSport(sportRequestData, sportRequestData.getMarketSelector());
      if (sportSegmentCache == null) {
        client.sendEvent(responseMessage, EMPTY_RESPONSE);
        return;
      }
      SportSegment sportSegment = sportSegmentCache.getSportSegment();
      if (YesNoFlag.YES.getValue().equals(sportRequestData.getAutoUpdates())) {
        sportSegment.getEventsIds().stream()
            .filter(Objects::nonNull)
            .forEach(
                eventId -> {
                  client.joinRoom(String.valueOf(eventId));
                });
      }
      client.sendEvent(responseMessage, sportSegment);
    }
  }

  private void getSportForSLP(
      GetSportRequestData sportRequestData, SocketIOClient client, String responseMessage) {
    List<String> marketSelectors = Arrays.asList(sportRequestData.getMarketSelector().split(","));
    List<SportSegment> allSportSegments = new ArrayList<>();
    marketSelectors.forEach(
        (String selector) -> {
          InPlayCache.SportSegmentCache sportSegmentCache =
              getSportSegmentCacheForGetSport(sportRequestData, selector);
          if (sportSegmentCache == null) {
            return;
          }
          SportSegment sportSegment = sportSegmentCache.getSportSegment();
          if (YesNoFlag.YES.getValue().equals(sportRequestData.getAutoUpdates())) {
            sportSegment.getEventsIds().stream()
                .filter(Objects::nonNull)
                .forEach((Integer eventId) -> client.joinRoom(String.valueOf(eventId)));
          }
          allSportSegments.add(sportSegment);
        });
    if (allSportSegments.isEmpty()) {
      client.sendEvent(responseMessage, EMPTY_RESPONSE);
    } else {
      client.sendEvent(responseMessage, allSportSegments);
    }
  }

  private InPlayCache.SportSegmentCache getSportSegmentCacheForGetSport(
      GetSportRequestData sportRequestData, String marketSelector) {
    RawIndex index =
        RawIndex.builder()
            .categoryId(sportRequestData.getCategoryId())
            .topLevelType(sportRequestData.getTopLevelType())
            .marketSelector(marketSelector)
            .build();
    InPlayCache.SportSegmentCache sportSegmentCache;
    if (YesNoFlag.YES.getValue().equals(sportRequestData.getEmptyTypes())) {
      sportSegmentCache =
          inplayMiddlewareContext.getInplayCachedData().getSportSegmentsWithEmptyTypes().get(index);
    } else {
      sportSegmentCache =
          inplayMiddlewareContext.getInplayCachedData().getSportSegments().get(index);
    }
    return sportSegmentCache;
  }

  /**
   * Called on 'GET_TYPE' event.
   *
   * @param client the socket relation
   * @param requestDataMap deserialized request parameters
   */
  @Trace(metricName = "Websocket/onGetType", dispatcher = true)
  public void onGetType(SocketIOClient client, Map<String, Object> requestDataMap) {
    GetTypeRequestData requestData = new GetTypeRequestData(requestDataMap);
    if (!requestData.isValid()) {
      return;
    }
    String marketSelector = requestData.getMarketSelector();
    if (marketSelector != null && marketSelector.contains(",")) {
      List<String> marketSelectors = Arrays.asList(marketSelector.split(","));
      List<ModuleDataItem> allModuleDataItems = new ArrayList<>();
      marketSelectors.forEach(
          (String selector) -> {
            InPlayCache.SportSegmentCache sportSegmentCache =
                getSportSegmentCacheByMarketSelector(requestData, selector);
            if (sportSegmentCache == null) {
              return;
            }
            List<ModuleDataItem> moduleDataItems = sportSegmentCache.getModuleDataItem();
            if (moduleDataItems != null) {
              moduleDataItems.forEach(
                  (ModuleDataItem moduleDataItem) -> moduleDataItem.setMarketSelector(selector));
            }
            allModuleDataItems.addAll(moduleDataItems);
          });
      if (allModuleDataItems.isEmpty()) {
        client.sendEvent(getResponseMessage(requestData), EMPTY_RESPONSE);
      } else {
        client.sendEvent(getResponseMessage(requestData), allModuleDataItems);
      }
    } else {
      InPlayCache.SportSegmentCache sportSegmentCache =
          getSportSegmentCacheByMarketSelector(requestData, requestData.getMarketSelector());
      if (sportSegmentCache == null) {
        client.sendEvent(getResponseMessage(requestData), EMPTY_RESPONSE);
        return;
      }
      List<ModuleDataItem> moduleDataItems = sportSegmentCache.getModuleDataItem();
      client.sendEvent(getResponseMessage(requestData), moduleDataItems);
    }
  }

  private String getResponseMessage(GetTypeRequestData requestData) {
    RawIndex index =
        RawIndex.builder()
            .categoryId(requestData.getCategoryId())
            .topLevelType(requestData.getTopLevelType())
            .marketSelector(requestData.getMarketSelector())
            .typeId(requestData.getTypeId())
            .build();
    return String.format(GET_TYPE_RESPONSE_TEMPLATE.messageId(), index.toStructuredKey());
  }

  private InPlayCache.SportSegmentCache getSportSegmentCacheByMarketSelector(
      GetTypeRequestData requestData, String marketSelector) {
    RawIndex index =
        RawIndex.builder()
            .categoryId(requestData.getCategoryId())
            .topLevelType(requestData.getTopLevelType())
            .marketSelector(marketSelector)
            .typeId(requestData.getTypeId())
            .build();
    return inplayMiddlewareContext.getInplayCachedData().getSportSegments().get(index);
  }

  private void joinToRoom(SocketIOClient client, String roomName) {
    if (roomName.isEmpty()) {
      log.debug("Name of room to be joined can not be empty.");
      return;
    }
    client.joinRoom(roomName);
  }

  private void leaveRoom(SocketIOClient client, String roomName) {
    if (roomName.isEmpty()) {
      log.debug("Name of room to be leaved can not be empty.");
      return;
    }
    client.leaveRoom(roomName);
  }

  /**
   * Called on subscribe request.
   *
   * @param client the socket relation
   * @param roomName the name of room to be joined
   */
  public void onSubscribe(SocketIOClient client, String roomName) {
    log.debug("ClientId: {} on room {}", client.getSessionId(), roomName);
    joinToRoom(client, roomName);
  }

  /**
   * Called on subscribe request. Expected EventIds.
   *
   * @param client the socket relationBuilderCompetitionDifferenceTest
   * @param roomNames the name of rooms to be joined
   */
  public void onSubscribe(SocketIOClient client, Collection<Object> roomNames) {
    for (Object rnObject : roomNames) {
      final String roomName = String.valueOf(rnObject);
      client.joinRoom(roomName);
      BaseObject[] incUpdate = inplayMiddlewareContext.getInplayCachedData().getPayload(roomName);
      if (incUpdate != null) {
        for (BaseObject payload : incUpdate) {
          log.debug(
              "[InplaySessionContext:onSubscribe] clientId {}; room {}; payload {}",
              client.getSessionId(),
              roomName,
              payload);
          client.sendEvent(roomName, payload);
        }
      }
    }
  }

  /**
   * Called on subscribe request.
   *
   * @param client the socket relation
   * @param roomName the name of room to be leaved
   */
  public void onUnsubscribe(SocketIOClient client, String roomName) {
    leaveRoom(client, roomName);
  }

  /**
   * Called on subscribe request.
   *
   * @param client the socket relation
   * @param roomNames the name of rooms to be leaved
   */
  public void onUnsubscribe(SocketIOClient client, Collection<Object> roomNames) {
    for (Object rnObject : roomNames) {
      final String roomName = String.valueOf(rnObject);
      client.leaveRoom(roomName);
    }
  }

  @Override
  public void registerListeners(SocketIOServer server) {
    new AbstractSocketEventListener<Object>(GET_RIBBON_REQUEST.messageId(), Object.class) {
      @Override
      public void onEventType(SocketIOClient socketIOClient, Object data, AckRequest ackRequest) {
        onGetRibbon(socketIOClient);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Object>(GET_LS_RIBBON_REQUEST.messageId(), Object.class) {
      @Override
      public void onEventType(SocketIOClient socketIOClient, Object data, AckRequest ackRequest) {
        onGetRibbonWithLiveStreamsEvents(socketIOClient);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Object>(
        GET_INPLAY_STRUCTURE_REQUEST.messageId(), Object.class) {
      @Override
      public void onEventType(SocketIOClient socketIOClient, Object data, AckRequest ackRequest) {
        onGetInplayStructure(socketIOClient);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Object>(
        GET_INPLAY_LS_STRUCTURE_REQUEST.messageId(), Object.class) {
      @Override
      public void onEventType(SocketIOClient socketIOClient, Object data, AckRequest ackRequest) {
        onGetInplayStructureWithLiveStreams(socketIOClient);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Map>(GET_SPORT_REQUEST.messageId(), Map.class) {
      @Override
      public void onEventType(
          SocketIOClient socketIOClient, Map requestData, AckRequest ackRequest) {
        onGetSport(socketIOClient, requestData);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Map>(GET_TYPE_REQUEST.messageId(), Map.class) {
      @Override
      public void onEventType(
          SocketIOClient socketIOClient, Map requestData, AckRequest ackRequest) {
        onGetType(socketIOClient, requestData);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<String>(SUBSCRIBE.messageId(), String.class) {
      @Override
      public void onEventType(
          SocketIOClient socketIOClient, String roomName, AckRequest ackRequest) {
        onSubscribe(socketIOClient, roomName);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Collection>(SUBSCRIBE.messageId(), Collection.class) {
      @Override
      public void onEventType(
          SocketIOClient socketIOClient, Collection roomNames, AckRequest ackRequest) {
        onSubscribe(socketIOClient, roomNames);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<String>(UNSUBSCRIBE.messageId(), String.class) {
      @Override
      public void onEventType(
          SocketIOClient socketIOClient, String roomName, AckRequest ackRequest) {
        onUnsubscribe(socketIOClient, roomName);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Collection>(UNSUBSCRIBE.messageId(), Collection.class) {
      @Override
      public void onEventType(
          SocketIOClient socketIOClient, Collection roomNames, AckRequest ackRequest) {
        onUnsubscribe(socketIOClient, roomNames);
      }
    }.registerListener(server);
    registerVirtualSportsListener(server);
  }

  private void registerVirtualSportsListener(SocketIOServer server) {
    new AbstractSocketEventListener<Object>(
        GET_VIRTUAL_SPORTS_RIBBON_REQUEST.messageId(), Object.class) {
      @Override
      public void onEventType(SocketIOClient socketIOClient, Object data, AckRequest ackRequest) {
        onGetVirtualRibbon(socketIOClient);
      }
    }.registerListener(server);
  }
}
