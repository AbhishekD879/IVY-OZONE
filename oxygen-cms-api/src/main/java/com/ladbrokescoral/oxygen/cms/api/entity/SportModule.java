package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.ArrayList;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = SportModule.COLLECTION_NAME)
@Data
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(
    name = "brand_sport_type_page_title_unique",
    def = "{ 'brand': 1, 'pageId': 1, 'moduleType': 1, 'pageType': 1 , 'title': 1}",
    unique = true)
public class SportModule extends AbstractSportEntity {

  public static final String COLLECTION_NAME = "sportmodules";

  private HomeInplayConfig inplayConfig;

  @NotEmpty
  @Pattern(
      regexp = "^[^!@$%^&*(){}'<>\\[\\]]*$",
      message = "should not be empty and without !@$%^&*(){}'<>[]")
  private String title;

  @Valid private RpgConfig rpgConfig;

  /**
   * TODO: make the same approach like in SportPageModuleDataItem with @type field and remove
   * [rpgConfig, inplayConfig] fields. PS. if you don't know, ask me how.
   */
  private AemBannersConfig moduleConfig;

  @Valid private RacingModuleConfig racingConfig;

  @NotNull private SportModuleType moduleType;

  @NotNull private List<String> publishedDevices = new ArrayList<>();

  private String archivalId;

  @Valid private TeamAndFansBetsConfig teamAndFansBetsConfig;

  private PopularBetConfig popularBetConfig;
}
