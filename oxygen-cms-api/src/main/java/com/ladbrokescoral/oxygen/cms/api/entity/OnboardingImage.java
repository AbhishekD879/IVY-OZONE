package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import lombok.Data;
import org.bson.types.ObjectId;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document
public class OnboardingImage {

  @Size(max = 50, message = "ImageLabel should be max of 50 chars")
  private String imageLabel;

  @Size(max = 50, message = "nextCTAButtonLabel should be max of 50 chars")
  private String nextCTAButtonLabel;

  private Filename onboardImageDetails;
  @NotNull private String imageType;

  private ObjectId id;

  public OnboardingImage() {
    this.id = ObjectId.get();
  }
}
