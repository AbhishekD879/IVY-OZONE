package com.egalacoral.spark.timeform.model.horseracing;

import com.egalacoral.spark.timeform.model.OBRelatedEntity;
import com.egalacoral.spark.timeform.model.greyhound.TimeformEntry;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.google.gson.annotations.SerializedName;
import java.io.Serializable;
import java.util.Objects;
import java.util.Set;

public class HREntry extends OBRelatedEntity implements Serializable, TimeformEntry {

  @SerializedName(value = "meetingDate")
  private String meetingDate;

  @SerializedName(value = "courseId")
  private Integer courseId;

  @SerializedName(value = "raceNumber")
  private Integer raceNumber;

  @SerializedName(value = "horseCode")
  private String horseCode;

  @SerializedName(value = "courseName")
  private String courseName;

  @SerializedName(value = "horseName")
  private String horseName;

  @SerializedName(value = "horseAge")
  private Integer horseAge;

  @SerializedName(value = "horseGender")
  private String horseGender;

  @SerializedName(value = "saddleCloth")
  private String saddleCloth;

  @SerializedName(value = "draw")
  private Integer draw;

  @SerializedName(value = "weightCarried")
  private Integer weightCarried;

  @SerializedName(value = "jockeyName")
  private String jockeyName;

  @SerializedName(value = "jockeyCode")
  private String jockeyCode;

  @SerializedName(value = "apprenticeClaim")
  private Integer apprenticeClaim;

  @SerializedName(value = "trainerName")
  private String trainerName;

  @SerializedName(value = "rating123")
  private Integer rating123;

  @SerializedName(value = "ratingStars")
  private Integer ratingStars;

  @SerializedName(value = "tissuePriceDecimal")
  private String tissuePriceDecimal;

  @SerializedName(value = "tissuePriceFractional")
  private String tissuePriceFractional;

  @SerializedName(value = "equipmentDescription")
  private String equipmentDescription;

  @SerializedName(value = "equipmentChar")
  private String equipmentChar;

  @SerializedName(value = "longHandicap")
  private Integer longHandicap;

  @SerializedName(value = "analystsComments")
  private String analystsComments;

  @SerializedName(value = "silksDescription")
  private String silksDescription;

  @SerializedName(value = "horseInFocus")
  private Integer horseInFocus;

  @SerializedName(value = "warningHorse")
  private Integer warningHorse;

  @SerializedName(value = "jockeyUplift")
  private Integer jockeyUplift;

  @SerializedName(value = "trainerUplift")
  private Integer trainerUplift;

  @SerializedName(value = "horsesForCoursePos")
  private Integer horsesForCoursePos;

  @SerializedName(value = "horsesForCourseNeg")
  private Integer horsesForCourseNeg;

  @SerializedName(value = "hotTrainer")
  private Integer hotTrainer;

  @SerializedName(value = "coldTrainer")
  private Integer coldTrainer;

  @SerializedName(value = "statusDescription")
  private String statusDescription;

  @SerializedName(value = "silkCode")
  private String silkCode;

  @SerializedName(value = "statusId")
  private Integer statusId;

  @SerializedName(value = "formFigures")
  private String formFigures;

  @SerializedName(value = "entryNumber")
  private Integer entryNumber;

  @SerializedName(value = "BHARating")
  private Integer BHARating;

  @SerializedName(value = "crsDisWinFavText")
  private String crsDisWinFavText;

  @SerializedName(value = "daysOff")
  private Integer daysOff;

  @SerializedName(value = "betfairBackPrice")
  private String betfairBackPrice;

  @SerializedName(value = "ratingsAdjustment")
  private Integer ratingsAdjustment;

  @SerializedName(value = "bfSelectionId")
  private String bfSelectionId;

  @SerializedName(value = "sportsbookDecimalOdds")
  private String sportsbookDecimalOdds;

  @SerializedName(value = "sportsbookFractionalOdds")
  private String sportsbookFractionalOdds;

  @SerializedName(value = "equipmentFirstTime")
  private Boolean equipmentFirstTime;

