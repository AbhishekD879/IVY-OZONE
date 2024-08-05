package com.ladbrokescoral.oxygen.betpackmp.model;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Builder(toBuilder = true)
public class PafExtractorPromotion {

  private Metadata metadata;

  private Promotion payload;
}
