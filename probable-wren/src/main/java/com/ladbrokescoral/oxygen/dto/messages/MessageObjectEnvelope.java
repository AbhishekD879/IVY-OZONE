package com.ladbrokescoral.oxygen.dto.messages;

import com.google.gson.Gson;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.val;
import org.springframework.util.StringUtils;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class MessageObjectEnvelope {

  private EnvelopeType type;
  private Channel channel;
  private Channel subChannel;
  private Event event;
  private Object message;

  public MessageObjectEnvelope(Envelope messageObject, Gson gson) {
    this.type = EnvelopeType.MESSAGE;
    this.message = gson.fromJson(messageObject.getMessage().getJsonData(), Object.class);
    this.event = new Event(messageObject.getEventId());
    this.channel = createChannelObject(messageObject.getChannel());

    val messageCode = messageObject.getMessage().getMessageCode();

    if (!StringUtils.isEmpty(messageCode)) {
      val subChannelName =
          messageCode.substring(messageCode.length() - 28, messageCode.length() - 12);
      this.subChannel = createChannelObject(subChannelName);
    }
  }

  private static Channel createChannelObject(String channel) {
    val name = channel;
    val id = Long.parseLong(channel.substring(6));
    val type = channel.substring(0, 6);
    return new Channel(id, name, type);
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  public static class Channel {
    private Long id;
    private String name;
    private String type;
  }

  @Data
  @NoArgsConstructor
  @AllArgsConstructor
  private static class Event {
    private Long id;
  }
}
