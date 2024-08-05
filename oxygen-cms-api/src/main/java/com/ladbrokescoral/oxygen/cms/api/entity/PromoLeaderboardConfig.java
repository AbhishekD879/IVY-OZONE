package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "promoleaderboardconfig")
public class PromoLeaderboardConfig extends AbstractEntity implements HasBrand {
  @NotNull private String brand;
  @NotNull private String name;
  private Integer topX;
  private Boolean individualRank;
  private String filePath;
  private String genericTxt;
  private Boolean status = false;
  private List<CSVHeaderColumns> columns;
}
