package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.CSVHeaderColumns;
import java.util.List;
import lombok.Data;

@Data
public class PromoLeaderboardConfigPublicDto {
  private String id;
  private String name;
  private Integer topX;
  private Boolean individualRank;
  private String genericTxt;
  private Boolean status;
  private List<CSVHeaderColumns> columns;
}