  @SerializedName(value = "sportsbookBetSlipUrl")
  private String sportsbookBetSlipUrl;

  @SerializedName(value = "trainerCode")
  private String trainerCode;

  @SerializedName(value = "ownerCode")
  private String ownerCode;

  @SerializedName(value = "ownerFullName")
  private String ownerFullName;

  @SerializedName(value = "topRated")
  private Boolean topRated;

  @SerializedName(value = "lastRunFlat")
  private Integer lastRunFlat;

  @SerializedName(value = "lastRunJump")
  private Integer lastRunJump;

  @SerializedName(value = "masterInPlaySymbol")
  private String masterInPlaySymbol;

  @SerializedName(value = "winsAtCourse")
  private Integer winsAtCourse;

  @SerializedName(value = "winsAtDistance")
  private Integer winsAtDistance;

  @SerializedName(value = "winsAtCourseDistance")
  private Integer winsAtCourseDistance;

  @JsonIgnore private HRHorse horse;

  @JsonIgnore private transient HREntryKey key;

  @JsonIgnore
  public HREntryKey getKey() {
    if (key == null) {
      key = new HREntryKey(courseId, raceNumber, horseCode);
    }
    return key;
  }

  /**
   * The date of the race the horse is entered at and is part of the primary key Value: Not Null
   *
   * @return Date Remarks: Meeting Date In The Format yyyy-mm-dd and part of the primary key (PK)
   */
  public String getMeetingDate() {
    return meetingDate;
  }

  /**
   * The ID of the course that the horse is entered at and is part of the primary key Value: Above 0
   *
   * @return Integer Remarks: Part of the primary key (PK)
   */
  public Integer getCourseId() {
    return courseId;
  }

  /**
   * The number of the race that the horse is entered at and is part of the primary key Value: Above
   * 0
   *
   * @return Integer Remarks: Part of the primary key (PK)
   */
  public Integer getRaceNumber() {
    return raceNumber;
  }

  /**
   * The code of the horse and is part of the primary key Value: Not Null
   *
   * @return String(12) Remarks: Part of the primary key (PK)
   */
  public String getHorseCode() {
    return horseCode;
  }

  /**
   * The full name of the course that the horse is entered at Value: Upper Case
   *
   * @return String Remarks: An example: HAYDOCK PARK
   */
  public String getCourseName() {
    return courseName;
  }

  /**
   * The full name of the horse, including breeding suffix Value: Upper Case
   *
   * @return String Remarks: An example: KAUTO STAR (FR)
   */
  public String getHorseName() {
    return horseName;
  }

  /**
   * The age of the horse on the day of the race Value: Above 0
   *
   * @return Integer Remarks: An example: 7
   */
  public Integer getHorseAge() {
    return horseAge;
  }

  /**
   * The gender of the horse on the day of the race Value: Lower Case
   *
   * @return String Remarks: Values are : f - filly, m - mare, c - colt, g - gelding, h - entire
   *     horse
   */
  public String getHorseGender() {
    return horseGender;
  }

  /**
   * The number the horse will carry on its saddle cloth Value: Can be 0 (pre declaration stage)
   *
   * @return Integer Remarks: 0 - pre declaration stage, greater than 0 is their saddle cloth number
   */
  public String getSaddleCloth() {
    return saddleCloth;
  }

  /**
   * The number of stall the horse will start from (0 for jump races and pre declaration stage)
   * Value: Can be 0
   *
   * @return Integer Remarks: 0 - jump or pre declaration stage, greater than 0 is the stall number
   */
  public Integer getDraw() {
    return draw;
  }

  /**
   * The weight in pounds the horse is set to carry (from 4/5 day entries) Value: Can be 0
   *
   * @return Integer Remarks: 0 - pre 4/5 day entries, greater than 0 is the weight the horse will
   *     carry
   */
  public Integer getWeightCarried() {
    return weightCarried;
  }

  /**
   * The full name of the jockey booked to ride the horse Value: Can be empty if no jockey has yet
   * been booked to ride
   *
   * @return String Remarks: "" if no jockey has been booked, an example: R. Walsh
   */
  public String getJockeyName() {
    return jockeyName;
  }

