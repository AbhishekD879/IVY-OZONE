package com.egalacoral.spark.liveserver;

import com.egalacoral.spark.liveserver.utils.StringUtils;
import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.io.Serializable;
import java.util.Date;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class Message implements Serializable {

  private static final long serialVersionUID = 805410867947402045L;

  private static final int EVENT_ID_END_INDEX = 17;

  private static final int EVENT_ID_START_INDEX = 7;

  @JsonProperty private String body;
  @JsonProperty private String eventHash;
  @JsonProperty private String jsonData;
  @JsonProperty private String lastMessageID;
  @JsonProperty private String messageCode;
  @JsonProperty private String type;

  @JsonProperty
  @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss.SSS")
  private Date publishedDate;

  public Message() {}

  public Message(
      String messageCode, String lastMessageID, String jsonData, String eventHash, String body) {
    this.messageCode = messageCode;
    this.jsonData = jsonData;
    this.lastMessageID = lastMessageID;
    this.eventHash = eventHash;
    this.body = body;
    this.type = getType();
    this.publishedDate = new Date();
  }

  public String getBody() {
    return body;
  }

  public String getEvenId() {
    String evenID = messageCode.substring(EVENT_ID_START_INDEX, EVENT_ID_END_INDEX);
    log.debug("event id {}", evenID);
    evenID = StringUtils.normalizeNumber(evenID);
    return evenID;
  }

  public String getType() {
    return messageCode.substring(1, 7);
  }

  public String getEventHash() {
    return eventHash;
  }

  public String getJsonData() {
    return jsonData;
  }

  public String getLastMessageID() {
    return lastMessageID;
  }

  public String getMessageCode() {
    return messageCode;
  }

  public Date getPublishedDate() {
    return publishedDate;
  }

  /** For tests only. */
  protected void setPublishedDate(Date publishedDate) {
    this.publishedDate = publishedDate;
  }

  /** For test only. */
  protected void setJsonData(String jsonData) {
    this.jsonData = jsonData;
  }

  /** For test only. */
  protected void setBody(String body) {
    this.body = body;
  }

  @Override
  public String toString() {
    return "Message{"
        + "body='"
        + body
        + '\''
        + ", eventHash='"
        + eventHash
        + '\''
        + ", messageCode='"
        + messageCode
        + '\''
        + ", jsonData='"
        + jsonData
        + '\''
        + ", lastMessageID='"
        + lastMessageID
        + '\''
        + ", type='"
        + type
        + '\''
        + '}';
  }
}
