package com.coral.oxygen.middleware.common.service;

import java.util.Arrays;
import java.util.List;
import org.springframework.stereotype.Component;

/** Created by azayats on 27.12.16. */
@Component
public class OutrightsConfig {

  private final List<String> sportSortCode =
      Arrays.asList(
          "TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20"
              .split(","));
  private final List<String> outrightsSportSortCode =
      Arrays.asList(
          "TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20,MTCH"
              .split(","));
  private final List<String> outrightsSports =
      Arrays.asList(
          "MOTOR_CARS",
          "TV_SPECIALS",
          "CYCLING",
          "MOTOR_SPEEDWAY",
          "MOTOR_BIKES",
          "POLITICS",
          "GOLF",
          "MOTOR_SPORTS",
          "MOVIES");

  public List<String> getOutrightsSportSortCode() {
    return outrightsSportSortCode;
  }

  public List<String> getSportSortCode() {
    return sportSortCode;
  }

  public List<String> getOutrightsSports() {
    return outrightsSports;
  }
}
