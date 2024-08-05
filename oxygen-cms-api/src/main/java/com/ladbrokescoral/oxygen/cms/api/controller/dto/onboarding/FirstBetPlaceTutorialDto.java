package com.ladbrokescoral.oxygen.cms.api.controller.dto.onboarding;

import com.ladbrokescoral.oxygen.cms.api.entity.onboarding.CloseButton;
import java.time.Instant;
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class FirstBetPlaceTutorialDto extends OnboardingDto {

  private String moduleName;
  private String moduleDiscription;
  private Instant displayFrom;
  private Instant displayTo;
  private int months;
  @Valid @NotNull private CloseButton button;
  @Valid @NotNull private HomePageDto homePage; // step :0 00
  @Valid @NotNull private StepContentDto pickYourBet; // step :1 01
  @Valid @NotNull private StepContentDto addSelection; // step :03
  @Valid @NotNull private BetSlipDto betSlip; // step 04
  @Valid @NotNull private PlaceBetDto placeYourBet; // step 2 02
  @Valid @NotNull private MyBetsDto myBets; // step 5  //07
  @Valid @NotNull private BetDetailsDto betDetails; // step 4 //06
  @Valid @NotNull private BetPlaceDto betPlaced; // step 3 05

  @Data
  public static class HomePageDto extends StepContentDto {
    @NotBlank private String button;
  }

  @Data
  public static class PlaceBetDto {
    @Valid @NotNull private StepContentDto boost;
    @Valid @NotNull private StepContentDto defaultContent;
  }

  @Data
  public static class BetDetailsDto {
    @Valid @NotNull private StepContentDto cashOut;
    @Valid @NotNull private StepContentDto defaultContent;
  }

  @Data
  public static class MyBetsDto {
    @Valid @NotNull private StepContentDto cashOut;
    @Valid @NotNull private StepContentDto defaultContent;
    @NotBlank private String buttonDesc;
  }

  @Data
  public static class BetPlaceDto {
    @Valid @NotNull private StepContentDto winAlert;
    @Valid @NotNull private StepContentDto defaultContent;
    @NotBlank private String buttonDesc;
  }

  @Data
  public static class BetSlipDto {
    @Valid @NotNull private StepContentDto boost;
    @Valid @NotNull private StepContentDto defaultContent;
  }
}
