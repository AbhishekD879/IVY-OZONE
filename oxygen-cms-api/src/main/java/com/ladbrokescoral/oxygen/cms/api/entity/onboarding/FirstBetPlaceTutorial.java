package com.ladbrokescoral.oxygen.cms.api.entity.onboarding;

import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document("first-bet-tutorial")
@EqualsAndHashCode(callSuper = true)
public class FirstBetPlaceTutorial extends OnBoarding {
  private String moduleName;
  private String moduleDiscription;
  private Instant displayFrom;
  private Instant displayTo;
  private int months;
  private CloseButton button;
  private HomePage homePage; // step :0 00
  private StepContent pickYourBet; // step :1 01
  private StepContent addSelection; // step :03
  private BetSlip betSlip; // step 04
  private PlaceBet placeYourBet; // step 2 02
  private MyBets myBets; // step 5  //07
  private BetDetails betDetails; // step 4 //06
  private BetPlace betPlaced; // step 3 05

  @Data
  public static class HomePage extends StepContent {
    private String button;
  }

  @Data
  public static class PlaceBet {
    private StepContent boost;
    private StepContent defaultContent;
  }

  @Data
  public static class BetDetails {
    private StepContent cashOut;
    private StepContent defaultContent;
  }

  @Data
  public static class MyBets {
    private StepContent cashOut;
    private StepContent defaultContent;
    private String buttonDesc;
  }

  @Data
  public static class BetSlip {
    private StepContent boost;
    private StepContent defaultContent;
  }

  @Data
  public static class BetPlace {
    private StepContent winAlert;
    private StepContent defaultContent;
    private String buttonDesc;
  }
}
