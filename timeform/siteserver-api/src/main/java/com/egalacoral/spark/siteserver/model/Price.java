package com.egalacoral.spark.siteserver.model;

/** Created by oleg.perushko@symphony-solutions.eu on 8/2/16 */
public class Price extends Identity {
  protected String id;
  protected Boolean isActive;
  protected Integer displayOrder;
  protected String outcomeVariantId;
  protected String priceType;
  protected Integer priceNum;
  protected Integer priceDen;
  protected Double priceDec;
  protected String handicapValueDec;
  protected Double rawHandicapValue;
  protected String poolId;
  protected String poolType;
  protected Boolean isToPlace;

  public String getId() {
    return id;
  }

  public Boolean isActive() {
    return isActive;
  }

  public Integer getDisplayOrder() {
    return displayOrder;
  }

  public String getOutcomeVariantId() {
    return outcomeVariantId;
  }

  public String getPriceType() {
    return priceType;
  }

  public Integer getPriceNum() {
    return priceNum;
  }

  public Integer getPriceDen() {
    return priceDen;
  }

  public Double getPriceDec() {
    return priceDec;
  }

  public String getHandicapValueDec() {
    return handicapValueDec;
  }

  public Double getRawHandicapValue() {
    return rawHandicapValue;
  }

  public String getPoolId() {
    return poolId;
  }

  public String getPoolType() {
    return poolType;
  }

  public Boolean isToPlace() {
    return isToPlace;
  }

  @Override
  public String toString() {
    return super.toString()
        + ", id='"
        + id
        + '\''
        + ", isActive="
        + isActive
        + ", displayOrder="
        + displayOrder
        + ", outcomeVariantId='"
        + outcomeVariantId
        + '\''
        + ", priceType='"
        + priceType
        + '\''
        + ", priceNum="
        + priceNum
        + ", priceDen="
        + priceDen
        + ", priceDec="
        + priceDec
        + ", handicapValueDec='"
        + handicapValueDec
        + '\''
        + ", rawHandicapValue="
        + rawHandicapValue
        + ", poolId='"
        + poolId
        + '\''
        + ", poolType='"
        + poolType
        + '\''
        + ", isToPlace="
        + isToPlace
        + "} ";
  }
}
