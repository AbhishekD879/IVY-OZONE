package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = PromotionSection.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
public class PromotionSection extends SortableEntity implements HasBrand {

  public static final String COLLECTION_NAME = "promotionSection";

  @NotBlank private String brand;

  @Pattern(regexp = Patterns.COMMA_SEPARTED_WORDS, message = "must be valid comma separated ids")
  private String promotionIds;

  @NotBlank private String name;
  private Boolean disabled = false;
  private List<String> unassignedPromotionIds;
}
