package com.egalacoral.spark.timeform.model.horseracing;

import com.egalacoral.spark.timeform.model.Identity;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;

/**
 * Object representation of the horse's country.
 *
 * @author Vitalij Havryk
 */
public class HRCountry extends Identity implements Serializable {
  private static final long serialVersionUID = 248568415436523563L;

  @SerializedName(value = "countryCode")
  private String countryCode;

  @SerializedName(value = "currencyCode")
  private String currencyCode;

  @SerializedName(value = "countryName")
  private String countryName;

  @SerializedName(value = "countryChar")
  private String countryChar;

  /**
   * The unique identifier for the country
   *
   * @note The primary key for the country table
   * @return String(3) UPPER CASE
   */
  public String getCountryCode() {
    return countryCode;
  }

  /**
   * The currency code of the given country
   *
   * @note An example: GBP - Great British Pound
   * @return String(3) UPPER CASE
   */
  public String getCurrencyCode() {
    return currencyCode;
  }

  /**
   * The full name of the country
   *
   * @note An example: GBR - Great Britain
   * @return String Title Case
   */
  public String getCountryName() {
    return countryName;
  }

  /**
   * A single character identifier for the country
   *
   * @note An example: K - Great Britain, no always populated
   * @return String(1)
   */
  public String getCountryChar() {
    return countryChar;
  }

  public void setCountryCode(String countryCode) {
    this.countryCode = countryCode;
  }

  public void setCurrencyCode(String currencyCode) {
    this.currencyCode = currencyCode;
  }

  public void setCountryName(String countryName) {
    this.countryName = countryName;
  }

  public void setCountryChar(String countryChar) {
    this.countryChar = countryChar;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HRCountry{");
    sb.append("countryCode='").append(countryCode).append('\'');
    sb.append(", currencyCode='").append(currencyCode).append('\'');
    sb.append(", countryName='").append(countryName).append('\'');
    sb.append(", countryChar='").append(countryChar).append('\'');
    sb.append('}');
    return sb.toString();
  }
}
