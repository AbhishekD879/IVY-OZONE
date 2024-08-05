package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.List;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "mybets")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class MyBet extends AbstractEntity implements HasBrand {
  @NotBlank private String brand;
  private String type;
  private String noBetText;
  private String addDescText;
  private String defaultImgLink;
  private List<BrandedImage> brandedImageList;
}
