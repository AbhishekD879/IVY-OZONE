package com.oxygen.publisher.sportsfeatured.context;

import static com.oxygen.publisher.sportsfeatured.context.SportsSocketMessages.*;
import static com.oxygen.publisher.sportsfeatured.util.SportsHelper.*;

import com.corundumstudio.socketio.AckRequest;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.newrelic.api.agent.NewRelic;
import com.newrelic.api.agent.Trace;
import com.oxygen.publisher.context.AbstractSessionContext;
import com.oxygen.publisher.context.AbstractSocketEventListener;
import com.oxygen.publisher.model.ApplicationVersion;
import com.oxygen.publisher.model.BaseObject;
import com.oxygen.publisher.model.TicksMetrics;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.ModuleRawIndex;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SegmentedFeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.util.SegmentedFeaturedModelHelper;
import com.oxygen.publisher.sportsfeatured.visitor.SocketIoRoomSubscriber;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

/**
 * Manages socket events.
 *
 * @author tvuyiv
 */
@RequiredArgsConstructor
@Slf4j
public class SportsSessionContext extends AbstractSessionContext {

  public static final String CLIENT_TYPE_PARAMETER_NAME = "clientType";
  private static final String SCBRD = "SCBRD";
  @Getter private final ApplicationVersion appVersion;
  private final SportsMiddlewareContext featuredMiddlewareContext;
  private static final String UNIVERSAL_SEGMENT = "Universal";

  /**
   * Called on 'subscribe' event. Subscribes to the given module ids and emits their data if
   * connection has no version param. In case of segmented subscriptions, moduleid would be appended
   * with segment name as well (with # as separator) to retrieve the segmented eventmoduledata
   * records.
   *
   * @param client the socket relation
   * @param module the module to subscribe
   * @param ack the ack request
   */
  @Trace(metricName = "Websocket/onSubscribe", dispatcher = true)
  public void onSubscribe(SocketIOClient client, String module, AckRequest ack) {
    setRelicTransactionName("Websocket/onSubscribe", client);
    if (module != null && module.contains("#")) {
      moduleBasedSubscribe(client, module);
    }
  }

  /**
   * Called on 'subscribe' event. Subscribes to the given module ids and emits their data if
   * connection has version param
   *
   * @param client the socket relation
   * @param modules the modules to subscribe
   */
  @Trace(metricName = "Websocket/onSubscribe", dispatcher = true)
  public void onSubscribe(SocketIOClient client, Collection<Object> modules) {
    setRelicTransactionName("Websocket/onSubscribe", client);
    if (modules == null || modules.isEmpty()) {
      log.debug("Collection of room names to subscribe can not be empty.");
      return;
    }
    for (Object rnObject : modules) {
      final String roomName =
          rnObject instanceof String ? (String) rnObject : String.valueOf(rnObject);

      moduleBasedSubscribe(client, roomName);
    }
  }

  private void moduleBasedSubscribe(final SocketIOClient client, final String module) {

    final EventInputDTO eventInputDTO = getEventInputDTO(client, module, false);
    final PageRawIndex pageRawIndex =
        checkValidSportId(
            client, featuredMiddlewareContext.getFeaturedCachedData(), eventInputDTO.getSportId());

    eventInputDTO
        .getModuleId()
        .ifPresent(
            moduleId ->
                eventInputDTO
                    .getSegmentId()
                    .ifPresentOrElse(
                        segmentId ->
                            subscribeToModule(client, moduleId, module, segmentId, pageRawIndex),
                        () -> subscribeToModule(client, moduleId, module, pageRawIndex)));
  }

  /**
   * Called on 'unsubscribe' event. Unsubscribes from the given module ids if connection has a
   * 'module=featured' query param.
   *
   * @param client the socket relation
   * @param modules the modules to subscribe
   * @param ack the ack request
   */
  @Trace(metricName = "Websocket/onUnsubscribe", dispatcher = true)
  public void onUnsubscribe(SocketIOClient client, Collection<String> modules, AckRequest ack) {
    setRelicTransactionName("Websocket/onUnsubscribe", client);
    modules.forEach(
        room -> {
          log.debug("{} relation leaving {} room.", client.getSessionId(), room);
          client.leaveRoom(room);
        });
  }

