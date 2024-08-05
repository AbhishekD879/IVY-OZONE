package com.ladbrokescoral.oxygen.dto.messages;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Envelope {
  private Long eventId;
  private EnvelopeType type;
  private String channel;
  private MessageObject message;

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class MessageObject {
    private String body;
    private String eventHash;
    private String jsonData;
    private String lastMessageID;
    private String messageCode;
    private String type;
    private String publishedDate;
  }
}