  /**
   * The code of the jockey booked to ride the horse Value: Can be empty if no jockey has yet been
   * booked to ride
   *
   * @return String Remarks: "" if no jockey has been booked, an example: "000000000001" if one has
   */
  public String getJockeyCode() {
    return jockeyCode;
  }

  /**
   * The amount in pounds that a horse will have removed from its weight as a result of the jockey
   * Value: Can be 0
   *
   * @return Integer Remarks: 0 = no claim, greater than 0 represents the weight that will be taken
   *     off the horse
   */
  public Integer getApprenticeClaim() {
    return apprenticeClaim;
  }

  /**
   * The full name of the trainer of the horse Value: Can be empty if a trainer is not recorded
   * against the horse
   *
   * @return String Remarks: "" if no trainer is registered for the horse, an example: Paul Nicholls
   */
  public String getTrainerName() {
    return trainerName;
  }

  /**
   * The Timeform 123 selections by analysts Value: Can be 0 if horses isn't selected, great than 0
   * if it has
   *
   * @return Integer Remarks: 1 - Timeform Analysts' Top Pick, 2 - 2nd, 3 - 3rd
   */
  public Integer getRating123() {
    return rating123;
  }

  /**
   * The number of stars attributed to the horses chances by the analyst Value: Will be 0 if the
   * race hasn't been assessed by the analyst, greater than 0 is the number of stars
   *
   * @return Integer Remarks: 0 - hasn't been assessed, 5 - best pick, 1- lowest pick
   */
  public Integer getRatingStars() {
    return ratingStars;
  }

  /**
   * The decimal price that the analyst thinks the horse will start Value: Will be 0.0 if the race
   * hasn't been assessed by the analyst, greater than 0 is the horses predicted price
   *
   * @return Decimal Remarks: 0.0 if the race hasn't been assessed, an example 1.0 = evens
   */
  public String getTissuePriceDecimal() {
    return tissuePriceDecimal;
  }

  /**
   * The price that the analyst thinks the horse will start Value: Will be "" if the race hasn't
   * been assessed by the analyst, otherwise it will be title case
   *
   * @return String Remarks: "" if the race hasn't been assessed, an example: 2/1
   */
  public String getTissuePriceFractional() {
    return tissuePriceFractional;
  }

  /**
   * The full description of any headgear the horse may be wearing Value: Will be "" if the horse
   * isn't wearing any headgear, otherwise Title Case
   *
   * @return String Remarks: "" if no equipment, an example: "Blinkers"
   */
  public String getEquipmentDescription() {
    return equipmentDescription;
  }

  /**
   * A char to represent the headgear any headgear the horse may be wearing Value: Will be "" if the
   * horse isn't wearing any headgear, otherwise a single char
   *
   * @return String(1) Remarks: "" where no headgear is being worn, an example: "b" blinkers
   */
  public String getEquipmentChar() {
    return equipmentChar;
  }

  /**
   * The weight in pounds that the horse may be out of the handicap Value: Will be 0 if the horses
   * isn't out of the handicap, above 0 when it is
   *
   * @return Integer Remarks: 0 where horse is not out of the handicap, an example: 4 where the
   *     horse is 4 pounds out of the handicap
   */
  public Integer getLongHandicap() {
    return longHandicap;
  }

  /**
   * The anaylst comment for the horse's chance in the race Value: Will be "" if the analyst hasn't
   * written a comment for the horse, otherwise it will have a comment
   *
   * @return String Remarks: "" if no comment, an example: "Has a great chance"
   */
  public String getAnalystsComments() {
    return analystsComments;
  }

  /**
   * A textual description of the silks the jockey will be wearing Value: "" if the silks
   * description isn't available, otherwise will be a string
   *
   * @return String Remarks: "" - no silk information available, an example "green hoops"
   */
  public String getSilksDescription() {
    return silksDescription;
  }

  /**
   * Indicates if the horse is a Horse In Focus for this race Value: True or False
   *
   * @return Boolean Remarks: True - horse is a Horse In Focus
   */
  public Integer getHorseInFocus() {
    return horseInFocus;
  }

