package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.ladbrokescoral.oxygen.cms.api.entity.Patterns;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@EqualsAndHashCode
@NoArgsConstructor
@AllArgsConstructor
@ToString(callSuper = true)
public class PromotionSectionDto {

  @NotBlank private String brand;

  @Pattern(regexp = Patterns.COMMA_SEPARTED_WORDS, message = "must be valid comma separated ids")
  private String promotionIds;

  private List<String> unassignedPromotionIds;
  @NotBlank private String name;
  private Boolean disabled = false;
  private Double sortOrder;
  private String id;
  private String createdBy;
  private String createdByUserName;
  private String updatedBy;
  private String updatedByUserName;

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant createdAt;

  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant updatedAt;
}