  @Trace(metricName = "Websocket/pageEnd", dispatcher = true)
  public void pageEnd(final SocketIOClient client, final String sportId) {
    setRelicTransactionName("Websocket/pageEnd", client);

    client.getAllRooms().forEach(client::leaveRoom);
    log.info("successfully leaved all rooms.");
  }

  private void universalSubscriptions(
      String segment, SocketIOClient client, final PageRawIndex pageId) {
    FeaturedModel structure =
        featuredMiddlewareContext.getFeaturedCachedData().getStructure(pageId);

    client.joinRoom(pageId.getSportId() + HASH + FEATURED_STRUCTURE_CHANGED.messageId());
    if (structure != null) {
      SegmentView segmentView = new SegmentView();
      if (structure.getSegmentWiseModules() != null
          && structure.getSegmentWiseModules().containsKey(segment)) {
        segmentView = structure.getSegmentWiseModules().get(segment);
      }
      List<AbstractFeaturedModule<?>> nonSegmentedModules = new ArrayList<>();
      SegmentedFeaturedModelHelper.fillNonSegmentedModules(structure, nonSegmentedModules);
      SegmentedFeaturedModel segmentedFeaturedModel =
          SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(structure);
      SegmentedFeaturedModelHelper.populateSegmentedFeaturedModel(
          structure, segmentedFeaturedModel, segmentView);
      segmentedFeaturedModel.addModules(nonSegmentedModules);
      CompletableFuture.runAsync(
          () -> {
            SocketIoRoomSubscriber initVisitor = new SocketIoRoomSubscriber(client, this);
            segmentedFeaturedModel.getModules().stream().forEach(m -> m.accept(initVisitor));
          });

      if (!segmentedFeaturedModel.isUseFSCCached()) {
        client.sendEvent(FEATURED_STRUCTURE_CHANGED.messageId(), segmentedFeaturedModel);
      }

    } else {
      client.sendEvent(FEATURED_STRUCTURE_CHANGED.messageId(), emptyModel(pageId));
    }
  }

  private void segmentedSubscriptions(String segment, SocketIOClient client, PageRawIndex pageId) {
    FeaturedModel structure =
        featuredMiddlewareContext.getFeaturedCachedData().getStructure(pageId);
    if (structure != null && structure.getSegmentWiseModules() != null) {
      if (!structure.getSegmentWiseModules().containsKey(segment)) {
        universalSubscriptions(UNIVERSAL_SEGMENT, client, pageId);
      } else {
        client.getAllRooms().stream().parallel().forEach(client::leaveRoom);
        SegmentView segmentView = structure.getSegmentWiseModules().get(segment);
        List<AbstractFeaturedModule<?>> nonSegmentedModules = new ArrayList<>();
        SegmentedFeaturedModelHelper.fillNonSegmentedModules(structure, nonSegmentedModules);
        SegmentedFeaturedModel segmentedFeaturedModel =
            SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(structure);
        SegmentedFeaturedModelHelper.populateSegmentedFeaturedModel(
            structure, segmentedFeaturedModel, segmentView);
        segmentedFeaturedModel.addModules(nonSegmentedModules);
        CompletableFuture.runAsync(
            () -> {
              SocketIoRoomSubscriber initVisitor = new SocketIoRoomSubscriber(client, this);
              segmentedFeaturedModel.getModules().stream()
                  .forEach(
                      (AbstractFeaturedModule<?> m) -> {
                        if (m instanceof SurfaceBetModule || m instanceof QuickLinkModule) {
                          m.accept(initVisitor, segment);
                        } else {
                          m.accept(initVisitor);
                        }
                      });
            });
        client.sendEvent(FEATURED_STRUCTURE_CHANGED.messageId(), segmentedFeaturedModel);
        client.joinRoom(
            pageId.getSportId() + HASH + segment + HASH + FEATURED_STRUCTURE_CHANGED.messageId());
      }
    }
  }