  /**
   * Indicates if the horse is a Warning Horse for this race Value: True or False
   *
   * @return Boolean Remarks: True - horse is a Warning Horse
   */
  public Integer getWarningHorse() {
    return warningHorse;
  }

  /**
   * Indicates if the horse is a jockey uplift for this race Value: True or False
   *
   * @return Boolean Remarks: True - horse is a jockey uplift
   */
  public Integer getJockeyUplift() {
    return jockeyUplift;
  }

  /**
   * Indicates if the horse is a trainer uplift for this race Value: True or False
   *
   * @return Boolean Remarks: True - horse is a trainer uplift
   */
  public Integer getTrainerUplift() {
    return trainerUplift;
  }

  /**
   * Indicates if the horse is a positive horses for courses for this race Value: True or False
   *
   * @return Boolean Remarks: True - horse is a positive horses for courses
   */
  public Integer getHorsesForCoursePos() {
    return horsesForCoursePos;
  }

  /**
   * Indicates if the horse is a negative horses for courses for this race Value: True or False
   *
   * @return Boolean Remarks: True - horse is a negative horses for courses
   */
  public Integer getHorsesForCourseNeg() {
    return horsesForCourseNeg;
  }

  /**
   * Indicates if the horse has a hot trainer for this race Value: True or False
   *
   * @return Boolean Remarks: True - horse has a hot trainer
   */
  public Integer getHotTrainer() {
    return hotTrainer;
  }

  /**
   * Indicates if the horse has a cold trainer for this race Value: True or False
   *
   * @return Boolean Remarks: True - horse has a cold trainer
   */
  public Integer getColdTrainer() {
    return coldTrainer;
  }

  /**
   * A description of the status that applies to the horse's entry Value: Title Case
   *
   * @return String Remarks: An example: Runner
   */
  public String getStatusDescription() {
    return statusDescription;
  }

  /**
   * The code of the jockey silks to match image files Value: "" if no silks are available, string
   * code if they are
   *
   * @return String Remarks: "" - no silks available, an example: "000000000001"
   */
  public String getSilkCode() {
    return silkCode;
  }

  /**
   * The integer value of the entry status of the horse Value: Above 0
   *
   * @return Remarks: 21 Runner, 22 Non Runner, 23 Withdrawn, 24 Reserve, 38 Dropped out at the five
   *     day stage, 39 Dropped out at the four day stage, 40 Dropped out at the overnight stage, 41
   *     Dropped out during early closers,46 Race Abandoned
   */
  public Integer getStatusId() {
    return statusId;
  }

  /**
   * The horse's past form over the last two seasons in summary Value: "" if the form hasn't been
   * calculated or the horse hasn't run before, a string if it has
   *
   * @return String Remarks: An example: 111P
   */
  public String getFormFigures() {
    return formFigures;
  }

  /**
   * The entry number of the horse Value: 0 if the horse is no longer a runner, above 0 if it is
   *
   * @return Integer Remarks: 0 indicates the horse is no longer entered in the race, above 0 means
   *     it is
   */
  public Integer getEntryNumber() {
    return entryNumber;
  }

  /**
   * The horse's official handicap mark Value: 0 if the horse doesn't have an official rating, above
   * 0 is its mark
   *
   * @return Integer Remarks: 0 - no official mark, greater than 0 is its official mark
   */
  public Integer getBHARating() {
    return BHARating;
  }

  /**
   * Information as to whether the horse has won over the course, distance or is a beaten favourite
   * Value: "" if there is no information, upper case if there is
   *
   * @return String Remarks: BF - Beaten Favourite, C - Course Winner, D - Distance Winner, CD -
   *     Course And Distance Winner
   */
  public String getCrsDisWinFavText() {
    return crsDisWinFavText;
  }

  /**
   * Number of days off the horse has had since its last run Value: Can be null where the horse
   * hasn't run before
   *
   * @return Integer Remarks: NULL - Horse hasn't run before, above 0 where it has
   */
  public Integer getDaysOff() {
    return daysOff;
  }

