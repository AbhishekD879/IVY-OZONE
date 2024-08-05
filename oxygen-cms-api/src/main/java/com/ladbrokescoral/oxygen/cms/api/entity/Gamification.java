package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "gamification")
@Data
@EqualsAndHashCode(callSuper = true)
public class Gamification extends AbstractEntity implements HasBrand {

  @Brand private String brand;

  @NotBlank private String seasonId;

  @Valid @NotNull private List<SeasonTeam> teams;

  @Valid @NotNull private List<BadgeType> badgeTypes;
}
