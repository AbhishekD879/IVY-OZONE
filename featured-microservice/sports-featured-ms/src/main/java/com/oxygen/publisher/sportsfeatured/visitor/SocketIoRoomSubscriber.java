package com.oxygen.publisher.sportsfeatured.visitor;

import static com.oxygen.publisher.sportsfeatured.util.SportsHelper.HASH;

import com.corundumstudio.socketio.SocketIOClient;
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.EventsModuleData;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SocketIoRoomSubscriber implements FeaturedModuleVisitor {

  private final SocketIOClient client;
  private final SportsSessionContext sportsSessionContext;

  public SocketIoRoomSubscriber(SocketIOClient client, SportsSessionContext sportsSessionContext) {
    this.client = client;
    this.sportsSessionContext = sportsSessionContext;
  }

  @Override
  public void visit(QuickLinkModule module) {
    String quickModuleId = module.getSportId() + HASH + module.getId();
    joinModuleIdRoom(quickModuleId);
  }

  @Override
  public void visit(QuickLinkModule module, String segment) {
    String quickModuleId = module.getSportId() + HASH + segment + HASH + module.getId();
    joinModuleIdRoom(quickModuleId);
  }

  @Override
  public void visit(RecentlyPlayedGameModule module) {
    String rpgModuleId = module.getSportId() + HASH + module.getId();
    joinModuleIdRoom(rpgModuleId);
  }

  /**
   * [05/06/2019] UI doesn't listen for module updates. Subscribing client to module update by
   * default can affect performance because they can be ~100kb or more each. At the moment, only iOS
   * listens to module updates, but they should send "subscribe" explicitly. Therefore, there is no
   * need for automatic subscription here and joinModuleIdRoom(module.getId()) call was removed from
   * the method;
   *
   * @param module - events module to initiate default subscription
   */
  @Override
  public void visit(EventsModule module) {
    if (Boolean.TRUE.equals(module.getShowExpanded())) {
      Set<String> eventsIds =
          module.getData().stream()
              .map(EventsModuleData::getId)
              .map(String::valueOf)
              .collect(Collectors.toSet());

      log.debug(
          "[{}] EventsModule {}: subscribing on events ids: {}",
          client.getSessionId(),
          module.getId(),
          eventsIds);

      eventsIds.forEach(this::joinEventIdRoom);
    }
  }

  @Override
  public void visit(HighlightCarouselModule module) {
    // downcast to EventModule (same behaviour as for events module)
    visit((EventsModule) module);
  }

  @Override
  public void visit(VirtualEventModule module) {
    // We don't  have event level update for virtual event module
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
  }

  @Override
  public void visit(PopularBetModule module) {
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
    visit((EventsModule) module);
  }

  @Override
  public void visit(InplayModule module) {
    if (Boolean.TRUE.equals(module.getShowExpanded())) {
      joinModuleIdRoom(module.getSportId() + HASH + module.getId());
      List<String> inplayEventIds =
          module.getData().stream()
              .flatMap(sportSegment -> sportSegment.getEventsByTypeName().stream())
              .flatMap(typeSegment -> typeSegment.getEvents().stream())
              .map(EventsModuleData::getId)
              .collect(Collectors.toList());

      log.debug(
          "[{}] InplayModule {}: subscribing on events ids: {}",
          client.getSessionId(),
          module.getId(),
          inplayEventIds);
      inplayEventIds.forEach(this::joinEventIdRoom);
    }
  }

  @Override
  public void visit(InplayModule module, String segment) {
    if (Boolean.TRUE.equals(module.getShowExpanded())) {
      joinModuleIdRoom(module.getSportId() + HASH + segment + HASH + module.getId());
      List<String> inplayEventIds =
          module.getData().stream()
              .flatMap(sportSegment -> sportSegment.getEventsByTypeName().stream())
              .flatMap(typeSegment -> typeSegment.getEvents().stream())
              .map(EventsModuleData::getId)
              .collect(Collectors.toList());

      log.debug(
          "[{}] InplayModule {}: subscribing on events ids: {}",
          client.getSessionId(),
          module.getId(),
          inplayEventIds);
      inplayEventIds.forEach(this::joinEventIdRoom);
    }
  }

  @Override
  public void visit(SurfaceBetModule module) {
    // downcast to EventModule (same behaviour as for events module)
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
    visit((EventsModule) module);
  }

  @Override
  public void visit(BybWidgetModule module) {
    // downcast to EventModule (same behaviour as for events module)
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
    visit((EventsModule) module);
  }

  @Override
  public void visit(SurfaceBetModule module, String segment) {
    // downcast to EventModule (same behaviour as for events module)
    joinModuleIdRoom(module.getSportId() + HASH + segment + HASH + module.getId());
    visit((EventsModule) module);
  }

  @Override
  public void visit(AemBannersModule module) {
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
  }

  @Override
  public void visit(RacingModule module) {
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
  }

  @Override
  public void visit(RacingEventsModule module) {
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
  }

  @Override
  public void visit(VirtualRaceModule module) {
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
  }

  @Override
  public void visit(InternationalToteRaceModule module) {
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
  }

  @Override
  public void visit(TeamBetsModule module) {
    joinModuleIdRoom(module.getId());
  }

  @Override
  public void visit(FanBetsModule module) {
    joinModuleIdRoom(module.getId());
  }

  @Override
  public void visit(TeamBetsModule module, String segment) {
    joinModuleIdRoom(module.getSportId() + HASH + segment + HASH + module.getId());
    visit(module);
  }

  @Override
  public void visit(PopularAccaModule module) {
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
    Set<String> eventsIds =
        module.getData().stream()
            .flatMap(data -> data.getPositions().stream())
            .map(position -> position.getEvent().getId())
            .collect(Collectors.toSet());

    log.debug(
        "[{}] PopularAccaModule {}: subscribing on events ids: {}",
        client.getSessionId(),
        module.getId(),
        eventsIds);

    eventsIds.forEach(this::joinEventIdRoom);
  }

  @Override
  public void visit(FanBetsModule module, String segment) {
    joinModuleIdRoom(module.getSportId() + HASH + segment + HASH + module.getId());
    visit(module);
  }

  private void joinModuleIdRoom(String id) {
    client.joinRoom(id);
  }

  private void joinEventIdRoom(String event) {
    client.joinRoom(event);
    sportsSessionContext.sendLatestLiveUpdates(client, event);
  }

  @Override
  public void visit(LuckyDipModule module) {
    joinModuleIdRoom(module.getSportId() + HASH + module.getId());
  }

  @Override
  public void visit(SuperButtonModule module) {
    {
      joinModuleIdRoom(module.getSportId() + HASH + module.getId());
    }
  }
}