  /**
   * Latest Betfair Price available on the exchange Value: 0.0 where a price isn't available, above
   * 0.0 is the horses back price
   *
   * @return Decimal Remarks: "" - no price available, An example: 2.0 - evens
   */
  public String getBetfairBackPrice() {
    return betfairBackPrice;
  }

  /**
   * The difference between the horse's master rating and adjusted rating Value: 0 if there is not
   * difference or the horse doesn't have a rating, above 0 is the difference
   *
   * @return Integer Remarks: 0 - no difference or can't be calculated, above 0 is the difference
   */
  public Integer getRatingsAdjustment() {
    return ratingsAdjustment;
  }

  /**
   * Betfair Selection ID of the horse to match to the Betfair API Value: 0 if the market has not
   * yet been formed or the horse is no longer entered, above 0 if it has an ID
   *
   * @return Integer Remarks: 0 - horse can't be mapped to a market, an example 134521
   */
  public String getBfSelectionId() {
    return bfSelectionId;
  }

  /**
   * Betfair Sportsbook decimal odds Value: "" - no odds available
   *
   * @return String Remarks: "" - no price available, An example: 2.0 - evens
   */
  public String getSportsbookDecimalOdds() {
    return sportsbookDecimalOdds;
  }

  /**
   * Betfair Sportsbook odds expressed as a fraction Value: "" - no odds available
   *
   * @return String Remarks: "" - no price available, An example: 1/1 - evens
   */
  public String getSportsbookFractionalOdds() {
    return sportsbookFractionalOdds;
  }

  /**
   * Flag to indicate this is the first time a horse has worn equipment Value: True for yes, false
   * for no
   *
   * @return Boolean Remarks: True or False
   */
  public Boolean getEquipmentFirstTime() {
    return equipmentFirstTime;
  }

  /**
   * Betfair Sportsbook url values Value: "" - no url
   *
   * @return String Remarks: Values required for building sportsbook bet slip url
   */
  public String getSportsbookBetSlipUrl() {
    return sportsbookBetSlipUrl;
  }

  /**
   * The code of the horse's trainer Value: "" if the horse doesn't have a registered trainer, has a
   * code if it does which corresponds to the trainer
   *
   * @return String Remarks: "" - no trainer available for the horse, an example: "000000000001"
   */
  public String getTrainerCode() {
    return trainerCode;
  }

  /**
   * The code of the owner of the horse Value: Can be empty if an owner is not recorded against the
   * horse
   *
   * @return String Remarks: "" if no owner is registered , an example: "000000000001" if one has
   */
  public String getOwnerCode() {
    return ownerCode;
  }

  /**
   * The full name of the owner of the horse Value: Can be empty if an owner is not recorded against
   * the horse, Title Case if it is
   *
   * @return String Remarks: "" if no owner is registered for the horse, an example: Gigginstown
   *     House Stud
   */
  public String getOwnerFullName() {
    return ownerFullName;
  }

  /**
   * Flag to indicate this horse is top rated based on Timeforms premium ratings. Value: True for
   * yes, false for no
   *
   * @return Boolean Remarks: True or False
   */
  public Boolean getTopRated() {
    return topRated;
  }

  /**
   * The number of days since this horse ran in a flat race
   *
   * @return Integer Remarks: 0 to 99999. If 0 the horse has never run on the flat before
   */
  public Integer getLastRunFlat() {
    return lastRunFlat;
  }

  /**
   * The number of days since this horse ran in a jump race
   *
   * @return Integer Remarks: 0 to 99999. If 0 the horse has never run on the jump before
   */
  public Integer getLastRunJump() {
    return lastRunJump;
  }

  /**
   * The master in play symbols for this horse in this race
   *
   * @return String
   */
  public String getMasterInPlaySymbol() {
    return masterInPlaySymbol;
  }

  /**
   * The number of times this horse has won at this course
   *
   * @return Integer Remarks:0 or more
   */
  public Integer getWinsAtCourse() {
    return winsAtCourse;
  }

  /**
   * The number of times this horse has won at this distance
   *
   * @return Integer Remarks:0 or more
   */
  public Integer getWinsAtDistance() {
    return winsAtDistance;
  }

