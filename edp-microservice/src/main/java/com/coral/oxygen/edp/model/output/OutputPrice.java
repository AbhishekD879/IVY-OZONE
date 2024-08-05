package com.coral.oxygen.edp.model.output;

import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class OutputPrice {

  protected String id;
  protected String priceType;
  protected Integer priceNum;
  protected Integer priceDen;
  protected Double priceDec;
  protected String handicapValueDec;
  protected Double rawHandicapValue;
  protected String priceStreamType;

  public String getId() {
    return id;
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

  public void setId(String id) {
    this.id = id;
  }

  public void setPriceType(String priceType) {
    this.priceType = priceType;
  }

  public void setPriceNum(Integer priceNum) {
    this.priceNum = priceNum;
  }

  public void setPriceDen(Integer priceDen) {
    this.priceDen = priceDen;
  }

  public void setPriceDec(Double priceDec) {
    this.priceDec = priceDec;
  }

  public void setHandicapValueDec(String handicapValueDec) {
    this.handicapValueDec = handicapValueDec;
  }

  public void setRawHandicapValue(Double rawHandicapValue) {
    this.rawHandicapValue = rawHandicapValue;
  }

  public String getPriceStreamType() {
    return priceStreamType;
  }

  public void setPriceStreamType(String priceStreamType) {
    this.priceStreamType = priceStreamType;
  }

  @Override
  public String toString() {
    return super.toString()
        + ", id='"
        + id
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
        + ", priceStreamType='"
        + priceStreamType
        + '\''
        + "} ";
  }
}
