package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSportSegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.Instant;
import javax.validation.constraints.Future;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.Pattern;
import lombok.AccessLevel;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.Setter;
import org.hibernate.validator.constraints.URL;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "sportquicklinks")
@Data
@EqualsAndHashCode(callSuper = true)
@DateRange(startDateField = "validityPeriodStart", endDateField = "validityPeriodEnd")
public class SportQuickLink extends AbstractSportSegmentEntity implements SvgAbstractMenu {

  @NotEmpty
  @Pattern(regexp = "^[^%^{}<>\\[\\]]*$", message = "should not be empty and without %^{}<>[]")
  private String title;

  @JsonIgnore
  @Setter(AccessLevel.NONE)
  @Getter(AccessLevel.NONE)
  private String titleOverwritten; // remove this field after data migration to 'title'

  @URL private String destination;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private String svg;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private SvgFilename svgFilename;

  private String svgId;

  @Future(message = " must be future date")
  private Instant validityPeriodEnd;

  private Instant validityPeriodStart;

  public String getTitle() {
    return this.titleOverwritten != null ? this.titleOverwritten : this.title;
  }
}
