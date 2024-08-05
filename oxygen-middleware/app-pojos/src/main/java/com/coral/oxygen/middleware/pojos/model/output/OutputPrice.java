package com.coral.oxygen.middleware.pojos.model.output;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import com.coral.oxygen.middleware.pojos.model.IdHolder;
import java.io.Serializable;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode
public class OutputPrice implements IdHolder, Serializable {

  protected String id;
  protected String priceType;
  protected Integer priceNum;
  protected Integer priceDen;
  protected Double priceDec;
  protected String handicapValueDec;
  protected Double rawHandicapValue;
  protected String priceStreamType;
  protected Integer priceAmerican;

  @ChangeDetect
  public String getId() {
    return id;
  }

  @ChangeDetect
  public String getPriceType() {
    return priceType;
  }

  @ChangeDetect
  public Integer getPriceNum() {
    return priceNum;
  }

  @ChangeDetect
  public Integer getPriceDen() {
    return priceDen;
  }

  @ChangeDetect
  public Double getPriceDec() {
    return priceDec;
  }

  @ChangeDetect
  public String getHandicapValueDec() {
    return handicapValueDec;
  }

  @ChangeDetect
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

  public Integer getPriceAmerican() {
    return priceAmerican;
  }

  public void setPriceAmerican(Integer priceAmerican) {
    this.priceAmerican = priceAmerican;
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
        + ", priceAmerican="
        + priceAmerican
        + "} ";
  }

  @Override
  public String idForChangeDetection() {
    return String.valueOf(id);
  }
}
