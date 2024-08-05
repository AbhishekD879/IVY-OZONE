package com.coral.oxygen.middleware.pojos.model.cache;

import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;

@Getter
@Builder
@EqualsAndHashCode
public class UploadItem {

  public enum Action {
    UPLOAD
  }

  private String brand;
  private String path;
  private String fileName;
  private String json;
  private Action action;
  private String cacheTag;

  public String getKeyName() {
    return cacheTag != null
        ? String.join("-", action.name(), brand, path, fileName, cacheTag)
        : String.join("-", action.name(), brand, path, fileName);
  }
}
