package com.ladbrokescoral.oxygen.cms.api.service.sporttab;

public enum SportTabNames {
  MATCHES,
  LIVE,
  COMPETITIONS,
  COUPONS,
  OUTRIGHTS,
  JACKPOT,
  SPECIALS,
  GOLF_MATCHES,
  TODAY,
  TOMORROW,
  MEETINGS,
  POPULARBETS;

  public String nameLowerCase() {
    return name().toLowerCase();
  }
}
