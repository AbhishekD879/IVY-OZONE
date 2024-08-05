package com.ladbrokescoral.cashout.api.client.entity.request;

import java.util.Map;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class BetUpdateRequest {

  private String pagingToken;
  private String blockSize;
  private String detailLevel;
  private String token;
  private String pagingBlockSize;
  private String group;
  private String settled;
  private String fromDate;
  private String toDate;
  private String ev_category_id;
  private String bet_type;
  private String pool_type_id;
  private String game_def;

  public BetUpdateRequest(Map<String, Object> objectMap) {
    pagingToken = (String) objectMap.get("pagingToken");
    blockSize = (String) objectMap.get("blockSize");
    detailLevel = (String) objectMap.get("detailLevel");
    token = (String) objectMap.get("token");
    pagingBlockSize = (String) objectMap.get("pagingBlockSize");
    group = (String) objectMap.get("group");
    settled = (String) objectMap.get("settled");
    fromDate = (String) objectMap.get("fromDate");
    toDate = (String) objectMap.get("toDate");
    ev_category_id = (String) objectMap.get("ev_category_id");
    bet_type = (String) objectMap.get("bet_type");
    pool_type_id = (String) objectMap.get("pool_type_id");
    game_def = (String) objectMap.get("game_def");
  }
}
