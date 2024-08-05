package com.ladbrokescoral.oxygen.notification.client.optin.model;

import lombok.Data;

/**
 * * A model class for IGameMedia event which is returned for ex. as opened live stream event.
 * eventId field is specific for IGameMedia, it can be converted to OpenBet event Id using
 * SiteServer.
 */
@Data
public class IGMEvent {
  protected String eventID;
  protected String locationCode;
  protected String locationName;
  protected String sportCode;
  protected String eventStatusCode;
  protected long eventNumber;
  protected String title;
  protected String startTime;
}
