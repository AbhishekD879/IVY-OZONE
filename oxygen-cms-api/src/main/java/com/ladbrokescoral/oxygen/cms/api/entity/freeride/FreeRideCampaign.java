package com.ladbrokescoral.oxygen.cms.api.entity.freeride;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "freeridecampaign")
public class FreeRideCampaign extends AbstractEntity implements HasBrand {

  @NotBlank private String name;
  @NotBlank private String brand;

  @NotNull private Instant displayFrom;
  @NotNull private Instant displayTo;

  @NotBlank private String openBetCampaignId;
  @NotBlank private String optimoveId;

  private String updatedByUserName;
  private String createdByUserName;

  private Boolean isPotsCreated = false;

  private Questionnarie questionnarie;
  private EventClassInfo eventClassInfo;
}
