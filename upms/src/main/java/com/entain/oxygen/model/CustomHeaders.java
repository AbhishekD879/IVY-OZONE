package com.entain.oxygen.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@SuppressWarnings("java:S116")
public class CustomHeaders {
  private boolean IS_PRIVILEGED_MSG;
  private String SOURCE;
  private String NOTIFICATION_TYPE;
}
