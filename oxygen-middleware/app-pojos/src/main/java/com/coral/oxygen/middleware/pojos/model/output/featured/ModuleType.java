package com.coral.oxygen.middleware.pojos.model.output.featured;

public enum ModuleType {
  QUICK_LINK(true),
  HIGHLIGHTS_CAROUSEL,
  SELECTION,
  RACE_ID,
  FEATURED,
  UNGROUPED_FEATURED,
  INPLAY,
  SUPPER_BUTTON(true),
  SURFACE_BET,
  RECENTLY_PLAYED_GAMES,
  AEM_BANNERS(true),
  RACING_MODULE,
  RACING_EVENT_MODULE,
  RACING_TOTE_MODULE,
  BETS_BASED_ON_YOUR_TEAM,
  BETS_BASED_ON_OTHER_FANS,

  // virtual sport next events module to show all events information.
  VIRTUAL_NEXT_EVENTS,

  POPULAR_BETS,

  BYB_WIDGET,
  SUPER_BUTTON,
  LUCKY_DIP,
  POPULAR_ACCA;

  private boolean isStatic;

  ModuleType(boolean isStatic) {
    this.isStatic = isStatic;
  }

  ModuleType() {
    this.isStatic = false;
  }

  public boolean isStatic() {
    return isStatic;
  }
}
