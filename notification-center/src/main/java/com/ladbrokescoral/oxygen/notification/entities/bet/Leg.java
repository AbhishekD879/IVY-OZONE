package com.ladbrokescoral.oxygen.notification.entities.bet;

import com.google.gson.annotations.SerializedName;
import java.util.List;
import lombok.Data;

@Data
public class Leg {
  @SerializedName("part")
  private List<Part> parts;

  private String legNo;
  private String legSort;
}
