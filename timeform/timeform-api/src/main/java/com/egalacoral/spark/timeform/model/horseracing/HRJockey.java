package com.egalacoral.spark.timeform.model.horseracing;

import com.egalacoral.spark.timeform.model.Identity;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;

/** Created by llegkyy on 07.09.16. */
public class HRJockey extends Identity implements Serializable {

  private static final long serialVersionUID = -8497514472693245397L;

  @SerializedName(value = "jockeyCode")
  private String jockeyCode;

  @SerializedName(value = "fullName")
  private String fullName;

  /**
   * Gets the value of the jockeyCode property. EntityColumn: jockeyCode | Standard Summary: The
   * code of the jockey and is the primary key Remark: The primary key (PK)
   *
   * @return a String(12) not Null
   */
  public String getJockeyCode() {
    return jockeyCode;
  }

  /**
   * Gets the value of the fullName property. EntityColumn: fullName | Standard Summary: Full
   * version of the jockey name. Remark: e.g. Frankie Dettori
   *
   * @return a String not Null
   */
  public String getFullName() {
    return fullName;
  }

  public void setJockeyCode(String jockeyCode) {
    this.jockeyCode = jockeyCode;
  }

  public void setFullName(String fullName) {
    this.fullName = fullName;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HRJockey{");
    sb.append("jockeyCode='").append(jockeyCode).append('\'');
    sb.append(", fullName='").append(fullName).append('\'');
    sb.append('}');
    return sb.toString();
  }
}
