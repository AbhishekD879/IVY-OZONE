package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.List;
import java.util.Map;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "preferencecentre")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@EqualsAndHashCode(callSuper = true)
public class PreferenceCentre extends FanzonePage {
  private String pcDescription;
  private List<Map<String, String>> pcKeys;
  private String ctaText;
  private String subscribeText;
  private String confirmText;
  private String confirmCTA;
  private String exitCTA;
  private String updatedByUserName;
  private String createdByUserName;
  private String notificationDescriptionDesktop;
  private String unsubscribeDescription;
  private String notificationPopupTitle;
  private String unsubscribeTitle;
  private String optInCTA;
  private String noThanksCTA;
  private String pushPreferenceCentreTitle;
  private Boolean active;
  private String genericTeamNotificationDescription;
  private String genericTeamNotificationTitle;
}
