package com.ladbrokescoral.oxygen.notification.entities;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import javax.validation.constraints.NotNull;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

@Data
@Setter
@EqualsAndHashCode(callSuper = true)
@AllArgsConstructor
@NoArgsConstructor
@ToString
@XmlAccessorType(XmlAccessType.FIELD)
public class Items extends BaseSubscription {
  @NotNull(message = "notification.exception.message.event_id")
  private Long eventId;

  @JsonProperty("isEnable")
  private Boolean isEnable;

  /** Empty list to unsubscribe */
  @XmlElement private List<String> types;

  @XmlElement private List<String> listOfChannelId;
  @XmlElement private String sportUri;
  @XmlElement private Integer appVersionInt;

  @Builder
  public Items(
      String token,
      String platform,
      long hoursToExpire,
      Long eventId,
      List<String> types,
      List<String> listOfChannelId,
      String sportUri,
      Integer appVersionInt,
      Boolean isEnable) {
    super(token, platform, hoursToExpire);
    this.eventId = eventId;
    this.types = types;
    this.listOfChannelId = listOfChannelId;
    this.sportUri = sportUri;
    this.appVersionInt = appVersionInt;
    this.isEnable = isEnable;
  }
}
