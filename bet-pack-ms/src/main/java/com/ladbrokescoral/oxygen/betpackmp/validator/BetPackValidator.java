package com.ladbrokescoral.oxygen.betpackmp.validator;

import com.ladbrokescoral.oxygen.betpackmp.model.PafExtractorPromotion;
import java.util.List;

public class BetPackValidator {

  private BetPackValidator() {
    throw new IllegalStateException("BetPackValidator class");
  }

  public static boolean validateActiveBetPack(
      PafExtractorPromotion pafExtractorPromotion, List<String> activeBetPacks, String dfBrand) {
    return (dfBrand.equals(pafExtractorPromotion.getPayload().getBrand())
        && pafExtractorPromotion.getPayload().getStatus().equals("Issued")
        && activeBetPacks.contains(pafExtractorPromotion.getPayload().getCampaignRef()));
  }
}