  /**
   * The number of times a horse has won at this course and distance
   *
   * @return Integer Remarks:0 or more
   */
  public Integer getWinsAtCourseDistance() {
    return winsAtCourseDistance;
  }

  public HRHorse getHorse() {
    return horse;
  }

  public void setMeetingDate(String meetingDate) {
    this.meetingDate = meetingDate;
  }

  public void setCourseId(Integer courseId) {
    this.courseId = courseId;
  }

  public void setRaceNumber(Integer raceNumber) {
    this.raceNumber = raceNumber;
  }

  public void setHorseCode(String horseCode) {
    this.horseCode = horseCode;
  }

  public void setCourseName(String courseName) {
    this.courseName = courseName;
  }

  public void setHorseName(String horseName) {
    this.horseName = horseName;
  }

  public void setHorseAge(Integer horseAge) {
    this.horseAge = horseAge;
  }

  public void setHorseGender(String horseGender) {
    this.horseGender = horseGender;
  }

  public void setSaddleCloth(String saddleCloth) {
    this.saddleCloth = saddleCloth;
  }

  public void setDraw(Integer draw) {
    this.draw = draw;
  }

  public void setWeightCarried(Integer weightCarried) {
    this.weightCarried = weightCarried;
  }

  public void setJockeyName(String jockeyName) {
    this.jockeyName = jockeyName;
  }

  public void setJockeyCode(String jockeyCode) {
    this.jockeyCode = jockeyCode;
  }

  public void setApprenticeClaim(Integer apprenticeClaim) {
    this.apprenticeClaim = apprenticeClaim;
  }

  public void setTrainerName(String trainerName) {
    this.trainerName = trainerName;
  }

  public void setRating123(Integer rating123) {
    this.rating123 = rating123;
  }

  public void setRatingStars(Integer ratingStars) {
    this.ratingStars = ratingStars;
  }

  public void setTissuePriceDecimal(String tissuePriceDecimal) {
    this.tissuePriceDecimal = tissuePriceDecimal;
  }

  public void setTissuePriceFractional(String tissuePriceFractional) {
    this.tissuePriceFractional = tissuePriceFractional;
  }

  public void setEquipmentDescription(String equipmentDescription) {
    this.equipmentDescription = equipmentDescription;
  }

  public void setEquipmentChar(String equipmentChar) {
    this.equipmentChar = equipmentChar;
  }

  public void setLongHandicap(Integer longHandicap) {
    this.longHandicap = longHandicap;
  }

  public void setAnalystsComments(String analystsComments) {
    this.analystsComments = analystsComments;
  }

  public void setSilksDescription(String silksDescription) {
    this.silksDescription = silksDescription;
  }

  public void setHorseInFocus(Integer horseInFocus) {
    this.horseInFocus = horseInFocus;
  }

  public void setWarningHorse(Integer warningHorse) {
    this.warningHorse = warningHorse;
  }

  public void setJockeyUplift(Integer jockeyUplift) {
    this.jockeyUplift = jockeyUplift;
  }

  public void setTrainerUplift(Integer trainerUplift) {
    this.trainerUplift = trainerUplift;
  }

  public void setHorsesForCoursePos(Integer horsesForCoursePos) {
    this.horsesForCoursePos = horsesForCoursePos;
  }

  public void setHorsesForCourseNeg(Integer horsesForCourseNeg) {
    this.horsesForCourseNeg = horsesForCourseNeg;
  }

  public void setHotTrainer(Integer hotTrainer) {
    this.hotTrainer = hotTrainer;
  }

  public void setColdTrainer(Integer coldTrainer) {
    this.coldTrainer = coldTrainer;
  }

  public void setStatusDescription(String statusDescription) {
    this.statusDescription = statusDescription;
  }

  public void setSilkCode(String silkCode) {
    this.silkCode = silkCode;
  }

  public void setStatusId(Integer statusId) {
    this.statusId = statusId;
  }

  public void setFormFigures(String formFigures) {
    this.formFigures = formFigures;
  }