  /**
   * fanzoneSegmentedSubscriptions for each fanzone segment. It will get FeaturedModel structure
   * from chache via passing pageId & bassed on structure its prepare segmented data and send out to
   * SocketIOClient.
   *
   * @param segment
   * @param client
   */
  private void fanzoneSegmentedSubscriptions(
      String segment, SocketIOClient client, PageRawIndex pageId) {
    log.info("Started executing fanzoneSegmentedSubscriptions");
    FeaturedModel structure =
        featuredMiddlewareContext.getFeaturedCachedData().getStructure(pageId);
    if (structure != null && structure.getFanzoneSegmentWiseModules() != null) {
      FanzoneSegmentView fanzoneSegmentView = structure.getFanzoneSegmentWiseModules().get(segment);
      SegmentedFeaturedModel segmentedFeaturedModel =
          SegmentedFeaturedModelHelper.createSegmentedFeaturedModel(structure);
      if (fanzoneSegmentView != null) {
        SegmentedFeaturedModelHelper.populateFanzoneSegmentedFeaturedModel(
            structure, segmentedFeaturedModel, fanzoneSegmentView, segment);
      }
      CompletableFuture.runAsync(
          () -> {
            SocketIoRoomSubscriber initVisitor = new SocketIoRoomSubscriber(client, this);
            segmentedFeaturedModel.getModules().stream()
                .forEach(
                    (AbstractFeaturedModule<?> m) -> {
                      if (m instanceof SurfaceBetModule
                          || m instanceof QuickLinkModule
                          || m instanceof TeamBetsModule
                          || m instanceof FanBetsModule) {
                        m.accept(initVisitor, segment);
                      } else {
                        m.accept(initVisitor);
                      }
                    });
          });
      client.sendEvent(FEATURED_STRUCTURE_CHANGED.messageId(), segmentedFeaturedModel);
      client.joinRoom(
          pageId.getSportId() + HASH + segment + HASH + FEATURED_STRUCTURE_CHANGED.messageId());
      log.info("Ended executing fanzoneSegmentedSubscriptions");
    }
  }

  private void defaultSubscriptions(PageRawIndex pageRawIndex, SocketIOClient client) {
    FeaturedModel structure =
        featuredMiddlewareContext.getFeaturedCachedData().getStructure(pageRawIndex);
    if (structure != null && structure.getModules() != null) {
      CompletableFuture.runAsync(
          () -> {
            SocketIoRoomSubscriber initVisitor = new SocketIoRoomSubscriber(client, this);
            structure.getModules().stream().parallel().forEach(m -> m.accept(initVisitor));
          });
    }
    log.debug("{} send >> application version.", client.getSessionId());
    FeaturedModel model = structure != null ? structure : emptyModel(pageRawIndex);
    if (!model.isUseFSCCached()) {
      client.sendEvent(FEATURED_STRUCTURE_CHANGED.messageId(), model);
    }
    client.joinRoom(pageRawIndex.getSportId() + HASH + FEATURED_STRUCTURE_CHANGED.messageId());
  }

  private FeaturedModel emptyModel(PageRawIndex pageRawIndex) {
    return FeaturedModel.builder()
        .pageId(String.valueOf(pageRawIndex.getSportId()))
        .visible(false)
        .build();
  }

  /**
   * Called on a new socket connection. Emits the application version and featured model structure.
   * Subscribes a relation to subscribed events.
   *
   * @param client the socket relation.
   */
  @Trace(metricName = "Websocket/Connection", dispatcher = true)
  public void onConnect(SocketIOClient client) {
    final String sportPageId = getValidSportQueryParam(client);
    client.sendEvent(APP_VERSION_RESPONSE.messageId(), appVersion.getVersion());
    switchSportPages(client, sportPageId);
  }

