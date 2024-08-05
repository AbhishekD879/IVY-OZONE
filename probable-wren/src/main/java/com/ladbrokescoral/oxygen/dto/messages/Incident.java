package com.ladbrokescoral.oxygen.dto.messages;

import lombok.Data;

@Data
public class Incident {

  private Context context;
  private String eventId;
  private Type type;
  private String correlationId;
  private String seqId;
  private Score score;
  private String periodScore;
  private String clock;
  private String participant;
  private String period;
  private String timeStamp;
  private String receiveTimestamp;
  private String feed;
}
