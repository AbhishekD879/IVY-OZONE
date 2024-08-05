package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.util.List;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = false)
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "bet-sharing")
public class BetSharingEntity extends BetSharingUrls implements HasBrand {
  @NotNull private String brand;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String lostBetsShareCardMessage;

  @NotNull private List<ShareCardDetails> lostBetControl;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String openBetShareCardMessage;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String openBetShareCardSecondMessage;

  private Boolean openBetShareCardStatus;
  @NotNull private List<ShareCardDetails> openBetControl;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String wonBetShareCardMessage;

  private Boolean wonBetShareCardStatus;
  @NotNull private List<ShareCardDetails> wonBetControl;

  @Size(max = 30, message = "message should be max of 30 chars")
  @NotNull
  private String cashedOutBetsShareCardMessage;

  @NotNull private List<ShareCardDetails> cashedOutBetControl;

  private FTPBetSharing ftpBetSharingConfigs;

  private LuckyDipBetSharing luckyDipBetSharingConfigs;
}
