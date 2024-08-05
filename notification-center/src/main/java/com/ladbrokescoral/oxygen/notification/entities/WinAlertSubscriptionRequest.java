package com.ladbrokescoral.oxygen.notification.entities;

import java.util.List;
import java.util.Map;
import javax.validation.constraints.Max;
import javax.validation.constraints.NotNull;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@Builder
@ToString(callSuper = true)
@AllArgsConstructor
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
@XmlAccessorType(XmlAccessType.FIELD)
public class WinAlertSubscriptionRequest extends BaseSubscription {

  @NotNull(message = "notification.exception.message.bet_id")
  @XmlElement
  private List<String> betIds;

  @Max(256)
  @XmlElement
  private String userName;

  private Integer appVersionInt;

  @XmlElement private Map<String, Object> additionalProperties;
}
