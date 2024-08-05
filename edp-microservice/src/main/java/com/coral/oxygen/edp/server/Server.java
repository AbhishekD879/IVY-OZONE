package com.coral.oxygen.edp.server;

import com.coral.oxygen.edp.liveserv.BaseObject;
import com.coral.oxygen.edp.liveserv.LiveServConnector;
import com.coral.oxygen.edp.liveserv.LiveServMessageConverter;
import com.coral.oxygen.edp.model.output.OutputEvent;
import com.coral.oxygen.edp.tracking.Subscription;
import com.coral.oxygen.edp.tracking.Tracker;
import com.coral.oxygen.edp.tracking.model.CategoryToUpcomingEvent;
import com.coral.oxygen.edp.tracking.model.EventData;
import com.coral.oxygen.edp.tracking.model.FirstMarketsData;
import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.Envelope;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType;
import com.coral.oxygen.middleware.ms.liveserv.model.messages.MessageEnvelope;
import com.coral.oxygen.middleware.ms.liveserv.utils.StringUtils;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIONamespace;
import com.corundumstudio.socketio.SocketIOServer;
import com.newrelic.api.agent.NewRelic;
import java.math.BigInteger;
import java.util.Collection;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class Server {
  public static final String SUBSCRIBE_VIRTUAL_MARKETS = "11011";
  public static final String SUBSCRIBE_VIRTUAL_SPORTS = "11012";
  public static final String UNSUBSCRIBE_SPORTS = "11022";
  public static final String SUBSCRIBE_FIRST_5_MARKETS = "11001";
  public static final String UNSUBSCRIBE_ALL_MARKETS = "11002";
  public static final String SUBSCRIBE_NEXT_N_MARKETS = "11003";
  public static final String EVENT_DATA_RESPONSE = "12001"; // initial & update message
  public static final String SPORTS_DATA_RESPONSE = "12002";

  private final SocketIOServer sioServer;

  private final Tracker<Long, FirstMarketsData> firstmarketsTracker;

  private final Tracker<Long, EventData> virtualMarketsTracker;

  private final Tracker<String, List<CategoryToUpcomingEvent>> sportsTracker;

  private final LiveServConnector liveServConnector;

  private final Object lsSubscriptionLock = new Object();

  private final LiveServMessageConverter converter;

  @Autowired
  public Server(
      SocketIOServer sioServer,
      Tracker<Long, FirstMarketsData> firstmarketsTracker,
      Tracker<Long, EventData> virtualMarketsTracker,
      LiveServConnector liveServConnector,
      LiveServMessageConverter converter,
      Tracker<String, List<CategoryToUpcomingEvent>> sportsTracker) {
    this.sioServer = sioServer;
    this.firstmarketsTracker = firstmarketsTracker;
    this.liveServConnector = liveServConnector;
    this.converter = converter;
    this.virtualMarketsTracker = virtualMarketsTracker;
    this.sportsTracker = sportsTracker;
  }

  private void addToRoom(SocketIOClient client, Set<String> channels) {
    synchronized (lsSubscriptionLock) {
      channels.forEach(client::joinRoom);
    }
  }

  private void removeFromRoom(SocketIOClient client, Set<String> channels) {
    synchronized (lsSubscriptionLock) {
      channels.forEach(
          channel -> {
            client.leaveRoom(channel);
            Collection<SocketIOClient> clients = sioServer.getRoomOperations(channel).getClients();
            if (Objects.isNull(clients) || clients.isEmpty()) {
              liveServConnector.unsubscribe(channel);
            }
          });
    }
  }

  private Set<String> extractLiveServChannels(Object data) {
    if (data instanceof EventData) {
      EventData fmData = (EventData) data;
      OutputEvent event = fmData.getEvent();
      return extractLiveServChannelsFromEvent(event);
    }
    return new HashSet<>();
  }

  private Set<String> extractLiveServChannelsFromEvent(OutputEvent event) {
    Set<String> result = new HashSet<>();
    result.add(
        ChannelType.sEVENT.getName()
            + StringUtils.addLeadingZeros(String.valueOf(event.getId()), 10));
    result.add(
        ChannelType.sCLOCK.getName()
            + StringUtils.addLeadingZeros(String.valueOf(event.getId()), 10));
    result.add(
        ChannelType.sSCBRD.getName()
            + StringUtils.addLeadingZeros(String.valueOf(event.getId()), 10));
    event
        .getMarkets()
        .forEach(
            market -> {
              result.add(
                  ChannelType.sEVMKT.getName()
                      + StringUtils.addLeadingZeros(String.valueOf(market.getId()), 10));
              market
                  .getOutcomes()
                  .forEach(
                      outcome -> {
                        result.add(
                            ChannelType.sSELCN.getName()
                                + StringUtils.addLeadingZeros(String.valueOf(outcome.getId()), 10));
                        converter.addSelectionToMarketIdMapping(
                            new BigInteger(outcome.getId()), new BigInteger(market.getId()));
                      });
            });
    return result;
  }

  private <T, D> void configureNamespace(
      SocketIONamespace ns,
      Class<T> ticketClass,
      Tracker<T, D> tracker,
      Tracker<T, EventData> virtualMarketsTracker,
      Tracker<String, List<CategoryToUpcomingEvent>> sportsTracker) {
    // Key - SocketIO client Id, Value - MAP where (keys - all subscribed tickets, value - set of
    // liveServ channels)
    Map<String, Map<T, Set<String>>> ticketsMap = new ConcurrentHashMap<>();

    ns.addEventListener(
        SUBSCRIBE_VIRTUAL_SPORTS,
        ticketClass,
        (client, ticket, ackSender) -> listenSports(client, ticket, sportsTracker, ticketsMap));

    ns.addEventListener(
        SUBSCRIBE_VIRTUAL_MARKETS,
        ticketClass,
        (client, ticket, ackSender) ->
            listenVirtual(client, ticket, virtualMarketsTracker, ticketsMap));

    ns.addEventListener(
        SUBSCRIBE_FIRST_5_MARKETS,
        ticketClass,
        (client, ticket, ackSender) -> listenFirst5Markets(client, ticket, ticketsMap, tracker));

    ns.addEventListener(
        SUBSCRIBE_NEXT_N_MARKETS,
        String.class,
        (client, compositeTicket, ackSender) ->
            listenNextNMarkets(client, compositeTicket, ticketsMap, tracker));

    ns.addEventListener(
        UNSUBSCRIBE_ALL_MARKETS,
        ticketClass,
        (client, data, ackSender) -> {
          if (data == null) {
            log.warn(
                "Event id is missing in unsubscribe request, will not unsubscribe until client disconnected!");
            return;
          }
          String clientId = client.getSessionId().toString();
          tracker.removeSubscription(clientId, data); // data is a ticket/event_id
          virtualMarketsTracker.removeSubscription(clientId, data);
          Map<T, Set<String>> clientTickets =
              ticketsMap.getOrDefault(clientId, Collections.emptyMap());
          Set<String> lsChannels = clientTickets.getOrDefault(data, Collections.emptySet());
          clientTickets.remove(data);
          removeFromRoom(client, lsChannels);
          log.info("Unsubscribed {} to {}", clientId, data);
        });

    ns.addEventListener(
        UNSUBSCRIBE_SPORTS,
        String.class,
        (client, data, ackSender) -> {
          String clientId = client.getSessionId().toString();
          sportsTracker.removeSubscription(clientId, data);
          log.info("Unsubscribed {} to {}", clientId, data);
        });

    ns.addConnectListener(
        client -> {
          NewRelic.incrementCounter("Custom/onConnect");
          log.info("Connected {}", client.getSessionId());
        });

    ns.addDisconnectListener(
        client -> {
          NewRelic.incrementCounter("Custom/onDisconnect");
          String clientId = client.getSessionId().toString();
          Map<T, Set<String>> clientTickets =
              ticketsMap.getOrDefault(clientId, Collections.emptyMap());
          clientTickets
              .keySet()
              .forEach(
                  ticket -> {
                    tracker.removeSubscription(clientId, ticket);
                    virtualMarketsTracker.removeSubscription(clientId, ticket);
                    sportsTracker.removeSubscription(clientId, clientId);
                  });
          Set<String> lsChannels =
              clientTickets.values().stream()
                  .flatMap(Collection::stream)
                  .collect(Collectors.toSet());
          removeFromRoom(client, lsChannels);
          ticketsMap.remove(clientId);
          log.info("Disconnected {}", clientId);
        });
  }

  private <T> void listenSports(
      SocketIOClient client,
      T ticket,
      Tracker<String, List<CategoryToUpcomingEvent>> sportsTracker,
      Map<String, Map<T, Set<String>>> ticketsMap) {
    String clientId = client.getSessionId().toString();
    addClientTicket(clientId, ticket, ticketsMap);
    Subscription<String, List<CategoryToUpcomingEvent>> trackerClient =
        new Subscription<String, List<CategoryToUpcomingEvent>>(clientId, clientId, 1) {
          @Override
          public void emit(List<CategoryToUpcomingEvent> data) {
            client.sendEvent(SPORTS_DATA_RESPONSE, data);
          }
        };
    sportsTracker.addSubscription(trackerClient);
    logSubscribtion(clientId, ticket);
  }

  private <T> void logSubscribtion(String clientId, T ticket) {
    log.info("Subscribed {} to {}", clientId, ticket);
  }

  private <T> void listenVirtual(
      SocketIOClient client,
      T ticket,
      Tracker<T, EventData> virtualMarketsTracker,
      Map<String, Map<T, Set<String>>> ticketsMap) {

    String clientId = client.getSessionId().toString();
    addClientTicket(clientId, ticket, ticketsMap);
    Subscription<T, EventData> trackerClient =
        createSubscription(client, ticket, 5, Collections.emptySet(), EVENT_DATA_RESPONSE, false);
    virtualMarketsTracker.addSubscription(trackerClient);
    logSubscribtion(clientId, ticket);
  }

  private <T, D> void listenFirst5Markets(
      SocketIOClient client,
      T ticket,
      Map<String, Map<T, Set<String>>> ticketsMap,
      Tracker<T, D> tracker) {
    String clientId = client.getSessionId().toString();
    Set<String> channelsForClosure = addClientTicket(clientId, ticket, ticketsMap);
    Subscription<T, D> trackerClient =
        createSubscription(client, ticket, 5, channelsForClosure, EVENT_DATA_RESPONSE, true);
    tracker.addSubscription(trackerClient);
    logSubscribtion(clientId, ticket);
  }

  private <T, D> void listenNextNMarkets(
      SocketIOClient client,
      String compositeTicket,
      Map<String, Map<T, Set<String>>> ticketsMap,
      Tracker<T, D> tracker) {
    String[] params = compositeTicket.split("_");

    if (params.length != 2) {
      throw new IllegalArgumentException(
          "request should be eventId_eventsCount, e.g. \"12334566_10\"");
    }

    final T ticket = (T) Long.valueOf(params[0]);
    final int marketsLimit = Integer.parseInt(params[1]);

    String clientId = client.getSessionId().toString();
    Set<String> channelsForClosure = addClientTicket(clientId, ticket, ticketsMap);
    Subscription<T, D> trackerClient =
        createSubscription(
            client, ticket, marketsLimit, channelsForClosure, EVENT_DATA_RESPONSE, true);
    tracker.addSubscription(trackerClient);
    logSubscribtion(clientId, ticket);
  }

  private <T> Set<String> addClientTicket(
      String clientId, T ticket, Map<String, Map<T, Set<String>>> ticketsMap) {
    Map<T, Set<String>> clientTickets = new ConcurrentHashMap<>();
    Map<T, Set<String>> oldTickets = ticketsMap.putIfAbsent(clientId, clientTickets);
    if (oldTickets != null) {
      clientTickets = oldTickets;
    }
    Set<String> channels = ConcurrentHashMap.newKeySet();
    Set<String> oldChannels = clientTickets.putIfAbsent(ticket, channels);
    if (Objects.nonNull(oldChannels)) {
      channels = oldChannels;
    }
    return channels;
  }

  private <T, D> Subscription<T, D> createSubscription(
      SocketIOClient client,
      T ticket,
      Integer marketsLimit,
      Set<String> channelsForClosure,
      String responseRoom,
      boolean liveServUpdates) {
    return new Subscription<T, D>(client.getSessionId().toString(), ticket, marketsLimit) {

      @Override
      public void emit(D data) {
        if (!(data instanceof FirstMarketsData)) {
          client.sendEvent(responseRoom, data);
        } else {
          D specificData;
          specificData = (D) ((FirstMarketsData) data).getCopyWithMarketLimit(getChunksToReturn());
          client.sendEvent(responseRoom, specificData);
          if (liveServUpdates) {
            Set<String> channels = extractLiveServChannels(specificData);
            channels.removeAll(channelsForClosure);
            if (!channels.isEmpty()) {
              channels.forEach(this::sendLastMessageToClient);
              addToRoom(client, channels);
              channelsForClosure.addAll(channels);
            }
          }
        }
      }

      private void sendLastMessageToClient(String channel) {
        Envelope lastMessage = liveServConnector.subscribe(channel);
        if (lastMessage != null) {
          MessageEnvelope mEnvelope = (MessageEnvelope) lastMessage;
          BaseObject baseObject = converter.convert(mEnvelope);
          client.sendEvent(mEnvelope.getChannel(), baseObject);
        }
      }
    };
  }

  public void start() {
    configureNamespace(
        sioServer.getNamespace(""),
        Long.class,
        firstmarketsTracker,
        virtualMarketsTracker,
        sportsTracker);
    liveServConnector.addMessageHandler(
        envelope -> {
          com.coral.oxygen.middleware.ms.liveserv.model.messages.EnvelopeType type =
              envelope.getType();
          if (type == EnvelopeType.MESSAGE) {
            MessageEnvelope mEnvelope = (MessageEnvelope) envelope;
            BaseObject baseObject = converter.convert(mEnvelope);
            sioServer
                .getRoomOperations(envelope.getChannel())
                .sendEvent(mEnvelope.getChannel(), baseObject);
          } else if (type == EnvelopeType.UNSUBSCRIBE
              && envelope.getChannel().startsWith(ChannelType.sSELCN.getName())) {
            converter.removeSelectionToMarketIdMapping(
                new BigInteger(
                    envelope.getChannel().substring(ChannelType.sSELCN.getName().length())));
          }
        });
    sioServer.start();
  }

  public void stop() {
    sioServer.stop();
  }
}
