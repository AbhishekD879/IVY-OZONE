package com.oxygen.publisher.sportsfeatured.model;

/** all possible sport module types should be here */
public enum ModuleType {
  QUICK_LINK(true),
  HIGHLIGHTS_CAROUSEL,
  SELECTION,
  RACE_ID,
  FEATURED,
  IN_PLAY,
  SURFACE_BET,
  RECENTLY_PLAYED_GAMES,
  SUPPER_BUTTON(true),
  AEM_BANNERS,
  RACING_MODULE(true),
  RACING_EVENTS_MODULE,
  VIRTUAL_RACE_CAROUSEL,
  INTERNATIONAL_TOTE_RACING,
  BETS_BASED_ON_YOUR_TEAM,
  BETS_BASED_ON_OTHER_FANS,

  // virtual sport next events module to show all events information.
  VIRTUAL_NEXT_EVENTS,

  POPULAR_BETS,
  BYB_WIDGET,
  LUCKY_DIP,
  SUPER_BUTTON,
  POPULAR_ACCA;

  private final boolean isStatic;

  ModuleType() {
    this.isStatic = false;
  }

  ModuleType(boolean isStatic) {
    this.isStatic = isStatic;
  }

  public boolean isStatic() {
    return isStatic;
  }
}
