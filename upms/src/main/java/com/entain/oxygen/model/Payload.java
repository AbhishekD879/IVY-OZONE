package com.entain.oxygen.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@SuppressWarnings("java:S116")
public class Payload {

  private String userName;
  private Preferences PreferencesObject;
}
