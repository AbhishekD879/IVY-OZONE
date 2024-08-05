package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.List;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "countries")
@Data
@EqualsAndHashCode(callSuper = true)
public class Country extends AbstractEntity implements HasBrand {

  @Valid @NotEmpty private List<CountryData> countriesData;
  @NotBlank private String brand;
}