  public void setEntryNumber(Integer entryNumber) {
    this.entryNumber = entryNumber;
  }

  public void setBHARating(Integer BHARating) {
    this.BHARating = BHARating;
  }

  public void setCrsDisWinFavText(String crsDisWinFavText) {
    this.crsDisWinFavText = crsDisWinFavText;
  }

  public void setDaysOff(Integer daysOff) {
    this.daysOff = daysOff;
  }

  public void setBetfairBackPrice(String betfairBackPrice) {
    this.betfairBackPrice = betfairBackPrice;
  }

  public void setRatingsAdjustment(Integer ratingsAdjustment) {
    this.ratingsAdjustment = ratingsAdjustment;
  }

  public void setBfSelectionId(String bfSelectionId) {
    this.bfSelectionId = bfSelectionId;
  }

  public void setSportsbookDecimalOdds(String sportsbookDecimalOdds) {
    this.sportsbookDecimalOdds = sportsbookDecimalOdds;
  }

  public void setSportsbookFractionalOdds(String sportsbookFractionalOdds) {
    this.sportsbookFractionalOdds = sportsbookFractionalOdds;
  }

  public void setEquipmentFirstTime(Boolean equipmentFirstTime) {
    this.equipmentFirstTime = equipmentFirstTime;
  }

  public void setSportsbookBetSlipUrl(String sportsbookBetSlipUrl) {
    this.sportsbookBetSlipUrl = sportsbookBetSlipUrl;
  }

  public void setTrainerCode(String trainerCode) {
    this.trainerCode = trainerCode;
  }

  public void setOwnerCode(String ownerCode) {
    this.ownerCode = ownerCode;
  }

  public void setOwnerFullName(String ownerFullName) {
    this.ownerFullName = ownerFullName;
  }

  public void setTopRated(Boolean topRated) {
    this.topRated = topRated;
  }

  public void setLastRunFlat(Integer lastRunFlat) {
    this.lastRunFlat = lastRunFlat;
  }

  public void setLastRunJump(Integer lastRunJump) {
    this.lastRunJump = lastRunJump;
  }

  public void setMasterInPlaySymbol(String masterInPlaySymbol) {
    this.masterInPlaySymbol = masterInPlaySymbol;
  }

  public void setWinsAtCourse(Integer winsAtCourse) {
    this.winsAtCourse = winsAtCourse;
  }

  public void setWinsAtDistance(Integer winsAtDistance) {
    this.winsAtDistance = winsAtDistance;
  }

  public void setWinsAtCourseDistance(Integer winsAtCourseDistance) {
    this.winsAtCourseDistance = winsAtCourseDistance;
  }

