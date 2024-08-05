package com.entain.oxygen.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class RtmsDto {

  private String eventId;
  private String eventType;
  private String userId;
  private String frontend;

  private String brand;
  private String product;
  private String channel;
  private long eventCreationTime;

  private Payload payload;

  private CustomHeaders customHeaders;
}
