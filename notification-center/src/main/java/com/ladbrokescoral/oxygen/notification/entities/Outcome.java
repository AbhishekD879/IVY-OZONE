package com.ladbrokescoral.oxygen.notification.entities;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class Outcome {
  private String id;
  private String name;
  private String resultCode;
  private int position;
}
