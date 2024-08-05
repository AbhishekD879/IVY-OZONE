package com.coral.oxygen.middleware.ms.liveserv.client.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Message {
  private String messageCode;
  private String jsonData;
}
