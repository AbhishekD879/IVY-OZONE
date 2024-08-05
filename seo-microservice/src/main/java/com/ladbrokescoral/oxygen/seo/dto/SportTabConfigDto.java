package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import java.util.ArrayList;
import java.util.List;
import lombok.*;

@Getter
@Setter
@Builder
@AllArgsConstructor
@EqualsAndHashCode
@JsonInclude(Include.NON_EMPTY)
public class SportTabConfigDto {

  private String id;
  private String name;
  private String label;
  private String url;
  private boolean hidden;
  private Double sortOrder;
  private List<SportTabConfigDto> subTabs;

  public void addSubTab(SportTabConfigDto tab) {
    if (subTabs == null) {
      subTabs = new ArrayList<>();
    }
    subTabs.add(tab);
  }
}