  @Trace(metricName = "Websocket/switchSportPages", dispatcher = true)
  public void switchSportPages(final SocketIOClient client, final String newSportPageId) {

    final PageRawIndex pageRawIndex =
        checkValidSportId(
            client, featuredMiddlewareContext.getFeaturedCachedData(), newSportPageId);

    // leave all existing rooms for this client bcz it's not required have the old rooms
    client.getAllRooms().forEach(client::leaveRoom);

    try {
      setRelicTransactionName("Websocket/Connection", client);
      if (pageRawIndex.getSportId() == HOME_PAGE_ID) {
        universalSubscriptions(UNIVERSAL_SEGMENT, client, pageRawIndex);
      } else if (pageRawIndex.getSportId() == FAN_ZONE_PAGE_ID) {
        /*  Fanzone functionality  is for login case only so when on connect we should not give any
        response back.
          */
      } else {
        defaultSubscriptions(pageRawIndex, client);
      }
    } catch (Exception ex) {
      log.error("Exception while session creation.", ex);
      client.sendEvent(
          ERROR_500.messageId(),
          "Exception while session creation. SessionID#{}.",
          client.getSessionId());
      client.disconnect();
      NewRelic.noticeError(ex);
    }
  }

  public void onLogin(SocketIOClient client, String segment) {

    if (!StringUtils.isNotBlank(segment)) {
      throw new IllegalArgumentException("Segment must be present with sportId.");
    }

    final EventInputDTO eventInputDTO = getEventInputDTO(client, segment, true);
    final PageRawIndex pageRawIndex =
        checkValidSportId(
            client, featuredMiddlewareContext.getFeaturedCachedData(), eventInputDTO.getSportId());

    // leave all existing rooms for this client bcz it's not required have the old rooms
    client.getAllRooms().forEach(client::leaveRoom);

    eventInputDTO
        .getSegmentId()
        .ifPresentOrElse(
            (String eventSegment) -> {
              if (pageRawIndex.getSportId() == FAN_ZONE_PAGE_ID) {
                // It will prepared Fanzone segmented response based on requested fanzone segment.
                log.info("Started executing fanzone login flow");
                fanzoneSegmentedSubscriptions(eventSegment, client, pageRawIndex);
              } else {
                segmentedSubscriptions(eventSegment, client, pageRawIndex);
              }
            },
            () -> {
              log.debug("segment is empty.");
              universalSubscriptions(UNIVERSAL_SEGMENT, client, pageRawIndex);
            });
  }

  @Trace(metricName = "Websocket/onDisconnect", dispatcher = true)
  @Override
  public void onDisconnect(SocketIOClient client) {
    setRelicTransactionName("Websocket/onDisconnect", client);
    super.onDisconnect(client);
  }

  private void setRelicTransactionName(String transactionName, SocketIOClient client) {
    String clientType = client.getHandshakeData().getSingleUrlParam(CLIENT_TYPE_PARAMETER_NAME);
    transactionName += ClientType.from(clientType).getTypeInUrlForm();
    NewRelic.setTransactionName(null, transactionName);
  }

  private void subscribeToModule(
      SocketIOClient client, String moduleId, String eventName, PageRawIndex pageRawIndex) {
    subscribeToModule(client, moduleId, eventName, UNIVERSAL_SEGMENT, pageRawIndex);
  }

