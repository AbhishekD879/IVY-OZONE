package com.oxygen.publisher.inplay.service.request;

import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

/** Parameters for GET_SPORT request */
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class GetSportRequestData {

  private String autoUpdates; // Yes/No
  private Integer categoryId;
  private String emptyTypes; // Yes/No
  private Boolean isLiveNowType; // Flag duplicates parameter "topLevelType"
  private String marketSelector; // can be null
  private String topLevelType;
  private boolean valid; // internal field

  public GetSportRequestData(Map<String, Object> objectMap) {
    valid = validateSportMap(objectMap);
    if (valid) {
      if (objectMap.get("autoUpdates") == null
          || YesNoFlag.YES.getValue().equals(objectMap.get("autoUpdates"))) {
        autoUpdates = YesNoFlag.YES.getValue();
      } else {
        autoUpdates = YesNoFlag.NO.getValue();
      }
      categoryId = Integer.valueOf(String.valueOf(objectMap.get("categoryId")));
      if (objectMap.get("emptyTypes") != null
          && YesNoFlag.YES.getValue().equals(objectMap.get("emptyTypes"))) {
        emptyTypes = YesNoFlag.YES.getValue();
      } else {
        emptyTypes = YesNoFlag.NO.getValue();
      }
      if (objectMap.get("isLiveNowType") == null
          || !(objectMap.get("isLiveNowType") instanceof Boolean)) {
        isLiveNowType = Boolean.FALSE;
      } else {
        isLiveNowType = Boolean.TRUE;
      }
      isLiveNowType = Boolean.valueOf(String.valueOf(objectMap.get("isLiveNowType")));
      if (objectMap.get("marketSelector") != null) {
        marketSelector = (String) objectMap.get("marketSelector");
      }
      topLevelType = (String) objectMap.get("topLevelType");
    }
  }

  private boolean validateSportMap(Map<String, Object> objectMap) {
    if (objectMap.get("categoryId") == null) {
      return false;
    }
    if (objectMap.get("topLevelType") == null
        || !(objectMap.get("topLevelType") instanceof String)) {
      return false;
    }
    return true;
  }
}
