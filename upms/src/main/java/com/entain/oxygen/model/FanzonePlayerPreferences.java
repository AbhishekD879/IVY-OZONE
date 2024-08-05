package com.entain.oxygen.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class FanzonePlayerPreferences {
  private String eventType;
  private String accountName;
  private String category;
  private String frontend;
  private String brand;
  private String product;
  private Preferences preferences;
  private String commLastUpdatedDate;
  private String teamLastUpdatedDate;
  private String subscriptionDate;
}
