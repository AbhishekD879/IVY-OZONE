package com.coral.oxygen.middleware.common.configuration;

import java.util.Optional;
import java.util.stream.Stream;
import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;

/**
 * @author volodymyr.masliy
 */
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
public enum DistributedKey {
  ATOMIC_FEATURED_DATA("featured_data"),
  FEATURED_PAGE_MODEL_MAP("featured_model"),
  FEATURED_MODULE_MAP("featured_module"),
  FEATURED_SPORT_PAGES("featured_sport_pages"),
  LIVE_SERVER_MODULE_MAP("live_server"),
  LIVE_SERVER_SUBSCRIPTIONS_MAP("live_server_subsriptions"),
  GENERATION_MAP("generation_map"),
  LAST_RUN_TIME("last_run_time"),

  ATOMIC_INPLAY_DATA("inplay_data"),
  INPLAY_STRUCTURE_MAP("inplay_structure"),
  INPLAY_SPORT_SEGMENT_MAP("inplay_module"),
  INPLAY_SPORTS_RIBBON_MAP("inplay_sports_ribbon"),
  INPLAY_CACHED_STRUCTURE_MAP("inplay_cached_structure"),
  ERRORS_MAP("errors"),
  VIRTUAL_SPORTS_STRUCTURE_MAP("virtual_sports_structure_map");

  private final String mapName;

  public static Optional<DistributedKey> fromString(String name) {
    return Stream.of(DistributedKey.values()).filter(e -> e.mapName.equals(name)).findFirst();
  }
}