  public void setHorse(HRHorse horse) {
    this.horse = horse;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("HREntry{");
    sb.append("meetingDate='").append(meetingDate).append('\'');
    sb.append(", courseId=").append(courseId);
    sb.append(", raceNumber=").append(raceNumber);
    sb.append(", horseCode='").append(horseCode).append('\'');
    sb.append(", courseName='").append(courseName).append('\'');
    sb.append(", horseName='").append(horseName).append('\'');
    sb.append(", horseAge=").append(horseAge);
    sb.append(", horseGender='").append(horseGender).append('\'');
    sb.append(", saddleCloth='").append(saddleCloth).append('\'');
    sb.append(", draw=").append(draw);
    sb.append(", weightCarried=").append(weightCarried);
    sb.append(", jockeyName='").append(jockeyName).append('\'');
    sb.append(", jockeyCode='").append(jockeyCode).append('\'');
    sb.append(", apprenticeClaim=").append(apprenticeClaim);
    sb.append(", trainerName='").append(trainerName).append('\'');
    sb.append(", rating123=").append(rating123);
    sb.append(", ratingStars=").append(ratingStars);
    sb.append(", tissuePriceDecimal='").append(tissuePriceDecimal).append('\'');
    sb.append(", tissuePriceFractional='").append(tissuePriceFractional).append('\'');
    sb.append(", equipmentDescription='").append(equipmentDescription).append('\'');
    sb.append(", equipmentChar='").append(equipmentChar).append('\'');
    sb.append(", longHandicap=").append(longHandicap);
    sb.append(", analystsComments='").append(analystsComments).append('\'');
    sb.append(", silksDescription='").append(silksDescription).append('\'');
    sb.append(", horseInFocus=").append(horseInFocus);
    sb.append(", warningHorse=").append(warningHorse);
    sb.append(", jockeyUplift=").append(jockeyUplift);
    sb.append(", trainerUplift=").append(trainerUplift);
    sb.append(", horsesForCoursePos=").append(horsesForCoursePos);
    sb.append(", horsesForCourseNeg=").append(horsesForCourseNeg);
    sb.append(", hotTrainer=").append(hotTrainer);
    sb.append(", coldTrainer=").append(coldTrainer);
    sb.append(", statusDescription='").append(statusDescription).append('\'');
    sb.append(", silkCode='").append(silkCode).append('\'');
    sb.append(", statusId=").append(statusId);
    sb.append(", formFigures='").append(formFigures).append('\'');
    sb.append(", entryNumber=").append(entryNumber);
    sb.append(", BHARating=").append(BHARating);
    sb.append(", crsDisWinFavText='").append(crsDisWinFavText).append('\'');
    sb.append(", daysOff=").append(daysOff);
    sb.append(", betfairBackPrice='").append(betfairBackPrice).append('\'');
    sb.append(", ratingsAdjustment=").append(ratingsAdjustment);
    sb.append(", bfSelectionId='").append(bfSelectionId).append('\'');
    sb.append(", sportsbookDecimalOdds='").append(sportsbookDecimalOdds).append('\'');
    sb.append(", sportsbookFractionalOdds='").append(sportsbookFractionalOdds).append('\'');
    sb.append(", equipmentFirstTime=").append(equipmentFirstTime);
    sb.append(", sportsbookBetSlipUrl='").append(sportsbookBetSlipUrl).append('\'');
    sb.append(", trainerCode='").append(trainerCode).append('\'');
    sb.append(", ownerCode='").append(ownerCode).append('\'');
    sb.append(", ownerFullName='").append(ownerFullName).append('\'');
    sb.append(", topRated=").append(topRated);
    sb.append(", lastRunFlat=").append(lastRunFlat);
    sb.append(", lastRunJump=").append(lastRunJump);
    sb.append(", masterInPlaySymbol='").append(masterInPlaySymbol).append('\'');
    sb.append(", winsAtCourse=").append(winsAtCourse);
    sb.append(", winsAtDistance=").append(winsAtDistance);
    sb.append(", winsAtCourseDistance=").append(winsAtCourseDistance);
    sb.append(", horse=").append(horse);
    sb.append(", key=").append(key);
    sb.append('}');
    return sb.toString();
  }

  public static class HREntryKey implements Serializable {

    private final int courseId;
    private final int raceNumber;
    private final String horseCode;

    public HREntryKey(int courseId, int raceNumber, String horseCode) {
      this.courseId = courseId;
      this.raceNumber = raceNumber;
      this.horseCode = horseCode;
    }

    public int getCourseId() {
      return courseId;
    }

    public int getRaceNumber() {
      return raceNumber;
    }

    public String getHorseCode() {
      return horseCode;
    }

    @Override
    public boolean equals(Object o) {
      if (this == o) return true;
      if (o == null || getClass() != o.getClass()) return false;
      HREntryKey that = (HREntryKey) o;
      return this.courseId == that.courseId
          && this.raceNumber == that.raceNumber
          && this.horseCode.equals(that.horseCode);
    }

    @Override
    public int hashCode() {
      return Objects.hash(courseId, raceNumber, horseCode);
    }

    @Override
    public String toString() {
      final StringBuilder sb = new StringBuilder("HRMeetingKey{");
      sb.append(", courseId=").append(courseId);
      sb.append(", raceNumber=").append(raceNumber);
      sb.append(", horseCode=").append(horseCode);
      sb.append('}');
      return sb.toString();
    }
  }

  @Override
  public Set<Integer> getObSelectionIds() {
    return getOpenBetIds();
  }
}
