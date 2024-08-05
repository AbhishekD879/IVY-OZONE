package com.egalacoral.spark.timeform.model.greyhound;

import com.egalacoral.spark.timeform.model.Identity;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.List;

/** Created by Igor.Domshchikov on 8/4/2016. */
public class Greyhound extends Identity implements Serializable {

  private static final long serialVersionUID = -2052614472693272771L;

  @SerializedName(value = "greyhound_id")
  private Integer greyhoundId;

  @SerializedName(value = "pa_greyhound_id")
  private Integer paGreyHoundId;

  @SerializedName(value = "greyhound_full_name")
  private String greyhoundFullName;

  @SerializedName(value = "trainer_full_name")
  private String trainerFullName;

  @SerializedName(value = "owner_full_name")
  private String ownerFullName;

  @SerializedName(value = "dam_full_name")
  private String damFullName;

  @SerializedName(value = "sire_full_name")
  private String sireFullName;

  private String colour;

  @SerializedName(value = "birth_date")
  private String birthDate;

  private String gender;

  @SerializedName(value = "seed_name")
  private String seedName;

  @SerializedName(value = "country_full_name")
  private String countryFullName;

  @SerializedName(value = "season_status")
  private String seasonStatus;

  @SerializedName(value = "form")
  private String form;

  private List<Performance> performances;

  public Greyhound() {
    // default constructor
  }

  /**
   * Gets the value of the greyhoundId property. EntityColumn: greyhound_id | Standard Summary: the
   * unique identifier for the greyhound Remark: the Primary Key for the greyhound (PK)
   *
   * @return an Integer value above 0
   */
  public Integer getGreyhoundId() {
    return greyhoundId;
  }

  /**
   * Gets the value of the paGreyHoundId property. EntityColumn: pa_greyhound_id | Standard Summary:
   * the PA unique identifier for the greyhound Remark: the PA Primary Key for the greyhound (FK)
   *
   * @return an Integer value above 0
   */
  public Integer getPaGreyHoundId() {
    return paGreyHoundId;
  }

  /**
   * Gets the value of the greyHoundFullName property. EntityColumn: greyhound_full_name | Standard
   * (PA) Summary: the full name of the greyhound Remark: an example: Mileheight alba
   *
   * @return a String with Title Case value
   */
  public String getGreyhoundFullName() {
    return greyhoundFullName;
  }

  /**
   * Gets the value of the trainerFullName property. EntityColumn: trainer_full_name | Standard (PA)
   * Summary: the full name of the greyhound's trainer (and the track they are attached to) for this
   * race Remark: an example: D Walsh (Hove). Trainer will be 'Unknown Trainer' in the event of us
   * not knowing it. Trainer will just be the name in the event of trainer or attached track
   * information being unavailable
   *
   * @return a String with Title Case value
   */
  public String getTrainerFullName() {
    return trainerFullName;
  }

  /**
   * Gets the value of the ownerFullName property. EntityColumn: owner_full_name | Standard (PA)
   * Summary: the full name of the greyhound's owner for this race Remark: an example: Courtcraft
   * Limited. Owner will be 'Unknown Owner' in the event of that information being unavailable
   *
   * @return a String with Title Case value
   */
  public String getOwnerFullName() {
    return ownerFullName;
  }

  /**
   * Gets the value of the damFullName property. EntityColumn: dam_full_name | Standard (PA)
   * Summary: the full name of the greyhound's dam Remark: an example: Giddyup Girl. Dam will be
   * 'Unknown Pedigree' in the event of the information being unavailable
   *
   * @return a String with Title Case value
   */
  public String getDamFullName() {
    return damFullName;
  }

  /**
   * Gets the value of the sireFullName property. EntityColumn: sire_full_name | Standard (PA)
   * Summary: the full name of the greyhound's sire Remark: an example: Ballymac Maeve. Sire will be
   * 'Unknown Pedigree' in the event of the information being unavailable
   *
   * @return a String with Title Case value
   */
  public String getSireFullName() {
    return sireFullName;
  }

  /**
   * Gets the value of the colour property. EntityColumn: colour | Standard (PA) Summary: the colour
   * of the greyhound Remark: an example: bk indicates black fur, etc
   *
   * @return a String with Lowercase value
   */
  public String getColour() {
    return colour;
  }

