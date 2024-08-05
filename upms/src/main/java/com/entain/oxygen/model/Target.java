package com.entain.oxygen.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Target {

  private String brand;
  private String product;
  private String channel;
  private String user;
}
