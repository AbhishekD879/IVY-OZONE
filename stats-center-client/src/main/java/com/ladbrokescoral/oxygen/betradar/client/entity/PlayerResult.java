package com.ladbrokescoral.oxygen.betradar.client.entity;

import java.util.List;
import lombok.Data;

@Data
public class PlayerResult {
  private String id; // 4694
  private String name; // Russia
  private String brId; // 9544
  private String gender; // M
  private Country country;
  private Promotion promotion;
  private List<Entry> values;
}