  private void subscribeToModule(
      SocketIOClient client,
      String moduleId,
      String eventName,
      String segmentName,
      PageRawIndex pageRawIndex) {

    if (moduleId == null || moduleId.isEmpty()) {
      log.debug("Room name to subscribe can not be empty.");
      return;
    }

    log.debug("Connection {} is joining to the {} room.", client.getSessionId(), moduleId);
    client.joinRoom(pageRawIndex.getSportId() + "#" + moduleId);
    AbstractFeaturedModule<?> module =
        featuredMiddlewareContext
            .getFeaturedCachedData()
            .getModuleIfPresent(new ModuleRawIndex(pageRawIndex, moduleId));
    if (module == null) {
      log.debug(
          "{} from the relation was requested a subscription to the {} module, but it doesn't exist",
          client.getSessionId(),
          moduleId);
      return;
    }

    if (module.isSegmented() && module instanceof EventsModule) {
      EventsModule eventsModule = (EventsModule) module.copyWithEmptyData();
      if (!module.getModuleSegmentView().containsKey(segmentName)) {
        segmentName = UNIVERSAL_SEGMENT;
      }
      if (!Objects.isNull(module.getModuleSegmentView().get(segmentName))) {
        eventsModule.setData(
            module
                .getModuleSegmentView()
                .get(segmentName)
                .getEventModules()
                .get(module.getId())
                .getEventsModuleData());
      }
      sendData(client, eventsModule, eventName);
    } else {
      sendData(client, module, eventName);
    }
  }

  private void sendData(SocketIOClient client, AbstractFeaturedModule<?> module, String eventName) {
    client.sendEvent(eventName, module);
    if (module.getData() != null) {
      module
          .getData()
          .forEach(
              item -> {
                log.debug("{} relation join {} room.", client.getSessionId(), item.getId());
                joinToRoom(client, String.valueOf(item.getId()));
              });
    }
  }

  private void joinToRoom(SocketIOClient client, String roomName) {
    if (roomName == null || roomName.isEmpty()) {
      log.debug("Name of room to be joined can not be empty.");
      return;
    }
    client.joinRoom(roomName);

    // Sending liveupdates on connect might cause performance issue.
    // Leaving this code here in case we need indeed need this

    sendLatestLiveUpdates(client, roomName);
  }

  public void sendLatestLiveUpdates(SocketIOClient client, String event) {
    BaseObject[] incUpdate = featuredMiddlewareContext.getFeaturedCachedData().getPayload(event);
    if (incUpdate != null) {
      Arrays.stream(incUpdate)
          .filter(payload -> SCBRD.equals(payload.getType()))
          .forEach(payload -> client.sendEvent(event, payload));
    }
  }

  @Override
  public TicksMetrics getTicksMetrics() {
    return featuredMiddlewareContext.getFeaturedCachedData().getTicksMetrics();
  }

  public void registerListeners(SocketIOServer server) {

    new AbstractSocketEventListener<String>(SUBSCRIBE.messageId(), String.class) {

      @Override
      public void onEventType(SocketIOClient socketIOClient, String data, AckRequest ackRequest) {
        onSubscribe(socketIOClient, data, ackRequest);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Collection>(SUBSCRIBE.messageId(), Collection.class) {
      @Override
      public void onEventType(
          SocketIOClient socketIOClient, Collection roomNames, AckRequest ackRequest) {
        onSubscribe(socketIOClient, roomNames);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<Collection>(UNSUBSCRIBE.messageId(), Collection.class) {

      @Override
      public void onEventType(
          SocketIOClient socketIOClient, Collection data, AckRequest ackRequest) {
        onUnsubscribe(socketIOClient, data, ackRequest);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<String>(
        GET_SEGMENTED_FEATURED_STRUCTURE.messageId(), String.class) {

      @Override
      public void onEventType(
          SocketIOClient socketIOClient, String segmentName, AckRequest ackRequest) {
        onLogin(socketIOClient, segmentName);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<String>(PAGE_SWITCH.messageId(), String.class) {

      @Override
      public void onEventType(
          SocketIOClient socketIOClient, String sportId, AckRequest ackRequest) {
        switchSportPages(socketIOClient, sportId);
      }
    }.registerListener(server);

    new AbstractSocketEventListener<String>(PAGE_END.messageId(), String.class) {

      @Override
      public void onEventType(
          SocketIOClient socketIOClient, String sportId, AckRequest ackRequest) {
        pageEnd(socketIOClient, sportId);
      }
    }.registerListener(server);
  }
}
