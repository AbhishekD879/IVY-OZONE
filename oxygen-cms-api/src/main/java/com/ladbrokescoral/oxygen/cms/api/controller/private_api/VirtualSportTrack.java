package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.Positive;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.validation.annotation.Validated;

@Data
@Accessors(chain = true)
@Validated
@EqualsAndHashCode(callSuper = true)
@Document(collection = "virtualSportTrack")
public class VirtualSportTrack extends SortableEntity implements HasBrand {

  @NotEmpty private String brand;

  @NotEmpty private String title;

  private boolean active;

  @NotEmpty private String classId;

  private String typeIds;

  private String className;

  private String streamUrl;

  @NotEmpty private String sportId;

  @Positive private Integer numberOfEvents;

  private boolean showRunnerImages;

  private boolean showRunnerNumber;

  private List<Filename> runnerImages = Collections.emptyList();
  private Map<String, List<Filename>> eventRunnerImages = new HashMap<>();

  private Map<String, String> eventAliases = new HashMap<>();
}
