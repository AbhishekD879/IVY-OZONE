package com.coral.oxygen.middleware.ms.quickbet.connector;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import java.util.Collections;
import lombok.ToString;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.commons.lang3.builder.ToStringBuilder;
import org.apache.commons.lang3.builder.ToStringStyle;

@ToString
public class BanachSelection {
  private final BanachSelectionRequestData requestData;
  private final String selectioHash;

  public BanachSelection(BanachSelectionRequestData banachSelectionRequestData) {
    this.requestData = banachSelectionRequestData;
    this.selectioHash = calculateHash();
  }

  private String calculateHash() {
    Collections.sort(requestData.getSelectionIds());
    Collections.sort(requestData.getPlayerSelections());

    String stringRepresentation =
        ToStringBuilder.reflectionToString(requestData, ToStringStyle.NO_CLASS_NAME_STYLE);
    return DigestUtils.sha1Hex(stringRepresentation);
  }

  public String selectionHash() {
    return this.selectioHash;
  }

  public BanachSelectionRequestData requestData() {
    return this.requestData;
  }
}
