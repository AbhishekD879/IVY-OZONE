package com.ladbrokescoral.oxygen.cms.api.entity;

import static com.ladbrokescoral.oxygen.cms.api.entity.Patterns.VIP_LEVELS_INPUT_PATTERN;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.bson.types.ObjectId;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "offers")
@Data
@EqualsAndHashCode(callSuper = true)
public class Offer extends SortableEntity implements HasBrand {
  @Pattern(
      regexp = VIP_LEVELS_INPUT_PATTERN,
      message =
          "Only hyphened and comma separated numbers are allowed. E.g: 1 or 1-3 or 12,3,5-1,4,7-10 or 1,2 ...")
  private String vipLevelsInput;

  private ObjectId module;
  @Transient private String moduleName;
  @NotBlank private String targetUri;
  @NotNull private Instant displayTo;
  @NotNull private Instant displayFrom;
  @NotBlank private String name;
  private List<Integer> vipLevels;
  @NotBlank private String brand;
  private Boolean disabled;
  private String showOfferTo;
  private String showOfferOn;
  private Filename image;
  private String imageUri;
  private String directImageUrl;
  private Boolean useDirectImageUrl;
}
