package com.ladbrokescoral.oxygen.notification.entities;

import javax.validation.constraints.NotEmpty;
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
@Builder
@Setter
@EqualsAndHashCode
@AllArgsConstructor
@NoArgsConstructor
@ToString
@XmlAccessorType(XmlAccessType.FIELD)
public class ItemEmpty {
  @NotNull(message = "notification.exception.message.event_id")
  @XmlElement
  private Long eventId;

  @NotEmpty(message = "notification.exception.message.token")
  @XmlElement
  private String token;

  @NotEmpty(message = "notification.exception.message.platform")
  @XmlElement
  private String platform;

  @XmlElement private Integer appVersionInt;
}
