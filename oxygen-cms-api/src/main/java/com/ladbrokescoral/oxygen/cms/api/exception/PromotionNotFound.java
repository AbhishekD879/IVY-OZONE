package com.ladbrokescoral.oxygen.cms.api.exception;

public class PromotionNotFound extends RuntimeException {
  private final String promotionId;

  public PromotionNotFound(String promotionId) {
    super();
    this.promotionId = promotionId;
  }

  public String getPromotionId() {
    return promotionId;
  }
}
