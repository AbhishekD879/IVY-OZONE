package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "quiz-popup-setting")
@Accessors(chain = true)
public class QuizPopupSetting extends AbstractEntity implements HasBrand {
  @Brand private String brand;
  private boolean enabled;
  @NotBlank private String pageUrls;

  private String popupText;
  private String popupTitle;
  @NotBlank private String quizId;
  private String yesText;
  private String remindLaterText;
  private String dontShowAgainText;
  @JsonIgnore private String sourceId;

  @JsonIgnore
  @JsonProperty(access = JsonProperty.Access.READ_ONLY)
  private Instant expirationDate;
}
