package com.entain.oxygen.model;

import com.entain.oxygen.entity.HorseInfo;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.io.Serializable;
import java.util.LinkedHashSet;
import java.util.Set;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
@SuppressWarnings("java:S1948")
public class UserStableDto implements Serializable {

  private String brand;
  private LinkedHashSet<HorseInfo> myStable;
  private Set<String> unbookmarkedHorses;
}