  /**
   * Gets the value of the birthDate property. EntityColumn: birth_date | Standard (PA) Summary: the
   * date the greyhound was born Remark: Date will be null in the event of the information being
   * unavailable
   *
   * @return a String value
   */
  public String getBirthDate() {
    return birthDate;
  }

  /**
   * Gets the value of the gender property. EntityColumn: gender | Standard (PA) Summary: the gender
   * of the greyhound Remark: Dog - male dog; Bitch - female dog. Gender will be 'Unknown' in the
   * event of the information being unavailable
   *
   * @return a String with Title Case value
   */
  public String getGender() {
    return gender;
  }

  /**
   * Gets the value of the seedName property. EntityColumn: seed_name | Standard (PA) Summary: the
   * greyhound's seed Remark: an example: Wide
   *
   * @return a String with Title Case value
   */
  public String getSeedName() {
    return seedName;
  }

  /**
   * Gets the value of the countryFullName property. EntityColumn: country_full_name | Standard (PA)
   * Summary: the country this greyhound was born in Remark: an example: Great Britain
   *
   * @return a String with Title Case value
   */
  public String getCountryFullName() {
    return countryFullName;
  }

  /**
   * Gets the value of the seasonStatus property. EntityColumn: Summary: the season date of the
   * bitch Remark: an example: 14.De.11. Date will be empty in the event of a male or the
   * information being unavailable
   *
   * @return a String with any date value
   */
  public String getSeasonStatus() {
    return seasonStatus;
  }

  /**
   * Gets the value of the performances property. EntityColumn: performance Summary: the
   * representation of a performance. Remark: {@link Performance }
   *
   * @return List of performance entities
   */
  public List<Performance> getPerformances() {
    return performances;
  }

  /**
   * Gets the value of the performances property. EntityColumn: Generated from greyhound,
   * performance and meeting Example: 312-3213: 312 - last year 3213 - current year 3 - 3th position
   * in first race 1 - 1th position in second race 2 - 2th position in third race Remark: {@link
   * Performance }
   *
   * @return List of performance entities
   */
  public String getForm() {
    return form;
  }

  public void setGreyhoundId(Integer greyhoundId) {
    this.greyhoundId = greyhoundId;
  }

  public void setPaGreyHoundId(Integer paGreyHoundId) {
    this.paGreyHoundId = paGreyHoundId;
  }

  public void setGreyhoundFullName(String greyhoundFullName) {
    this.greyhoundFullName = greyhoundFullName;
  }

  public void setTrainerFullName(String trainerFullName) {
    this.trainerFullName = trainerFullName;
  }

  public void setOwnerFullName(String ownerFullName) {
    this.ownerFullName = ownerFullName;
  }

  public void setDamFullName(String damFullName) {
    this.damFullName = damFullName;
  }

  public void setSireFullName(String sireFullName) {
    this.sireFullName = sireFullName;
  }

  public void setColour(String colour) {
    this.colour = colour;
  }

  public void setBirthDate(String birthDate) {
    this.birthDate = birthDate;
  }

  public void setGender(String gender) {
    this.gender = gender;
  }

  public void setSeedName(String seedName) {
    this.seedName = seedName;
  }

  public void setCountryFullName(String countryFullName) {
    this.countryFullName = countryFullName;
  }

  public void setSeasonStatus(String seasonStatus) {
    this.seasonStatus = seasonStatus;
  }

  public void setForm(String form) {
    this.form = form;
  }

  public void setPerformances(List<Performance> performances) {
    this.performances = performances;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("Greyhound{");
    sb.append("greyhoundId=").append(greyhoundId);
    sb.append(", paGreyHoundId=").append(paGreyHoundId);
    sb.append(", greyhoundFullName='").append(greyhoundFullName).append('\'');
    sb.append(", trainerFullName='").append(trainerFullName).append('\'');
    sb.append(", ownerFullName='").append(ownerFullName).append('\'');
    sb.append(", damFullName='").append(damFullName).append('\'');
    sb.append(", sireFullName='").append(sireFullName).append('\'');
    sb.append(", colour='").append(colour).append('\'');
    sb.append(", birthDate=").append(birthDate);
    sb.append(", gender='").append(gender).append('\'');
    sb.append(", seedName='").append(seedName).append('\'');
    sb.append(", countryFullName='").append(countryFullName).append('\'');
    sb.append(", seasonStatus='").append(seasonStatus).append('\'');
    sb.append(", form='").append(form).append('\'');
    sb.append(", performances=").append(performances);
    sb.append('}');
    return sb.toString();
  }
}
