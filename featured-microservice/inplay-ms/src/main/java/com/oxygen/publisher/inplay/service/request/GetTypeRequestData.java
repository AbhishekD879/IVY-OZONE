package com.oxygen.publisher.inplay.service.request;

import com.newrelic.api.agent.NewRelic;
import java.util.Map;
import lombok.Getter;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;

/** Parameters for GET_TYPE request */
@Getter
@Setter
@Slf4j
public class GetTypeRequestData extends GetSportRequestData {

  private Integer typeId;

  public GetTypeRequestData(Map<String, Object> objectMap) {
    super(objectMap);
    setValid(validateTypeMap(objectMap));
    if (isValid()) {
      try {
        typeId =
            objectMap.get("typeId") instanceof Integer
                ? (Integer) objectMap.get("typeId")
                : Integer.parseInt(String.valueOf(objectMap.get("typeId")));
      } catch (NumberFormatException e) {
        NewRelic.noticeError(e);
        log.error("Cannot convert typeId \"{}\" to Integer.", objectMap.get("typeId"));
        setValid(false);
      }
    }
  }

  protected boolean validateTypeMap(Map<String, Object> objectMap) {
    if (!isValid() || objectMap.get("typeId") == null) {
      return false;
    }
    return true;
  }
}
